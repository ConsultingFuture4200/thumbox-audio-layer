# NC-AL-12 — Board / Team Appetite for Phase 2 Research Commitment

**Status:** PENDING-BOARD-DECISION
**Linear:** [DEV-1040](https://linear.app/staqs/issue/DEV-1040)
**Resolves:** PRD §7 NC-AL-12; gates Phase 4 (Audio Codec Layer / GSD Phase 4 = Linear M3) commitment.
**Created:** 2026-05-07
**Author:** Dustin (Claude prep)

---

## Board Sync Memo (one-pager)

### Ask

**Does Heron Labs / UMB Group leadership commit to staffing Phase 2 (3–4 months, research-grade) of the thUMBox Audio Layer, conditional on the Phase 0 spike succeeding and Phase 1 production results clearing the Phase 2 entry gate?**

### Phase 2 scope summary (from PRD §2.3, §3.3)

- **Mimi codec integrated as parallel pipeline alongside ASR.** LLM consumes audio tokens via fine-tuned adapter; ASR continues in parallel for guardrails + audit (DR-AL-2).
- **Adapter training.** Trained projection layer maps Mimi audio tokens into a representation Qwen3-4B consumes via cross-attention on a fine-tuned input embedding. Research-grade work; no published voice agent ships this exact architecture.
- **Token-aware transcript persistence + Phase 2 ship-gate verification.** Audio token storage schema (FR-AL-12), audio-token prompt-injection threat model (NC-AL-7), VRAM budget verification (NFR-AL-5 ≤ 8GB on Strix Halo).

Estimated p90 latency win on top of Phase 1: **+150–300ms** (PRD §0 latency budget summary). Stacked with Phase 1 (~100ms): combined **~230–450ms p90 reduction** vs receptionBOX v1 baseline. Difference between "fast" and "feels human."

### Cost shape

Phase 2 is **3–4 months of focused engineering equivalent**, plus GPU budget for adapter training. Three options:

| Option | Description | Pro | Con |
|--------|-------------|-----|-----|
| **(a) Internal headcount** | Existing engineers + new hire | Tightest coupling to receptionBOX, full control | Pulls from receptionBOX/UMB consulting capacity at the moment they're most stretched |
| **(b) External research collaboration** | University lab or small AI research org as partner | Preserves internal bandwidth; brings deeper research bench | Slower coordination; IP questions; harder to time-box |
| **(c) Defer Phase 2 indefinitely** | Ship Phase 1 (predictive-delta ASR) and stop | Caps risk; locks in the smaller but real ~100ms win | Abandons the codec research bet; the per-firm fine-tuning differentiator (Phase 3) becomes unreachable |

### Decision needed by

Target: **end of Phase 0 spike**, ~2 weeks after Phase 0 starts. Phase 0 produces the binary go/no-go signal that should anchor this decision (if Phase 0 fails, this question is moot).

### Kill / pause criteria (PRD §6.2 Phase 2)

If Phase 2 proceeds, the off-ramps are:

- Phase 2 latency reduction over Phase 1 < 100ms p90
- Intent classification regresses by > 2 percentage points
- Any measurable guardrail recall regression on the receptionBOX UPL test suite
- VRAM overhead exceeds the 8GB budget after reasonable optimization

### Honest framing (PRD §14)

This is the most speculative bet in the project. The closest published analog (Moshi) couples codec and LLM tightly in a way the cascade-with-codec-input architecture does not. We may discover during Phase 2 that the decoupling fundamentally doesn't work, and end up either shipping an end-to-end S2S model anyway or abandoning Phase 2. The S2S field is moving fast — the codec-as-input bet may already be obsolete by the time Phase 2 ships.

The board should know this is not a comfortable commitment. The strongest version of this idea may be option (b) — a research collaboration — rather than internal headcount.

---

## Decision Recorded

> *To be filled at the board sync. Replace this section with the verbatim decision (or a faithful summary signed off by attendees).*

**Decision:** _pending_ (one of: green-light / green-light-conditional / defer / no-go)

**Staffing path (if green-lit):** _pending_ (one of: a / b / c)

**Named owner(s):** _pending_

**Conditions (if conditional):** _pending_

**Re-open trigger (if deferred):** _pending_

**Budget envelope:** _pending_

**Attendees:** _pending_

**Date:** _pending_

**Dissent or open questions captured at the meeting:** _pending_

---

## Action Items

- [ ] **Dustin:** Schedule the board sync (Eric, Kevin, any other Heron Labs / UMB Group decision-makers). Target: before end of Phase 0 spike.
- [ ] **Dustin:** Bring this memo + the latency budget summary from PRD §0 to the meeting.
- [ ] **Claude (on sync completion):** Fill "Decision Recorded" section with verbatim outcome. Update Linear DEV-1040 with comment + Done status. Update PRD §13 Open Items to reflect the resolution.
- [ ] **Plan 03 dependency:** PRD v0.2 §10.3 Phase 2 owner field will be populated from this decision (a named owner / external collaboration / "deferred until X").
