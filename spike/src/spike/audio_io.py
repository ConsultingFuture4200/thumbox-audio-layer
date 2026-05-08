"""Audio I/O helpers for the Phase 0 spike.

Wraps soundfile + librosa.resample for mono PCM WAV load/save and dumps Mimi
audio token tensors to JSON for inspection. Pure I/O — no model logic.

Plan 02-01 Task 4 / DEV-1046.
"""

from __future__ import annotations

import json
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf


def load_wav(path: Path, target_sr: int) -> np.ndarray:
    """Load a mono PCM WAV at any sample rate; resample to ``target_sr``.

    Returns float32 samples in [-1.0, 1.0]. Multichannel inputs are downmixed
    to mono via simple mean. Mimi expects 24 kHz; the spike resamples 16 kHz
    inputs in this function rather than during inference.
    """
    samples, sr = sf.read(str(path), always_2d=False)
    if samples.ndim > 1:
        samples = samples.mean(axis=1)
    samples = samples.astype(np.float32)
    if sr != target_sr:
        samples = librosa.resample(samples, orig_sr=sr, target_sr=target_sr)
    return samples


def save_wav(path: Path, samples: np.ndarray, sr: int) -> None:
    """Write mono PCM WAV at the given sample rate. Float32 [-1.0, 1.0]."""
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), samples.astype(np.float32), sr, subtype="FLOAT")


def dump_tokens(path: Path, codes, metadata: dict) -> None:
    """Write Mimi audio token tensor as JSON for inspection / downstream probes.

    ``codes`` is a torch.Tensor of shape [B=1, n_q, T]; we move to CPU and dump
    as nested int lists. Metadata captures shape and runtime context.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = codes.detach().cpu().numpy().astype(np.int32)
    payload = {
        "metadata": metadata,
        "shape": list(arr.shape),
        "n_q": int(arr.shape[1]),
        "n_frames": int(arr.shape[2]),
        "codes": arr.tolist(),
    }
    with path.open("w") as f:
        json.dump(payload, f)
