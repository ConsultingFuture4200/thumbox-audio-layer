# Partner Firm — 90-Day Call Corpus Path

**Status:** PATH-A (agreement landed)
**Linear:** [DEV-1042](https://linear.app/staqs/issue/DEV-1042)
**Resolves:** PRD §8.2 Internal Dependencies; gates Phase 1 (Predictive-Delta ASR / GSD Phase 3 = Linear M2).
**Created:** 2026-05-07
**Author:** Dustin (Claude prep)

---

## Corpus Requirement (one-pager for partner firm)

### What we need

A **90-day rolling window** of inbound call data from a single partner firm running receptionBOX. The corpus trains the Phase 1 predictor model (Qwen3-0.5B fine-tune) so it can predict caller utterances from call context (ANI, time-of-day, conversation history).

### Volume and format

| Artifact | Required | Notes |
|----------|----------|-------|
| Source audio | Preferred | PCM WAV at any common rate (we re-encode); compressed acceptable. Ideally 90 days inbound. |
| Text transcripts | Required | Whatever the firm already has from receptionBOX or any ASR pipeline. Phase 1 can train on transcripts alone if raw audio is the privacy blocker. |
| Call metadata | Required | ANI (caller number), time-of-day, call duration. Used as predictor features. |
| Existing call outcome labels (intent, disposition) | Optional | If the firm has them, they accelerate predictor training. Not required. |

### Privacy posture

- **Audio stays under firm control.** Phase 3 (per-firm fine-tuning) is the architecture endgame, but Phase 1 needs source data once, not continuously. Two paths the firm can choose between:
  - (a) Audio + transcripts shared with Heron Labs / UMB Group under a data-sharing agreement, used only for predictor training, deleted after Phase 1 ships.
  - (b) Transcripts only — sufficient for predictor training. Removes the strongest privacy concern; audio never leaves the firm.
- **No audio retention beyond Phase 1.** Whatever is shared is destroyed after the predictor model lands and Phase 1 ships to production.
- **PII handling.** ANI is the most sensitive metadata; we can hash phone numbers if the firm prefers (slight predictor accuracy cost; testable).

### Term

- **Phase 1 development window:** 6–10 weeks of active corpus use during predictor training.
- **Long-term retention:** None on Heron Labs / UMB Group side. Long-term firm-side retention follows the firm's existing receptionBOX retention policy.

### Reciprocity (Dustin to fill in)

What the firm gets in exchange:

- **Early access** to the predictor latency improvement when Phase 1 ships (~100ms p90 reduction on high-confidence calls; ~40% of calls).
- **Named pilot status** if they want it (or anonymous, their choice).
- _[Dustin to add commercial terms if applicable: discount, extended pilot, co-marketing, etc.]_

---

## Partner Firm

**Firm name:** [partner firm under signed agreement — details in Heron Labs CRM, not captured in this repo]

**Primary contact:** [in Heron Labs CRM]

**Existing receptionBOX status:** Discovery-phase partner with signed data-sharing agreement landing in Phase 1 calendar window.

**Why details aren't captured here:** Per Dustin (2026-05-07), partner identity and contact stay in Heron Labs CRM rather than the public Audio Layer repo. The data-sharing agreement and corpus delivery mechanism are tracked operationally; this doc records only that Path A landed and the corpus is on-track for Phase 1 (M2 / GSD Phase 3) consumption.

---

## Path Chosen

**Path:** **A** — agreement signed within Phase 1 calendar window. Corpus is available for Phase 1 (GSD Phase 3 / Linear M2) predictor training when that phase begins.

### Path A — Agreement signed within Phase 1

If counsel review of agreement template, send to firm, and signature land within Phase 1's calendar window. The signed agreement (or its tracked location) is appended as Appendix A.

### Path B — Agreement on a tracked timeline

If signature won't land before Phase 1 (M0) closes, document the named owner, target signature date, and any blockers. The Phase 0 spike (GSD Phase 2 / Linear M1) can proceed without the corpus; **Phase 1 (GSD Phase 3 / Linear M2) cannot start without it**. Make this gating explicit.

### Path C — No firm identified yet

If no candidate exists, document this as a project-level risk. PRD §13.6 already flags it. The risk is real and should not be papered over: **Phase 1 (GSD Phase 3 / Linear M2) is blocked until a partner is identified**. Surface this to Plan 03 for v0.2 to acknowledge.

---

## Agreement Status

**Path A:** signed data-sharing agreement landed 2026-05-07 (per Dustin). Agreement and operational details tracked in Heron Labs CRM; Audio Layer repo records the landing event and the corpus availability for Phase 1.

Effective date: agreement covers Phase 1 development window (estimated 6-10 weeks active corpus use during predictor training).

---

## Corpus Delivery Mechanism

**Transport, storage, encryption, and destruction trigger:** Operational details tracked in Heron Labs CRM and the signed agreement (not captured in this repo). Phase 1 (GSD Phase 3 / Linear M2) execution work will reference the agreement for the operational specifics when the predictor training pipeline is built (DEV-1053).

Destruction trigger (per Path A framing): corpus destroyed after Phase 1 evaluation document committed and predictor model in production.

---

## Privacy / Retention Constraints

Specific firm-side constraints (PII handling, audit-log, sub-processor disclosures) tracked in the signed agreement and Heron Labs CRM. Phase 1 execution work (DEV-1053 predictor training pipeline) must read the agreement before training starts to ensure compliance.

---

## Action Items

- [x] Dustin identified partner firm and landed signed data-sharing agreement (Path A) 2026-05-07.
- [x] Linear DEV-1042 closed (Delivered) with link to this doc.
- [ ] **Plan 03 input:** PRD v0.2 §8.2 Internal Dependencies updated — partner corpus is available for Phase 1; firm details in Heron Labs CRM.
- [ ] **Plan 03 input:** PRD v0.2 §13 Open Items #6 (Predictor corpus) marked resolved.
- [ ] **DEV-1053 (Phase 1 predictor training pipeline) prerequisite:** Read the signed agreement before training starts to confirm corpus access and constraints.

---

## Appendix A — Signed Agreement

Agreement and supporting documents stored operationally in Heron Labs CRM. Not committed to this repo for partner-confidentiality reasons. Audio Layer engineering work that needs the agreement (DEV-1053) will read it through the operational channel when Phase 1 starts.
