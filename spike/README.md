# thUMBox Audio Layer — Phase 0 Feasibility Spike

> **Project:** thUMBox Audio Layer (`/home/bob/code/thumbox-audio-layer`)
> **Phase:** Phase 2 / GSD Phase 0 / Linear M1
> **Status:** Plan 02-01 in progress (Task 1 ✅ resolved, Task 3 ✅ scaffold landing here, Task 2/4 ⏳ pending cloud provisioning)
> **Linear:** DEV-1045 (env setup), DEV-1046 (Mimi encode/decode loop)
> **Owner:** Dustin

## What this is

A 2-week timeboxed feasibility spike per **PRD §10.1**. Goal: produce binary go/no-go evidence on whether the thUMBox Audio Layer architecture is viable on T3 (Strix Halo) hardware.

**This is NOT production code.** Total LOC budget: **≤500** across all of `src/spike/`.

The spike answers four questions:

1. **Mimi decode latency** on T3-equivalent hardware (PRD SM-AL-1) — Plan 02-02
2. **VRAM at 4 concurrent calls** (PRD NC-AL-1) — Plan 02-02
3. **Pipecat/LiveKit parallel-stream support** (PRD NC-AL-2) — Plan 02-03
4. **LLM-on-tokens coherence** (PRD SM-AL-2; stretch) — Plan 02-04

A fifth deliverable, the **Phase 0 evaluation document** (Plan 02-05), rolls up findings into the Phase 1 go/no-go decision.

## Hardware path

**Path Cloud — TensorWave MI300X (or RunPod / Vultr) with Strix Halo derating.**

See [`../​.planning/phases/02-phase-0-mimi-feasibility-spike/02-01-HARDWARE-PATH-DECISION.md`](../.planning/phases/02-phase-0-mimi-feasibility-spike/02-01-HARDWARE-PATH-DECISION.md) for the full decision rationale, derating commitment, switch criterion, and cost ceiling.

Strix Halo derating methodology: reused from `/home/bob/RBOX/CLAUDE.md` §7.

## Setup (operator workstation)

These steps run on Dustin's workstation. The cloud pod runs `uv sync` separately after provisioning (see "Setup (cloud pod)" below).

```bash
# From the spike/ directory
uv sync                             # resolves and locks pyproject.toml deps (no torch yet)
uv run python -c "import spike; print(spike.__version__)"   # 0.0.1
```

## Setup (cloud pod, after provisioning lands)

`torch` is intentionally NOT in `pyproject.toml`. It must be installed against the right wheel index per provider:

```bash
# On the pod, after pyproject.toml + uv.lock are rsync'd over

# AMD MI300X (TensorWave / Vultr / RunPod-AMD):
uv sync --frozen
uv pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/rocm6.2

# NVIDIA H100 (RunPod-H100; fallback only):
uv sync --frozen
uv pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu124
```

Then verify:

```bash
uv run python -c "import torch; print('torch:', torch.__version__, 'device:', 'cuda' if torch.cuda.is_available() else 'cpu')"
```

For ROCm pods, `torch.cuda.is_available()` returns `True` (PyTorch presents ROCm as cuda).

## Provisioning

Pick a provider; defaults to `tensorwave`:

```bash
GSD_CLOUD_PROVIDER=tensorwave  bash scripts/provision_mi300x.sh
GSD_CLOUD_PROVIDER=runpod-amd  bash scripts/provision_mi300x.sh
GSD_CLOUD_PROVIDER=runpod-h100 bash scripts/provision_mi300x.sh   # CUDA fallback
GSD_CLOUD_PROVIDER=vultr       bash scripts/provision_mi300x.sh
```

The scripts are documentation + idempotent helpers — they do **not** authenticate to providers (the operator does that via web dashboard).

Tear down when not in use to control spend:

```bash
GSD_CLOUD_PROVIDER=tensorwave  bash scripts/teardown_mi300x.sh
```

**Cost ceiling: $200/mo cap.** Soft trigger at $150 to reconfirm with operator. See hardware-path decision doc for full cost framing.

## Run

Once Plan 02-01 Task 4 lands (Mimi encode/decode loop):

```bash
uv run python -m spike.cli encode-decode \
  --input  assets/test-utterances/utt-001.wav \
  --output /tmp/utt-001-recon.wav \
  --tokens-out /tmp/utt-001-tokens.json \
  --runtime rocm
```

Detailed run instructions for the four measurement plans (02-02 / 02-03 / 02-04) are in each plan's `<action>` block.

## Reproducibility

- **Model weights** pinned by Hugging Face revision SHA in `configs/models.lock.yaml` (populated in Plan 02-01 Task 4 with `kyutai/mimi`, `Systran/faster-distil-whisper-large-v3`, `Qwen/Qwen3-4B`, `Qwen/Qwen2.5-0.5B`).
- **Container image** pinned by `sha256:` digest in `configs/models.lock.yaml` and `configs/.image-digest` (gitignored copy of the digest).
- **Python deps** pinned via `uv.lock`.
- **Audio assets** documented per directory README (`assets/test-utterances/README.md`, `assets/llm-eval/README.md`); deterministic acquisition scripts where applicable.
- **Random seeds** fixed at run time per benchmark config.

This pattern matches `/home/bob/RBOX/CLAUDE.md` §9 reproducibility discipline.

## Linear linkage

| Linear ID | Owns | Status |
|-----------|------|--------|
| DEV-1045 | Env setup (provisioning + skeleton) | In progress (this PR scaffolds; closure on Task 2 + Task 3 both landing) |
| DEV-1046 | Mimi encode/decode roundtrip | Pending (Task 4) |
| DEV-1047 | LLM-on-tokens stretch | Plan 02-04 |
| DEV-1048 | Decode latency benchmark | Plan 02-02 |
| DEV-1049 | VRAM at 4 concurrent | Plan 02-02 |
| DEV-1050 | Pipecat/LiveKit framework probe | Plan 02-03 |
| DEV-1051 | FFmpeg/PyTorch streaming probe | Plan 02-03 |
| DEV-1052 | Phase 0 evaluation + go/no-go | Plan 02-05 |

## Layout

```
spike/
├── README.md                       # this file
├── pyproject.toml                  # deps; torch installed separately on cloud pod
├── uv.lock                         # generated by `uv sync`
├── .python-version                 # 3.11
├── configs/
│   ├── runtime.yaml                # rocm / cuda / cpu profiles
│   ├── models.lock.yaml            # pinned HF revisions + image digest (Plan 02-01 Task 4)
│   ├── bench-decode.yaml           # decode-latency benchmark config (Plan 02-02 Task 1)
│   ├── bench-vram.yaml             # VRAM benchmark config (Plan 02-02 Task 2)
│   └── llm-on-tokens.yaml          # LLM stretch config (Plan 02-04 Task 2)
├── src/spike/
│   ├── __init__.py
│   ├── audio_io.py                 # WAV load/save + token JSON dump (Plan 02-01 Task 4)
│   ├── mimi_loop.py                # encode → log tokens → decode (Plan 02-01 Task 4)
│   ├── cli.py                      # typer CLI entrypoint (Plan 02-01 Task 4)
│   ├── bench_mimi_decode.py        # latency benchmark (Plan 02-02 Task 1)
│   ├── bench_vram_concurrent.py    # VRAM probe (Plan 02-02 Task 2)
│   ├── derate.py                   # MI300X→Strix Halo derate (Plan 02-02)
│   ├── adapter.py                  # placeholder linear projection (Plan 02-04 Task 2)
│   └── llm_on_tokens.py            # stretch eval harness (Plan 02-04 Task 2)
├── scripts/
│   ├── provision_mi300x.sh         # provisioning helper for tensorwave/vultr/runpod-amd/runpod-h100
│   └── teardown_mi300x.sh          # symmetric shutdown helper
├── assets/
│   ├── test-utterances/            # 3-5 short WAVs for the encode/decode roundtrip
│   └── llm-eval/                   # 20 utterances for the LLM-on-tokens stretch (Plan 02-04 Task 1)
├── probes/                         # markdown probe documents (Plan 02-03, 02-04)
└── bench/results/                  # JSON measurement outputs (Plans 02-02, 02-04)
```

## Anti-patterns (do NOT)

- ❌ Use real client / receptionBOX call recordings (per PRD §8.3 + operator CLAUDE.md)
- ❌ `pip install` (uv only; matches RBOX §11)
- ❌ Reference unpinned model `revision: "main"` or unpinned image tags
- ❌ Commit credentials, API keys, or SSH endpoints to this repo
- ❌ Exceed $200/mo cloud spend without explicit operator reconfirmation
