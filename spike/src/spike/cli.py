"""Typer CLI entrypoint for the Phase 0 spike.

Plan 02-01 Task 4 / DEV-1046. The ``encode-decode`` command runs the Mimi
roundtrip; future plans add ``bench-decode``, ``bench-vram``, etc.
"""

from __future__ import annotations

import json
from pathlib import Path

import typer

from .mimi_loop import roundtrip

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("encode-decode")
def encode_decode(
    input_wav: Path = typer.Option(
        ..., "--input", "-i", help="Path to input WAV (any sample rate, mono or stereo)."
    ),
    output_wav: Path = typer.Option(
        ..., "--output", "-o", help="Path to write reconstructed WAV (24 kHz mono)."
    ),
    tokens_out: Path = typer.Option(
        ..., "--tokens-out", "-t", help="Path to write Mimi tokens JSON."
    ),
    runtime: str = typer.Option(
        "cuda",
        "--runtime",
        "-r",
        help="Runtime profile: cuda | rocm | cpu (per configs/runtime.yaml).",
    ),
    models_lock: Path = typer.Option(
        Path("spike/configs/models.lock.yaml"), "--models-lock", help="Path to models.lock.yaml."
    ),
    runtime_config: Path = typer.Option(
        Path("spike/configs/runtime.yaml"), "--runtime-config", help="Path to runtime.yaml."
    ),
) -> None:
    """Run the Mimi encode → log → decode roundtrip on one WAV."""
    result = roundtrip(
        input_wav=input_wav,
        output_wav=output_wav,
        tokens_out=tokens_out,
        runtime_profile=runtime,
        models_lock_path=models_lock,
        runtime_path=runtime_config,
    )
    typer.echo(json.dumps(result, indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
