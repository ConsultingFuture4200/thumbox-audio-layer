"""Mimi decode latency benchmark.

Plan 02-02 Task 1 / DEV-1048 / SM-AL-1 / NC-AL-3.

Measures per-chunk decode latency on the provisioned runtime and writes JSON
with p50/p90/p99 plus environment metadata for downstream derate (derate.py)
and the Phase 0 evaluation document (Plan 02-05).
"""

from __future__ import annotations

import json
import os
import platform
import statistics
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import torch
import typer

from .mimi_loop import _load_yaml, encode, load_mimi

app = typer.Typer(no_args_is_help=False, add_completion=False)


def _gpu_sku() -> str:
    if torch.cuda.is_available():
        return torch.cuda.get_device_name(0)
    return "cpu"


def _runtime_version() -> dict:
    """Capture ROCm or CUDA version from environment."""
    info = {"rocm": None, "cuda": None}
    try:
        if torch.cuda.is_available():
            info["cuda"] = getattr(torch.version, "cuda", None)
            info["hip"] = getattr(torch.version, "hip", None)
    except Exception:
        pass
    try:
        out = subprocess.run(
            ["rocminfo"], capture_output=True, text=True, timeout=5
        )
        if out.returncode == 0:
            for line in out.stdout.splitlines():
                if "ROCm Version" in line or "Runtime Version" in line:
                    info["rocm"] = line.split(":", 1)[1].strip()
                    break
    except Exception:
        pass
    return info


def _image_digest(models_lock_path: Path) -> str:
    """Read image digest from models.lock.yaml; fall back to env or 'unknown'."""
    try:
        m = _load_yaml(models_lock_path)
        d = m.get("runtime_image", {}).get("digest")
        if d and not str(d).startswith("sha256:TBD"):
            return d
    except Exception:
        pass
    return os.environ.get("RUNPOD_IMAGE_DIGEST", "unknown")


@app.command()
def bench(
    config: Path = typer.Option(..., "--config"),
    out: Path = typer.Option(..., "--out"),
    n_override: int | None = typer.Option(None, "--n"),
    runtime_override: str | None = typer.Option(None, "--runtime"),
    models_lock: Path = typer.Option(Path("configs/models.lock.yaml"), "--models-lock"),
    runtime_config: Path = typer.Option(Path("configs/runtime.yaml"), "--runtime-config"),
) -> None:
    cfg = _load_yaml(config)
    n = int(n_override or cfg["n_iterations"])
    warmup = int(cfg["warmup_iterations"])
    chunk_ms = int(cfg["chunk_size_ms"])
    sr = int(cfg["sample_rate_hz"])
    seed = int(cfg["seed"])
    profile = runtime_override or cfg["runtime_profile"]
    sync_required = bool(cfg.get("device_synchronize", True))

    np.random.seed(seed)
    torch.manual_seed(seed)

    typer.echo(f"==> loading Mimi (profile={profile})")
    model, fe, runtime_profile = load_mimi(models_lock, runtime_config, profile)
    device = model.device

    # Generate one chunk's worth of audio (chunk_ms at sr) and encode it once
    # to obtain a single-chunk audio_codes tensor we reuse across iterations.
    n_samples = int(sr * chunk_ms / 1000)
    typer.echo(f"==> generating {n_samples}-sample synthetic chunk @ {sr} Hz")
    audio = (np.random.randn(n_samples).astype(np.float32) * 0.05)
    chunk_codes = encode(model, fe, audio, sample_rate=sr)
    typer.echo(f"==> chunk codes shape: {tuple(chunk_codes.shape)}")

    # Warmup
    typer.echo(f"==> warmup ({warmup} iterations)")
    with torch.inference_mode():
        for _ in range(warmup):
            _ = model.decode(chunk_codes)
            if sync_required and torch.cuda.is_available():
                torch.cuda.synchronize()

    # Measurement
    typer.echo(f"==> measuring ({n} iterations)")
    timings_ns = []
    with torch.inference_mode():
        for _ in range(n):
            if sync_required and torch.cuda.is_available():
                torch.cuda.synchronize()
            t0 = time.perf_counter_ns()
            _ = model.decode(chunk_codes)
            if sync_required and torch.cuda.is_available():
                torch.cuda.synchronize()
            t1 = time.perf_counter_ns()
            timings_ns.append(t1 - t0)

    timings_ms = [t / 1_000_000.0 for t in timings_ns]
    p50 = statistics.median(timings_ms)
    p90 = statistics.quantiles(timings_ms, n=10)[8]   # 90th percentile
    p99 = statistics.quantiles(timings_ms, n=100)[98] # 99th percentile

    runtime_info = _runtime_version()
    record = {
        "p50_ms": round(p50, 4),
        "p90_ms": round(p90, 4),
        "p99_ms": round(p99, 4),
        "n_samples": len(timings_ms),
        "warmup_iterations": warmup,
        "chunk_size_ms": chunk_ms,
        "sample_rate_hz": sr,
        "chunk_codes_shape": list(chunk_codes.shape),
        "runtime": str(profile),
        "device": str(device),
        "dtype": str(model.dtype),
        "mimi_revision": _load_yaml(models_lock)["mimi"]["revision"],
        "image_digest": _image_digest(models_lock),
        "gpu_sku": _gpu_sku(),
        "rocm_version": runtime_info.get("rocm"),
        "cuda_version": runtime_info.get("cuda"),
        "torch_version": torch.__version__,
        "python_version": platform.python_version(),
        "seed": seed,
        "timestamp_utc": datetime.now(UTC).isoformat(timespec="seconds"),
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        json.dump(record, f, indent=2)
    typer.echo(f"==> wrote {out}")
    typer.echo(json.dumps(record, indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
