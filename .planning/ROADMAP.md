# Roadmap

5 phases mirroring Linear milestones M0-M4. Linear is the operational source of truth; this roadmap is the GSD execution layer.

## Overview

| # | Phase | Linear | Goal | Window | Gate |
|---|-------|--------|------|--------|------|
| 1 | PRD v0.2 & Pre-Phase-0 Resolution | M0 | Resolve PRD §13 open items; promote PRD to v0.2 | now | Naming + NC-AL-9 + NC-AL-12 + NC-AL-6 + corpus path |
| 2 | Phase 0 — Mimi Feasibility Spike | M1 | Binary go/no-go for Phase 1 | 2 weeks | SM-AL-1 + SM-AL-2 pass; NC-AL-1 within capacity |
| 3 | Phase 1 — Predictive-Delta ASR | M2 | Ship predictor + delta processor; ≥100ms p90 win on high-confidence calls | 6-10 weeks | SM-AL-3 ≥ 100ms; no regression in NFR-AL-9/10 |
| 4 | Phase 2 — Audio Codec Layer | M3 | Mimi codec + adapter in production parallel to ASR; ≥200ms p90 win | 3-4 months | SM-AL-5 ≥ 200ms; no regression in NFR-AL-9/10; VRAM ≤ 8GB |
| 5 | Phase 3 — Per-Firm Codec Fine-Tuning | M4 | On-appliance per-firm head; ≥30% compression on firm patterns | 6+ months | SM-AL-7 ≥ 30%; NC-AL-8 privacy defensibility cleared |

---

## Phase 1: PRD v0.2 & Pre-Phase-0 Resolution

**Goal:** Resolve all PRD §13 review items so the project moves from "strawman" to "committed scope" and unblocks the Phase 0 spike.

**Linear milestone:** M0 — `c223bf7d-68a6-4670-9a25-374cf3b64530`

**Requirements:** No FRs. Coordination outcomes only — see Linear DEV-1037 through DEV-1044.

**Success criteria:**
1. Naming finalized (DEV-1038)
2. NC-AL-9 Mimi licensing position recorded; DR-AL-3 promoted from candidate (DEV-1039)
3. NC-AL-12 board appetite for Phase 2 documented; staffing plan exists if green-lit (DEV-1040)
4. NC-AL-6 legal position on audio token storage written (DEV-1041)
5. Partner firm 90-day corpus path with signed data agreement (DEV-1042)
6. PRD v0.2 committed; project moves out of Backlog into In Progress (DEV-1044)

**Issues:** DEV-1037, DEV-1038, DEV-1039, DEV-1040, DEV-1041, DEV-1042, DEV-1043, DEV-1044

---

## Phase 2: Phase 0 — Mimi Feasibility Spike

**Goal:** 2-week timeboxed prototype on T3 hardware producing a binary go/no-go for Phase 1.

**Linear milestone:** M1 — `6a997a77-d81b-4431-81f9-0e1c28788b19`

**Requirements:** SM-AL-1, SM-AL-2, NC-AL-1, NC-AL-3, NC-AL-11.

**Success criteria:**
1. Mimi decode < 100ms per chunk on Strix Halo (SM-AL-1) — DEV-1048
2. LLM produces *any* coherent behavior on audio token input over a 20-utterance test set (SM-AL-2) — DEV-1047
3. VRAM at 4 concurrent calls fits Strix Halo capacity (NC-AL-1) — DEV-1049
4. Spike repository (200-500 lines) reproducible from a clean checkout — DEV-1046
5. Phase 0 evaluation document committed; Phase 1 unblocked or project paused — DEV-1052

**Kill criteria (PRD §6.2):**
- Mimi decode > 100ms per chunk after reasonable optimization
- No coherent LLM behavior on audio tokens within 2-week timebox
- VRAM exceeds Strix Halo capacity

**Issues:** DEV-1045, DEV-1046, DEV-1047, DEV-1048, DEV-1049, DEV-1050, DEV-1051, DEV-1052

**Depends on:** Phase 1 (M0) completing — specifically NC-AL-9, NC-AL-12.

---

## Phase 3: Phase 1 — Predictive-Delta ASR

**Goal:** Ship the predictor + delta processor as an opt-in optimization within receptionBOX's existing cascade. Measurable latency win on high-confidence calls without architectural changes for non-opt-in packs.

**Linear milestone:** M2 — `ede089ae-ff4d-462e-86e8-b03ea6a15c9a`

**Requirements:** FR-AL-1, FR-AL-2, FR-AL-3, FR-AL-4, FR-AL-5, FR-AL-6, FR-AL-7, NFR-AL-1, NFR-AL-2, NFR-AL-6, NFR-AL-8, SM-AL-3, SM-AL-4, NFR-AL-9, NFR-AL-10.

**Success criteria:**
1. Predictor training pipeline produces a model meeting NFR-AL-8 (≥ 60% utterance match) — DEV-1053
2. Confidence threshold T calibrated; high-confidence rate ≥ 40% (SM-AL-4) — DEV-1054
3. Delta processor ships; FR-AL-3 commit/divergence behavior verified — DEV-1055
4. Production deploy to first partner firm; A/B telemetry shows SM-AL-3 ≥ 100ms p90 reduction — DEV-1059
5. NFR-AL-9 and NFR-AL-10 invariants hold in A/B comparison
6. Phase 1 evaluation document with explicit Phase 2 go / pause / no-go decision — DEV-1060

**Kill criteria (PRD §6.2):**
- Predictor accuracy plateaus < 40% utterance match
- Phase 1 latency reduction p90 < 50ms after full implementation
- Predictor inference > 100ms p90

**Issues:** DEV-1053, DEV-1054, DEV-1055, DEV-1056, DEV-1057, DEV-1058, DEV-1059, DEV-1060

**Depends on:** Phase 2 (M1) success criteria met. receptionBOX v1 production-stable. Partner corpus delivered (DEV-1042 from M0).

---

## Phase 4: Phase 2 — Audio Codec Layer

**Goal:** Mimi codec integrated as parallel pipeline alongside ASR; LLM consumes audio tokens via fine-tuned adapter; ASR continues in parallel for guardrails + audit. Research-grade architectural bet.

**Linear milestone:** M3 — `cb41fa00-bdd0-45cd-8ad7-76f86484b4b1`

**Requirements:** FR-AL-8, FR-AL-9, FR-AL-10, FR-AL-11, FR-AL-12, FR-AL-13, FR-AL-14, NFR-AL-3, NFR-AL-4, NFR-AL-5, NFR-AL-6, SM-AL-5, SM-AL-6, NFR-AL-9, NFR-AL-10. Plus open questions NC-AL-4, NC-AL-5, NC-AL-7, NC-AL-10.

**Success criteria:**
1. Mimi encoder hits NFR-AL-3 (≤ 30ms per 80ms chunk) under 4-concurrent load — DEV-1061
2. Adapter trained; intent classification accuracy on audio tokens within NFR-AL-9 of text baseline — DEV-1062
3. Parallel ASR + codec pipeline shipped; guardrails operate on text per FR-AL-11; LLM on tokens per FR-AL-9 — DEV-1063
4. SM-AL-5 ≥ 200ms p90 reduction over Phase 1 baseline; NFR-AL-9 / NFR-AL-10 invariants hold
5. NC-AL-7 audio-token prompt-injection threat model documented; ship gate cleared — DEV-1067
6. Phase 2 evaluation document with explicit Phase 3 go / pause / no-go decision — DEV-1071

**Kill criteria (PRD §6.2):**
- Phase 2 latency reduction over Phase 1 < 100ms p90
- Intent classification regresses by > 2 percentage points
- Any measurable guardrail recall regression
- VRAM > 8GB after reasonable optimization

**Issues:** DEV-1061, DEV-1062, DEV-1063, DEV-1064, DEV-1065, DEV-1066, DEV-1067, DEV-1068, DEV-1069, DEV-1070, DEV-1071

**Depends on:** Phase 3 (M2) success criteria met. NC-AL-9 (Mimi licensing) and NC-AL-12 (board appetite) resolved in Phase 1 (M0).

---

## Phase 5: Phase 3 — Per-Firm Codec Fine-Tuning

**Goal:** Per-firm fine-tuned codec head trained on-appliance from the firm's 90-day call corpus. The marketing-legible differentiator: "appliance gets faster the more your firm uses it."

**Linear milestone:** M4 — `de74e562-f23f-471b-87d9-b682d0e7fee4`

**Requirements:** FR-AL-15, FR-AL-16, FR-AL-17, NFR-AL-7, SM-AL-7. Plus NC-AL-8 privacy defensibility.

**Success criteria:**
1. Base encoder + firm-specific head architecture documented and trained — DEV-1072
2. On-appliance training pipeline runs with zero outbound network calls during training — DEV-1073
3. NC-AL-8 privacy defensibility position written; ship gate cleared by external review — DEV-1074
4. SM-AL-7 ≥ 30% compression on firm-specific patterns; downstream NFR-AL-9 / NFR-AL-10 hold
5. Telemetry surfaces actionable codec drift / distribution-shift signals — DEV-1076
6. Phase 3 evaluation: retain / refine / retire recommendation against differentiator claim

**Kill criteria (PRD §6.2):**
- Per-firm fine-tuning < 15% compression improvement (half target)
- Privacy-preserving training cannot survive plausible audit
- Hot-swap of firm heads cannot be made robust against state corruption

**Issues:** DEV-1072, DEV-1073, DEV-1074, DEV-1075, DEV-1076

**Depends on:** Phase 4 (M3) in production for ≥ 60 days with stable behavior.

---

## Coverage

All 17 FRs and all 10 NFRs from PRD v0.1 are mapped to exactly one phase, except cross-phase invariants (NFR-AL-6, NFR-AL-9, NFR-AL-10, SM-AL-8, SM-AL-9) which apply to Phases 3-5 inclusive. All 12 NC-AL open questions are tracked in Linear and surfaced at the phase that blocks on them.

## Notes

- **Phase numbering note.** PRD uses Phase 0/1/2/3 for the technical phases; GSD numbers them 1-5 (counting M0 prep as Phase 1). Phase titles preserve the PRD names.
- **Linear is the source of truth for issue status.** GSD will track phase artifacts here; status stays in Linear.
- **Auto-advance is OFF.** Each phase requires explicit `/gsd-plan-phase N` to begin. Gates between phases are honored.
