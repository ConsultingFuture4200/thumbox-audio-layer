# thUMBox Audio Layer

## What This Is

Platform-layer infrastructure that lets thUMBox voice-bearing personality packs (receptionBOX first) consume audio as an LLM-native token stream rather than as text transcripts produced by ASR.

It is **not** a personality pack. Customers don't buy it. It enables receptionBOX (and future voice packs) to achieve latency, expressiveness, and cost characteristics a conventional ASR → text → LLM cascade cannot reach.

## Core Value

Three-phase decomposition with binary go/no-go gates between each phase, each delivering a measurable latency win that compounds:

1. **Predictive-delta ASR** (achievable with existing tools, 6-10 weeks)
2. **LLM-targeted neural audio codec** (research-grade architectural bet, 3-4 months)
3. **Per-firm codec fine-tuning** (the differentiator: "appliance gets faster the more your firm uses it")

The asymmetry argument: a single-tenant on-prem appliance can do per-firm codec fine-tuning that multi-tenant cloud cannot safely do. Same structural argument as receptionBOX Path B, generalized to the codec layer.

## Context

- **Project type:** Platform capability layer — consumed by packs, not a pack itself
- **First consumer:** receptionBOX (slots in as Path E in the v1.5/v2 latency roadmap)
- **Hardware target:** T3 (Strix Halo, 128GB unified memory) only. T2 voice support out of scope.
- **Parent PRD:** `thumbox-technical-prd-v2_1-2026-04-16.md`
- **Source PRD:** `docs/audiolayer-technical-prd-v0_2-2026-05-07.md` (Accepted 2026-05-07; v0.1 strawman preserved as historical baseline at `docs/audiolayer-technical-prd-v0_1-2026-05-07.md`)
- **Linear project:** [thUMBox Audio Layer](https://linear.app/staqs/project/thumbox-audio-layer-51d112886016/overview) (`a281ae7e-5842-4095-a1c9-2b9e6a265404`)

## Source-of-Truth Hierarchy

This `.planning/` directory is the **GSD execution layer**. Linear remains the primary backlog and status surface. When they conflict, Linear wins. The mapping:

| GSD Phase | Linear Milestone | Theme |
|-----------|------------------|-------|
| Phase 1 | M0 — PRD v0.2 & Pre-Phase-0 Resolution | Open items / coordination |
| Phase 2 | M1 — Phase 0: Mimi Feasibility Spike | 2-week timeboxed spike |
| Phase 3 | M2 — Phase 1: Predictive-Delta ASR | 6-10 week build |
| Phase 4 | M3 — Phase 2: Audio Codec Layer | 3-4 month research-grade build |
| Phase 5 | M4 — Phase 3: Per-Firm Codec Fine-Tuning | 6+ month differentiator |

PRD-numbered phases (Phase 0/1/2/3) are referenced by their PRD names; GSD-numbered phases (1-5) are how this roadmap counts.

## Requirements

### Validated

Phase 1 (M0) coordination outcomes — validated 2026-05-07:

- ✓ Naming finalized as "thUMBox Audio Layer"
- ✓ DR-AL-3 adopted (Mimi CC-BY-4.0; commercial appliance distribution clear)
- ✓ NC-AL-9 (Mimi licensing) resolved
- ✓ NC-AL-12 (board appetite) resolved — green-light, internal headcount, Dustin owner
- ✓ NC-AL-6 (audio token storage legal) resolved — FR-AL-12 ship-gate clear
- ✓ Partner corpus Path A — signed agreement landed
- ✓ Path E framing reconciled with receptionBOX latency-unconventional addendum

Functional and non-functional requirements remain hypotheses until Phase 0 spike validates feasibility.

### Active

Pulled from PRD §4 (FR-AL) and §5 (NFR-AL). All 17 FRs and 10 NFRs are hypotheses until shipped and measured. See `.planning/REQUIREMENTS.md` for the full mapping.

### Out of Scope

- TTS pipeline changes (covered in receptionBOX PRD §5.3)
- SIP edge / carrier integration (covered in receptionBOX PRD §4.2)
- Personality pack contract changes (this layer is consumed by packs, not a pack)
- Multi-modal extensions (vision, video) — audio only
- Replacing the ASR pipeline entirely — Audio Layer runs *alongside* ASR through Phase 2
- T2 (Jetson Orin Nano 8GB) voice support — capacity-constrained for receptionBOX v1 alone

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| **DR-AL-1** Audio Layer is platform infrastructure, not a pack | Customers don't buy "audio infrastructure"; gating capability behind pack commerce is artificial | Adopted on PRD acceptance |
| **DR-AL-2** ASR cascade remains in place through all phases; guardrails operate on text | Token-based guardrails are not mature; "you own the data" requires legible audit trail | Adopted on PRD acceptance |
| **DR-AL-3** Mimi (Kyutai) is the Phase 2 codec target | Strongest published track record (Moshi, 12.5Hz real-time inference, established LLM-input semantics). CC-BY-4.0; counsel cleared commercial appliance distribution. | **Adopted (2026-05-07)** — `docs/decisions/dr-al-3-mimi-licensing.md` |
| **DR-AL-4** receptionBOX is the first and only Phase 1/2 consumer | Voice packs are obvious consumers; receptionBOX is the only one in roadmap | Adopted on PRD acceptance |
| **DR-AL-5** Phase 0 is gated on a 2-week timeboxed prototype | Strongest signal on Phase 1 viability is whether basic Mimi pipeline runs at acceptable latency on T3 | Adopted on PRD acceptance |
| **DR-AL-6** FFmpeg/libavcodec patterns inform timing layer; not used as neural runtime | 25 years of solved PTS/DTS/error-resilience patterns; neural inference happens in ONNX/TensorRT/PyTorch | Adopted on PRD acceptance |

## Honest Uncertainty

Captured from PRD §14 — these inform what success looks like and where this project might fail:

1. **Customer-legible value is mostly indirect.** Customers ask for "fast voice," not "audio tokens." Phase 1 alone may make Phases 2/3 commercially unjustifiable even if technically successful.
2. **The asymmetry argument is real but not unique.** Per-firm fine-tuning works for any LLM. Phase 3 differentiation depends on per-firm *codec* fine-tuning specifically producing perceivable effects.
3. **The Phase 2 research bet is genuinely speculative.** No published voice agent ships this architecture. Closest analog (Moshi) couples codec and LLM tightly; we may discover the decoupled architecture doesn't work.
4. **Bandwidth is real.** UMB Group consulting contracts + receptionBOX Phase 1 will absorb most engineering capacity through 2026.
5. **Strongest version may be a research collaboration.** A university lab or small AI research org may be the right Phase 2 partner, not internal headcount.
6. **Codec-as-input may be obsolete by Phase 2 ship.** S2S models (Hertz-dev, Moshi, successors) are moving fast and may collapse the cascade entirely.

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition:**
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active and reflect in Linear
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone:**
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-07 after Phase 1 (M0) completion and PRD v0.2 promotion. Linear milestones M0-M4 mirrored as GSD Phases 1-5; Phase 1 complete, Phase 2 (Mimi feasibility spike) ready to plan.*
