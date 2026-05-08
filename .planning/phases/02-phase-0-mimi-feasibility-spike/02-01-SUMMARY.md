---
phase: 02-phase-0-mimi-feasibility-spike
plan: 01
status: complete
date: 2026-05-07
linear: [DEV-1045, DEV-1046]
---

# Plan 02-01 — Hardware path + provisioning + Mimi encode/decode roundtrip

## Outcome

Mimi encode → log tokens → decode roundtrip is **working end-to-end on cloud A100 80GB PCIe**. Reconstruction shape correct (12.67 Hz frame rate; spec 12.5 Hz), decode latency well under PRD §6.2 kill criterion. Plan 02-02 (decode latency benchmark + VRAM probe) is unblocked.

## Tasks

| Task | Status | Artifact |
|------|--------|----------|
| 1. Hardware path decision | ✅ | `02-01-HARDWARE-PATH-DECISION.md` (Path Cloud, RBOX §7 derate; A100 chosen over MI300X due to RunPod availability — cross-vendor derate accepted with broader CIs flagged in Plan 05) |
| 2. Cloud provisioning | ✅ | RunPod pod `g7wxghi3u6xm4c` (NVIDIA A100 80GB PCIe, $1.39/hr, region RO, template `runpod-torch-v240`) |
| 3. Spike repo skeleton | ✅ | `spike/` directory with uv-managed Python 3.11 env (50 deps + 1 torch wheel installed on pod against CUDA 12.4 index) |
| 4. Mimi encode/decode loop | ✅ | `spike/src/spike/{audio_io,mimi_loop,cli}.py` — 248 LOC total, well under PRD §10.1 ≤500 budget; smoke-test passed on pod |

## Hardware path

**Path Cloud chosen.** Default plan was TensorWave MI300X but RunPod's public catalog (which the operator has authenticated for) does not list MI300X — it's a sales-contact tier. Cheapest viable from RunPod's catalog: NVIDIA A100 80GB PCIe at $1.39/hr (priced moved up from $1.19 listed, accepted).

**Cross-vendor derate caveat:** A100 (CUDA, Hopper-class) → Strix Halo (ROCm, RDNA3.5+CDNA-ish APU) is a wider derate than MI300X → Strix Halo (within-vendor). Plan 02-05 evaluation must publish broader confidence intervals. **Strategic open item:** Linear DEV-1081 (Urgent) — under-$20K hardware reopener — may move the production target away from Strix Halo entirely, reducing derate uncertainty.

**Initial provisioning attempt failed:** image `nvcr.io/nvidia/pytorch:25.04-py3` stalled on first pull (uptime 0s for ~30 min; pod `l4ut7lxn0eq2lh` was deleted). Switched to RunPod-native template `runpod-torch-v240` (`runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`) which is pre-cached on RunPod's registry and came up in seconds.

## Smoke test result

| Metric | Value |
|--------|-------|
| Input audio | 3.0 s synthesized chirp + dual-formant signal, 24 kHz mono, 72000 samples |
| Mimi revision | `89091b3e466eb6a9d11e537bf26b144f194978f7` (HF Hub `main` 2026-05-07) |
| Encode time | 2457.7 ms (includes first-call GPU warmup; not the steady-state number) |
| Decode time | 116.9 ms total |
| Decode per frame | ~3.0 ms (38 frames × 32 codebooks at 12.67 Hz) |
| Output | 72960 samples (input duration preserved within 1.3%) |
| Reconstruction RMS | 0.227 (vs input 0.237) — energy preserved |

PRD §6.2 Phase 0 kill criterion is "Mimi decode > 100ms per chunk" on Strix Halo. On A100 we measured ~3ms per chunk; even with a generous 20× cross-vendor derate the prediction stays well under the kill threshold. **Encouraging signal, not the answer** — Plan 02-02 will run the formal 1000-chunk benchmark with proper warmup, p50/p90/p99, and the explicit Strix Halo derate.

## Notable findings

- **Mimi loaded with `n_q=32` codebooks** (transformers default) rather than the 8 cited in PRD §1.2 / RBOX/Mimi paper. This affects:
  - VRAM (more codebook embeddings resident)
  - Compression ratio (32× more tokens than the n_q=8 case)
  - Latency (decode does 32 codebooks per frame, not 8)
  - Plan 02-02 should both measure n_q=32 (default) AND test n_q=8 (configured) to cover both modes.
  - PRD §1.2 / FR-AL-8 should be re-checked for consistency.
- **Encode warmup matters.** First encode includes model→GPU transfer + JIT compilation. Plan 02-02 latency benchmark must include explicit warmup iterations before measurement.
- **`torch_dtype` deprecation warning** from transformers — non-blocking but worth fixing in Plan 02-02 / general housekeeping.

## Files committed

- `spike/configs/models.lock.yaml` (5 HF revision SHAs + image template ID + pod ID)
- `spike/src/spike/audio_io.py` (57 LOC)
- `spike/src/spike/mimi_loop.py` (136 LOC)
- `spike/src/spike/cli.py` (52 LOC, post-format)
- `spike/pyproject.toml` (per-file-ignore for typer's `B008` false-positive)
- `.planning/phases/02-phase-0-mimi-feasibility-spike/02-01-HARDWARE-PATH-DECISION.md`

## Linear status

- DEV-1045 (env setup) — Delivered
- DEV-1046 (Mimi encode/decode roundtrip) — Delivered

## Cost so far

- Failed pod `l4ut7lxn0eq2lh` (NGC stall): ~$0.70 (~30 min idle)
- Active pod `g7wxghi3u6xm4c` (RunPod-native): ~$0.40 so far (~17 min including bootstrap + smoke test)
- **Cumulative: ~$1.10** of the $200 cap

## Next: Plan 02-02 (Wave 2)

Decode latency benchmark + concurrent VRAM probe. Read-only consumer of `models.lock.yaml`. Will run on the same pod `g7wxghi3u6xm4c` to amortize provisioning cost.
