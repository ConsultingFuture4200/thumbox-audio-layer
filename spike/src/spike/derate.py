"""Cross-vendor / cross-architecture derate functions.

Derates cloud GPU measurements (MI300X or A100) to the production target
(originally Strix Halo per PRD §8.3; under-$20K reopener may shift this — see
Linear DEV-1081). The methodology follows /home/bob/RBOX/CLAUDE.md §7:

- **Bandwidth-bound** stages (Mimi decode, LLM decode tokens/sec): derate by
  the realized memory-bandwidth ratio.
- **Compute-bound** stages (encode prefill, adapter forward): derate by the
  Strix Halo prompt-processing penalty (~10–15× per Phoronix Nov 2025).
- **VRAM** is a capacity-fit check, not a ratio derate.

Confidence intervals are propagated explicitly; raw point estimates without
CIs would mislead the Phase 0 evaluation (Plan 02-05).
"""

from __future__ import annotations

# Memory bandwidth (GB/s) — realized values, not spec peaks.
# Sources: AMD data sheet, Phoronix Strix Halo benchmarks, RBOX/CLAUDE.md §7.1.
BANDWIDTH_GB_S = {
    "mi300x": 4240.0,        # ~80% of 5.3 TB/s spec peak
    "a100_80gb_pcie": 1555.0,  # ~80% of 1.94 TB/s spec peak
    "h100_80gb_pcie": 2680.0,  # ~80% of 3.35 TB/s spec peak
    "strix_halo": 212.0,     # measured via rocm_bandwidth_test (RBOX §7.1)
    "rtx_5090": 1792.0,      # ~80% of 2.24 TB/s GDDR7 spec peak
    "rtx_4090": 800.0,       # ~80% of 1008 GB/s spec peak
    "rtx_6000_ada": 768.0,   # ~80% of 960 GB/s spec peak
}

# Compute (relative to A100 = 1.0 for FP16 dense compute, RBOX §3 informed).
# Used for compute-bound stages (encode prefill).
COMPUTE_REL = {
    "mi300x": 1.40,
    "a100_80gb_pcie": 1.00,   # baseline
    "h100_80gb_pcie": 2.10,
    "strix_halo": 0.06,       # ~15× slower than A100 prompt processing per Phoronix
    "rtx_5090": 1.30,
    "rtx_4090": 0.85,
    "rtx_6000_ada": 0.75,
}

# CI band on the bandwidth ratio reflects rocm_bandwidth_test realized-vs-spec
# spread + measurement-to-measurement variance.
BANDWIDTH_CI_FRAC = 0.15  # ±15%

# CI band on compute ratio is wider — cross-vendor compute comparison includes
# kernel maturity, software stack differences, and quantization effects.
COMPUTE_CI_FRAC = 0.30  # ±30%


def derate_decode_latency_to_strix(
    measured_ms: float,
    source_gpu: str = "a100_80gb_pcie",
    method: str = "bandwidth",
) -> dict:
    """Derate a bandwidth-bound decode latency from source GPU to Strix Halo.

    Returns a dict with the predicted Strix Halo latency and a ±15% CI band
    (RBOX §7.1 measurement spread). Use for Mimi decode (memory-bandwidth-bound).
    """
    if method != "bandwidth":
        raise ValueError(f"unsupported method: {method!r}")
    src_bw = BANDWIDTH_GB_S[source_gpu]
    dst_bw = BANDWIDTH_GB_S["strix_halo"]
    ratio = src_bw / dst_bw  # how much slower Strix is, per byte
    predicted = measured_ms * ratio
    return {
        "method": "bandwidth",
        "source_gpu": source_gpu,
        "source_gb_s": src_bw,
        "target_gb_s": dst_bw,
        "ratio": round(ratio, 2),
        "measured_ms": measured_ms,
        "predicted_strix_ms": round(predicted, 2),
        "ci_low_ms": round(predicted * (1 - BANDWIDTH_CI_FRAC), 2),
        "ci_high_ms": round(predicted * (1 + BANDWIDTH_CI_FRAC), 2),
        "ci_pct": BANDWIDTH_CI_FRAC * 100.0,
    }


def derate_compute_to_strix(
    measured_ms: float,
    source_gpu: str = "a100_80gb_pcie",
) -> dict:
    """Derate a compute-bound latency (encode prefill, adapter forward) to Strix Halo.

    Wider CI than bandwidth derate (±30%) reflecting cross-vendor compute
    comparison uncertainty (RBOX §7.3).
    """
    src = COMPUTE_REL[source_gpu]
    dst = COMPUTE_REL["strix_halo"]
    ratio = src / dst
    predicted = measured_ms * ratio
    return {
        "method": "compute",
        "source_gpu": source_gpu,
        "source_rel": src,
        "target_rel": dst,
        "ratio": round(ratio, 2),
        "measured_ms": measured_ms,
        "predicted_strix_ms": round(predicted, 2),
        "ci_low_ms": round(predicted * (1 - COMPUTE_CI_FRAC), 2),
        "ci_high_ms": round(predicted * (1 + COMPUTE_CI_FRAC), 2),
        "ci_pct": COMPUTE_CI_FRAC * 100.0,
    }


def derate_vram_to_strix(
    measured_gb: float,
    strix_halo_allocatable_gb: float = 96.0,
) -> dict:
    """Capacity-fit check: does measured VRAM fit Strix Halo's allocatable budget?

    Strix Halo has 128 GB unified memory; BIOS-configurable GPU allocation up
    to ~120 GB. Default conservative assumption is 96 GB allocatable.
    Plan 02-05 should publish pass/fail across {64, 96, 120} for sensitivity.
    """
    fits = measured_gb <= strix_halo_allocatable_gb
    return {
        "method": "capacity-fit",
        "measured_gb": measured_gb,
        "strix_halo_allocatable_gb": strix_halo_allocatable_gb,
        "fits": fits,
        "headroom_gb": round(strix_halo_allocatable_gb - measured_gb, 2),
    }


if __name__ == "__main__":
    # Sanity smoke test (full unit tests in spike/tests/test_derate.py).
    bw_a100 = BANDWIDTH_GB_S["a100_80gb_pcie"]
    bw_strix = BANDWIDTH_GB_S["strix_halo"]
    expected_ratio = bw_a100 / bw_strix
    result = derate_decode_latency_to_strix(50.0, source_gpu="a100_80gb_pcie")
    print(f"50ms on A100 → predicted {result['predicted_strix_ms']}ms on Strix")
    print(f"   ratio={result['ratio']} (expected {expected_ratio:.2f})")
    print(f"   CI: {result['ci_low_ms']}–{result['ci_high_ms']}ms")

    vram = derate_vram_to_strix(48.0)
    print(f"48 GB measured → fits Strix? {vram['fits']} (headroom {vram['headroom_gb']} GB)")
