# Partner Firm — 90-Day Call Corpus Path

**Status:** PENDING-FIRM-IDENTIFICATION
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

## Candidate Partner Firm

> *To be filled when Dustin identifies the firm.*

**Firm name:** _pending_

**Primary contact:** _pending_

**Why this firm:** _pending_ (volume, willingness, fit with discovery-phase pilot framing)

**Existing receptionBOX status:** _pending_ (active pilot / signed but not started / interested but pre-pilot)

---

## Path Chosen

**Path:** _pending_ (one of A / B / C)

### Path A — Agreement signed within Phase 1

If counsel review of agreement template, send to firm, and signature land within Phase 1's calendar window. The signed agreement (or its tracked location) is appended as Appendix A.

### Path B — Agreement on a tracked timeline

If signature won't land before Phase 1 (M0) closes, document the named owner, target signature date, and any blockers. The Phase 0 spike (GSD Phase 2 / Linear M1) can proceed without the corpus; **Phase 1 (GSD Phase 3 / Linear M2) cannot start without it**. Make this gating explicit.

### Path C — No firm identified yet

If no candidate exists, document this as a project-level risk. PRD §13.6 already flags it. The risk is real and should not be papered over: **Phase 1 (GSD Phase 3 / Linear M2) is blocked until a partner is identified**. Surface this to Plan 03 for v0.2 to acknowledge.

---

## Agreement Status

> *Filled per the chosen path.*

- **Path A:** signed agreement attached as Appendix A; legal review noted; effective date recorded.
- **Path B:** named owner = _pending_; target signature date = _pending_; current blocker = _pending_.
- **Path C:** Phase 1 blocker is open; surfaced to Plan 03; risk note added to v0.2 §8.2 / §13.

---

## Corpus Delivery Mechanism

> *Filled when path + agreement land.*

- **Transport:** _pending_ (e.g., one-time secure cloud drop, on-appliance ingestion at the firm site, etc.)
- **Storage at Heron Labs / UMB Group side:** _pending_ (path, encryption-at-rest scope, access control)
- **Destruction trigger:** _pending_ (e.g., "after Phase 1 evaluation document committed and predictor model in production")

---

## Privacy / Retention Constraints

> *Filled when agreement is negotiated. Capture any specific firm-side asks: PII handling, audit-log requirements, sub-processor disclosures, etc.*

_pending_

---

## Action Items

- [ ] **Dustin:** Survey active receptionBOX discovery-phase partners (per PRD §8.2 — discovery-phase firm partnerships are the dependency path). Identify candidate firm by volume + willingness.
- [ ] **Dustin:** Choose between corpus-A (audio + transcripts) and corpus-B (transcripts only) framings when initiating partner conversation. Either is acceptable for Phase 1; B is easier to negotiate.
- [ ] **Dustin:** Engage legal on data-sharing agreement template (counsel may overlap with NC-AL-9 / NC-AL-6 review).
- [ ] **Claude (when path chosen):** Update Linear DEV-1042 — Done if Path A or B (with named owner + date for B); In Progress with surfaced blocker if Path C. Update this doc's Path Chosen field.
- [ ] **Plan 03 dependency:** PRD v0.2 §8.2 will reflect the corpus path status; if Path C, also flagged in §13 Open Items as a Phase 1 entry blocker.

---

## Appendix A — Signed Agreement

> *To be appended on Path A.* If transcripts-only path was negotiated, include the signed agreement here verbatim (or a stable internal link).
