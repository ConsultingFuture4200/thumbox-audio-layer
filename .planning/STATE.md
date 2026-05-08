# Project State

## Current Status

**Phase:** Phase 2 (Phase 0 — Mimi Feasibility Spike) — Plan 02-01 in progress (Tasks 1, 3 complete; Task 2 cloud provisioning landed; Task 4 pending pod SSH-ready)
**Last action:** RunPod A100 80GB pod `l4ut7lxn0eq2lh` provisioned ($1.39/hr); 1Password vault `thUMBox Audio Layer` created; Linear DEV-1081 filed for under-$20K hardware reopener.
**Date:** 2026-05-07

## Phase Progress

| # | Phase | Status |
|---|-------|--------|
| 1 | PRD v0.2 & Pre-Phase-0 Resolution | ✅ Complete (2026-05-07) |
| 2 | Phase 0 — Mimi Feasibility Spike | 🟡 In progress (Plan 02-01 partial) |
| 3 | Phase 1 — Predictive-Delta ASR | ⏳ Blocked on Phase 2 + receptionBOX v1 |
| 4 | Phase 2 — Audio Codec Layer | ⏳ Blocked on Phase 3 |
| 5 | Phase 3 — Per-Firm Codec Fine-Tuning | ⏳ Blocked on Phase 4 + 60d stable production |

## Secrets — 1Password Vault

**Vault:** `thUMBox Audio Layer` (ID `wzvdy2vtb5qivb6bynkx5i33j4`)
**Account:** dustin@umbadvisors.com
**Scope:** API keys, tokens, and SSH key material only — no metadata or notes. Project documentation and operational notes (partner agreement details, spending caps, pod metadata) live in the repo (`docs/decisions/`, `.planning/phases/`) or in Heron Labs CRM, not the vault.

**Current items:**
- `RunPod API Key` — `runpodctl` auth (rotate `rpa_MX0K…` which was leaked in chat 2026-05-07)
- `TensorWave API Key` — fallback if MI300X path is pursued
- `Hugging Face Token` — pinned model downloads (Mimi, Whisper, Qwen3-4B, Qwen2.5-0.5B)
- `GitHub PAT — thumbox-audio-layer` — non-`gh`-CLI access (CI, Linear webhooks, automation)

**To be added:**
- `Pod SSH Key — thumbox-spike-mimi` — when pod SSH is ready and an SSH key strategy is chosen

**Access:** `op` CLI on Linux requires desktop-CLI integration enabled in the 1Password app, OR manual `eval $(op signin)` per shell. Operator-driven (not Claude-driven) due to fragile Linux desktop-CLI socket.

## Phase 1 Outcomes

All 6 PRD §13 review items resolved:

- **Naming:** kept "thUMBox Audio Layer"
- **DR-AL-3 / NC-AL-9 (Mimi licensing):** adopted (CC-BY-4.0 clean approval)
- **NC-AL-12 (Phase 2 board appetite):** green-light, internal headcount, Dustin owner
- **NC-AL-6 (audio token storage legal):** clear; FR-AL-12 ship-gate cleared
- **Partner corpus:** Path A (signed agreement; details in Heron Labs CRM)
- **Path E reconciliation:** Strategy 2 + cross-repo patch staged + applied to RBOX (commit 34b6d7f)

PRD v0.2 promoted: `docs/audiolayer-technical-prd-v0_2-2026-05-07.md` (status = Accepted).
v0.1 historical baseline preserved at `docs/audiolayer-technical-prd-v0_1-2026-05-07.md` (byte-identical).

Decision audit trail: `docs/decisions/` (6 documents) + `.planning/phases/02-phase-0-mimi-feasibility-spike/02-01-HARDWARE-PATH-DECISION.md`.

## Phase 2 Outcomes (so far)

- **Plan 02-01 Task 1** ✅ Hardware path = Path Cloud (decision doc committed d07a8f7)
- **Plan 02-01 Task 2** ✅ Cloud provisioning landed: RunPod A100 80GB PCIe `l4ut7lxn0eq2lh`, $1.39/hr, image `nvcr.io/nvidia/pytorch:25.04-py3`, 100GB volume at `/workspace`. SSH endpoint pending — image still pulling.
- **Plan 02-01 Task 3** ✅ Spike repo skeleton committed (1b8e449) — uv-managed Python 3.11 env, runtime profiles, provisioning helpers, README.
- **Plan 02-01 Task 4** ⏳ Mimi encode/decode loop — pending pod SSH-ready.

**Strategic open item:** Linear DEV-1081 (Urgent) — under-$20K hardware reopener. Surfaces a reopen of PRD §8.3 hardware tier (Strix Halo) given Dustin's expressed openness to other hardware in the under-$20K class. Cross-project impact (receptionBOX). Phase 2 spike continues on A100 cloud regardless; derate target may move from Strix Halo to a different production target after the review.

## Recent Decisions

- **2026-05-07** RunPod A100 PCIe chosen over TensorWave MI300X for Phase 2 spike (cheapest viable cloud path; cross-vendor derate to Strix Halo with broader CIs documented).
- **2026-05-07** 1Password project vault scope locked to **secrets-only** (API keys, tokens, SSH key material). Project metadata stays in repo / CRM.
- **2026-05-07** Phase 1 complete in single session via inline draft mode (no executor agents spawned). Saved subagent budget for downstream technical phases.
- **2026-05-07** Lightweight GSD scaffold chosen over full `/gsd-new-project` flow.
- **2026-05-07** Linear is primary source of truth for issue status; `.planning/` is the GSD execution layer only.

## Next Action

When pod SSH is ready (poll: `runpodctl pod get l4ut7lxn0eq2lh -o json | grep host`), resume `/gsd-execute-phase 2 --interactive` from Plan 02-01 Task 4: pin 5 model SHAs in `spike/configs/models.lock.yaml`, write `src/spike/{audio_io,mimi_loop,cli}.py`, run encode/decode roundtrip on the pod, verify reconstruction is audible, close DEV-1045 / DEV-1046.

In parallel, DEV-1081 (Urgent — hardware reopener) needs a board sync before any production-hardware commitment.

---
*Last updated: 2026-05-07 after RunPod pod provisioning + 1Password vault creation.*
