"""Mimi encode → log tokens → decode loop.

Core feasibility harness for Plan 02-01 Task 4 / DEV-1046. Loads the pinned
Kyutai Mimi model, encodes a WAV to discrete audio codes, dumps the codes to
JSON, decodes back to audio, and writes the reconstruction.

Plans 02-02 (decode latency benchmark) and 02-04 (LLM-on-tokens stretch) hook
into ``load_mimi``, ``encode``, and ``decode`` rather than re-implementing the
loop.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import torch
import yaml
from transformers import AutoFeatureExtractor, MimiModel

from .audio_io import dump_tokens, load_wav, save_wav


def _load_yaml(path: Path) -> dict:
    with Path(path).open() as f:
        return yaml.safe_load(f)


def load_mimi(
    models_lock_path: Path,
    runtime_path: Path,
    runtime_profile: str,
) -> tuple[MimiModel, AutoFeatureExtractor, dict]:
    """Load the pinned Mimi model and feature extractor onto the chosen device.

    Returns ``(model, feature_extractor, runtime_config)``. Model is on the
    profile's device in eval mode. ``runtime_config`` is the resolved profile
    dict from ``runtime.yaml``.
    """
    models = _load_yaml(models_lock_path)
    runtime = _load_yaml(runtime_path)

    profile = runtime["profiles"][runtime_profile]
    device = profile["device"]
    dtype_str = profile["dtype"]
    dtype = {"float16": torch.float16, "float32": torch.float32, "bfloat16": torch.bfloat16}[
        dtype_str
    ]

    mimi_cfg = models["mimi"]
    repo_id = mimi_cfg["repo_id"]
    revision = mimi_cfg["revision"]

    fe = AutoFeatureExtractor.from_pretrained(repo_id, revision=revision)
    model = MimiModel.from_pretrained(repo_id, revision=revision, torch_dtype=dtype)
    model = model.to(device)
    model.eval()

    return model, fe, profile


@torch.inference_mode()
def encode(
    model: MimiModel,
    fe: AutoFeatureExtractor,
    audio: np.ndarray,
    sample_rate: int,
) -> torch.Tensor:
    """Encode mono PCM audio to Mimi audio codes [B=1, n_q, T]."""
    inputs = fe(raw_audio=audio, sampling_rate=sample_rate, return_tensors="pt")
    input_values = inputs["input_values"].to(model.device)
    if model.dtype != torch.float32:
        input_values = input_values.to(model.dtype)
    out = model.encode(input_values)
    return out.audio_codes


@torch.inference_mode()
def decode(model: MimiModel, codes: torch.Tensor) -> np.ndarray:
    """Decode Mimi audio codes back to mono PCM at the model's native sample rate."""
    out = model.decode(codes.to(model.device))
    waveform = out[0]
    samples = waveform.detach().cpu().to(torch.float32).numpy()
    if samples.ndim == 3:
        samples = samples[0, 0]
    elif samples.ndim == 2:
        samples = samples[0]
    return samples


def roundtrip(
    input_wav: Path,
    output_wav: Path,
    tokens_out: Path,
    runtime_profile: str = "cuda",
    models_lock_path: Path = Path("spike/configs/models.lock.yaml"),
    runtime_path: Path = Path("spike/configs/runtime.yaml"),
) -> dict:
    """End-to-end encode → log → decode for one WAV."""
    model, fe, profile = load_mimi(models_lock_path, runtime_path, runtime_profile)
    target_sr = profile["mimi_sample_rate"]

    audio = load_wav(input_wav, target_sr)
    duration_s = float(len(audio)) / target_sr

    t_encode_start = time.perf_counter()
    codes = encode(model, fe, audio, sample_rate=target_sr)
    t_encode_ms = (time.perf_counter() - t_encode_start) * 1000.0

    metadata = {
        "input_wav": str(input_wav),
        "input_sample_rate": target_sr,
        "duration_s": duration_s,
        "encode_total_ms": t_encode_ms,
        "device": str(model.device),
        "dtype": str(model.dtype),
        "mimi_revision": _load_yaml(models_lock_path)["mimi"]["revision"],
    }
    dump_tokens(tokens_out, codes, metadata)

    t_decode_start = time.perf_counter()
    recon = decode(model, codes)
    t_decode_ms = (time.perf_counter() - t_decode_start) * 1000.0

    save_wav(output_wav, recon, target_sr)

    return {
        **metadata,
        "decode_total_ms": t_decode_ms,
        "n_q": int(codes.shape[1]),
        "n_frames": int(codes.shape[2]),
        "output_wav": str(output_wav),
        "tokens_out": str(tokens_out),
        "recon_samples": int(len(recon)),
    }
