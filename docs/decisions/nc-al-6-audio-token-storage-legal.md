# NC-AL-6 — Legal Position on Storing Audio Tokens Alongside Transcripts

**Status:** PENDING-LEGAL-REVIEW
**Linear:** [DEV-1041](https://linear.app/staqs/issue/DEV-1041)
**Resolves:** PRD §7 NC-AL-6; gates FR-AL-12 (PRD §4.2) for Phase 2 ship.
**Created:** 2026-05-07
**Author:** Dustin (Claude prep)

---

## Context for Counsel

The thUMBox Audio Layer (PRD `docs/audiolayer-technical-prd-v0_1-2026-05-07.md` §3.3, §4.2, §4.4, §12.1) introduces a Phase 2 architectural decision that adds **a parallel persisted artifact** to receptionBOX's existing call record:

- Today: receptionBOX persists call audio + ASR text transcripts under a published retention policy (receptionBOX PRD §8 Security & Data Architecture).
- Phase 2 (FR-AL-12): "Transcripts persisted to Postgres shall include both text (from ASR) and audio token sequences (from codec) for audit completeness."

The Mimi codec is reversible by design: its tokens decode back to audible audio. This is the design intent (PRD §1.2 "compression mismatch" framing). Storing tokens alongside text is the architectural choice that preserves the "you own the data" pillar (PRD §4.4) while capturing the latency benefit of LLM-on-tokens.

**Customer base context:** receptionBOX customers are **law firms**. Discovery is a frequent operational concern. State call-recording laws (one-party / two-party consent) attach to the source audio; the legal status of audio tokens is undetermined.

---

## Four-Question Intake to Legal Counsel

### Q1 — Classification of audio tokens

Are Mimi audio tokens, in the abstract, considered:

- (a) a recording of the underlying audio (legally equivalent to the source audio)?
- (b) a derivative or transformation of the recording (a separate artifact with its own classification)?
- (c) a non-audio data artifact (more like a hash or compressed representation, distinct from a recording)?

The legal status of recording-call audio (consent, retention, breach disclosure, two-party-consent state laws) attaches differently in each case. A definitive classification anchors the rest of the answer.

### Q2 — Reconstruction risk

Mimi tokens decode back to audible audio. This is its design (it's a neural audio codec, intended for reconstruction; PRD §1.2). The reconstruction is lossy but recognizable.

Does the ability to decode tokens back to audio make storage of the tokens **equivalent to storing the original recording** for legal purposes (consent, retention, breach disclosure)? Or does the lossy compression / non-trivial decode step create legal distance?

A specific sub-question: if a breach exposed only the tokens (not the original audio), would breach-disclosure obligations attach as if the audio itself were exposed?

### Q3 — Retention and deletion

receptionBOX retains text transcripts under a published retention policy (receptionBOX PRD §8). If audio tokens are stored alongside (FR-AL-12):

- (a) Should the retention policy treat tokens **identically to transcripts**?
- (b) **Identically to source audio**?
- (c) As a **third class** with its own retention rules?

Sub-question on deletion: when a customer requests deletion of a call record, must the tokens also be deleted under the same trigger? Are there any technical-deletion-versus-legal-deletion distinctions counsel wants to flag (e.g., crypto-shredding vs. row-level delete vs. audit-log preservation)?

### Q4 — Disclosure and discovery

Customer base is law firms. Legal discovery scenarios are frequent operational concerns for them.

- (a) Are audio tokens discoverable as a separate artifact from text transcripts in litigation? Or are they considered the same artifact?
- (b) Does dual-storage (text + tokens for the same call) **create new disclosure exposure** vs. text-only storage today? In particular: would a discovery request producing transcripts also require producing tokens?
- (c) Any opinion on whether the firm-side data-handling policy should explicitly address audio-token discovery, or is that a downstream concern?

---

## Implied Controls (to be confirmed by counsel)

> *Counsel may add or modify these. Listed here as the engineering-side starting expectations.*

- **Encryption at rest.** Tokens stored under the same encryption-at-rest scope as source audio + transcripts. No separate key handling.
- **Access control.** Token access scoped to the same RBAC roles that gate transcript access; no broader access surface.
- **Retention.** Tokens retained on the same schedule as transcripts unless counsel directs otherwise.
- **Deletion triggers.** Tokens deleted on the same triggers as transcripts (customer request, retention expiration, persona change if relevant).
- **Audit log.** Token reads and writes logged identically to transcript reads and writes.

---

## Legal's Written Position

> *To be inserted after counsel review. Replace this section with counsel's verbatim response (or a faithful summary with counsel's review noted) before changing the Status field.*

Q1 — Classification: _pending_

Q2 — Reconstruction risk: _pending_

Q3 — Retention and deletion: _pending_

Q4 — Disclosure and discovery: _pending_

Implied controls confirmed / modified: _pending_

---

## FR-AL-12 Ship-Gate Verdict

**Status:** pending

To be set to one of:

- **clear** — counsel confirms tokens can be stored alongside transcripts under the same regime; FR-AL-12 proceeds as PRD §4.2 specifies.
- **clear-with-conditions** — storage permitted but counsel imposes specific controls beyond what's listed in "Implied Controls" above. Document the conditions; they become Phase 2 design constraints.
- **blocked** — storing tokens creates unacceptable legal exposure. Document the blocker. Plan 03 must reflect this in PRD v0.2 as either a scope reduction (do not persist tokens; tokens used in-memory only) or a new NC-AL with a Phase 2 ship-gate.

---

## Action Items

- [ ] **Dustin:** Route this document to legal counsel. Same counsel as NC-AL-9 if practical.
- [ ] **Dustin:** Surface receptionBOX PRD §8 (security architecture) to counsel as supporting context — the existing transcript-storage regime is the baseline they'd be augmenting.
- [ ] **Claude (on counsel response):** Insert verbatim response into "Legal's Written Position." Set FR-AL-12 ship-gate verdict. Update Linear DEV-1041 with comment + Done status.
- [ ] **Claude (on response, if blocked):** File follow-up Linear issue against the new constraint and surface to Plan 03 as a v0.2 scope change.
