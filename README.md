# thUMBox Audio Layer

Platform-layer capability that lets thUMBox voice-bearing packs (receptionBOX first) consume audio as an LLM-native token stream rather than as text transcripts produced by ASR.

**Linear:** [thUMBox Audio Layer](https://linear.app/staqs/project/thumbox-audio-layer-51d112886016/overview)
**Status:** v0.1 PRD draft (2026-05-07) — strawman, pre-pressure-test
**Hardware target:** T3 (Strix Halo, 128GB unified memory) only. T2 voice support out of scope.
**First consumer:** receptionBOX (slots in as "Path E" in the latency-unconventional addendum)

## Why

The conventional ASR → text → LLM cascade has three structural problems:

- **Lossy** — text discards prosody, emphasis, hesitation, emotional valence
- **Serial** — LLM cannot start until ASR commits to a transcription
- **Compression mismatch** — text is ~10,000× more compressed than raw audio; useful middle ground exists

## Three-phase decomposition

| Phase | Scope | Timebox | Expected p90 reduction |
|-------|-------|---------|------------------------|
| **0** | Mimi feasibility prototype on T3, binary go/no-go | 2 weeks | — |
| **1** | Predictive-delta ASR | 6–10 weeks | 80–150 ms |
| **2** | LLM-targeted neural audio codec (research-grade) | 3–4 months | +150–300 ms (if it works) |
| **3** | Per-firm codec fine-tuning — the differentiator | TBD | "appliance gets faster the more your firm uses it" |

## Asymmetry argument

A single-tenant appliance can do per-firm codec fine-tuning that multi-tenant cloud cannot safely do. Same structural argument as receptionBOX Path B (exemplar cache), generalized to the codec layer.

## Parent documents

- `thumbox-technical-prd-v2_1-2026-04-16.md` — parent platform PRD
- `receptionbox-technical-prd-v0_2-2026-05-06.md` — first consumer
- `addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md` — composes with Paths A and B

## Tracked issues

- [DEV-1037](https://linear.app/staqs/issue/DEV-1037/thumbox-audio-layer-research-spike-prd-v01) — research-spike PRD v0.1
