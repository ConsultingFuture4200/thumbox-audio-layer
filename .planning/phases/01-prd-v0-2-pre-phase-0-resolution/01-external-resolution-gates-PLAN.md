---
phase: 01-prd-v0-2-pre-phase-0-resolution
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - docs/decisions/dr-al-3-mimi-licensing.md
  - docs/decisions/nc-al-12-board-appetite-phase-2.md
  - docs/decisions/nc-al-6-audio-token-storage-legal.md
autonomous: false
requirements:
  - DEV-1039
  - DEV-1040
  - DEV-1041
must_haves:
  truths:
    - "A written legal position on Mimi/Kyutai commercial licensing exists and resolves NC-AL-9 with one of: clear-to-use, clear-to-use-with-attribution, restricted-do-not-use."
    - "DR-AL-3 status has been moved out of 'candidate' (either to 'adopted' or to 'rejected with NC-AL-10 contingency triggered') in a committed decision document."
    - "A documented decision on board/team appetite for the Phase 2 research-grade commitment exists, including either (a) green-light with named staffing plan or (b) defer/no-go with rationale."
    - "A written legal position on storing Mimi audio tokens alongside text transcripts (FR-AL-12) exists, identifying any data-handling, retention, or disclosure constraints."
    - "All three corresponding Linear issues (DEV-1039, DEV-1040, DEV-1041) are marked Done with the decision documents linked from each issue."
  artifacts:
    - path: "docs/decisions/dr-al-3-mimi-licensing.md"
      provides: "Resolution of NC-AL-9; promotion or rejection of DR-AL-3"
      contains: "License source URL, three-question intake to legal, legal's written position, DR-AL-3 status"
    - path: "docs/decisions/nc-al-12-board-appetite-phase-2.md"
      provides: "Resolution of NC-AL-12 board appetite question"
      contains: "Decision (green-light / defer / no-go), staffing plan if green-lit, named owners, rationale"
    - path: "docs/decisions/nc-al-6-audio-token-storage-legal.md"
      provides: "Resolution of NC-AL-6 audio token persistence legal position"
      contains: "FR-AL-12 storage scope, retention questions, legal's written position, ship-gate verdict"
  key_links:
    - from: "docs/decisions/dr-al-3-mimi-licensing.md"
      to: "Linear DEV-1039"
      via: "Linear issue comment with file link"
      pattern: "decision document attached or linked from DEV-1039"
    - from: "docs/decisions/nc-al-12-board-appetite-phase-2.md"
      to: "Linear DEV-1040"
      via: "Linear issue comment with file link"
      pattern: "decision document attached or linked from DEV-1040"
    - from: "docs/decisions/nc-al-6-audio-token-storage-legal.md"
      to: "Linear DEV-1041"
      via: "Linear issue comment with file link"
      pattern: "decision document attached or linked from DEV-1041"
    - from: "All three decision docs"
      to: "PRD v0.2 (produced in Plan 03)"
      via: "Each decision doc referenced by section in v0.2"
      pattern: "v0.2 §7 (NC-AL table) and §11 (DRs) cite these files"
---

<objective>
Close the three external-resolution gates that block Phase 2 (and therefore PRD v0.2): Mimi licensing review (NC-AL-9), board/team appetite for the Phase 2 commitment (NC-AL-12), and legal position on storing audio tokens alongside transcripts (NC-AL-6).

Purpose: Each of these requires input from outside the engineering loop (legal counsel, board/leadership). All three have the same shape — pull prior art, formulate specific questions, route to the relevant external party, capture the written response in a decision document, close the Linear issue. They run in parallel because they have no inter-dependencies.

Output: Three decision documents in `docs/decisions/`, three closed Linear issues. These feed Plan 03 (PRD v0.2 promotion) which depends on all three landing.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@docs/audiolayer-technical-prd-v0_1-2026-05-07.md

Linear MCP tool: mcp__linear-staqs__* (use to update DEV-1039, DEV-1040, DEV-1041 status and to attach decision docs).
</context>

<tasks>

<task type="checkpoint:human-action">
  <name>Task 1: NC-AL-9 — Mimi (Kyutai) commercial licensing review (DEV-1039)</name>
  <files>docs/decisions/dr-al-3-mimi-licensing.md</files>

  <read_first>
    - PRD §1 (project context — appliance distribution model)
    - PRD §7 NC-AL-9 (the open question as stated)
    - PRD §8.1 (Mimi external dependency, "open weights as of 2026-Q1; commercial licensing terms require legal review")
    - PRD §11.2 DR-AL-3 (candidate status, "gated on Phase 0 prototype + NC-AL-9 license review")
    - PRD §9.1 risks table — "Mimi license restricts commercial use" / "NC-AL-10 contingency plan with alternative codec"
    - Mimi license text from Kyutai source. Pull from: https://huggingface.co/kyutai/mimi (LICENSE file) and the Kyutai GitHub repo (https://github.com/kyutai-labs/moshi). Capture license name, version, and full text in the decision doc as Appendix A.
  </read_first>

  <action>
    1. Claude (autonomous prep): Fetch the Mimi license text from Hugging Face (`huggingface.co/kyutai/mimi`) and from the Kyutai GitHub repo. Save full text as Appendix A in the decision document. Identify license type (e.g., CC-BY, Apache 2.0, custom Kyutai license) and any non-standard clauses.

    2. Claude (autonomous prep): Draft a three-question intake memo for legal counsel. The three questions are non-negotiable and must be answered explicitly:
       - **Q1 — Commercial appliance distribution.** Does the license permit distributing Mimi weights and/or compiled inference artifacts as part of a commercial single-tenant appliance product (thUMBox), where the end customer is a law firm and pays a recurring license fee for the appliance?
       - **Q2 — Attribution and notice requirements.** What attribution, notice, source-availability, or copyleft obligations does the license impose on the appliance product, its documentation, and its end-customer-facing materials?
       - **Q3 — Derivative works (per-firm fine-tuning).** Phase 3 of this project trains a firm-specific codec head on the firm's call corpus on-appliance. Are these fine-tuned weights considered a derivative work, and what license obligations attach to those derivatives (especially given the audio corpus never leaves the firm)?

    3. Human action (Dustin): Route the intake memo + Appendix A license text to legal counsel. Capture written response.

    4. Claude (autonomous wrap-up after response received): Insert legal's written position into the decision document. Then move DR-AL-3 status to one of:
       - **adopted** — if license clearly permits commercial appliance distribution; promote DR-AL-3 from "candidate" to "adopted" with a citation to legal's response.
       - **adopted-with-conditions** — if permitted with attribution / notice obligations; document the obligations as a Phase 2 ship-gate checklist.
       - **rejected** — if license restricts commercial use; mark DR-AL-3 rejected and trigger NC-AL-10 contingency planning (note: that contingency is a Phase 2 scoping concern, not a Phase 1 deliverable — flag it in the decision doc, do NOT execute the contingency in this phase).

    5. Claude (autonomous wrap-up): Update Linear DEV-1039 — comment with link to `docs/decisions/dr-al-3-mimi-licensing.md`, mark status Done. Use mcp__linear-staqs__update_issue.

    Why specific: The PRD §7 question is broad ("licensing implications"). The three-question intake is narrow enough to get a yes/no/conditional answer from counsel without endless back-and-forth, and maps directly to the Phase 2 ship gate, the marketing/compliance work, and the Phase 3 architecture choice.
  </action>

  <verify>
    <automated>test -f docs/decisions/dr-al-3-mimi-licensing.md && grep -qiE 'Status:\s*(adopted|adopted-with-conditions|rejected)' docs/decisions/dr-al-3-mimi-licensing.md</automated>
    <manual>Confirm via mcp__linear-staqs__get_issue that DEV-1039 status is "Done" and has a comment referencing docs/decisions/dr-al-3-mimi-licensing.md.</manual>
  </verify>

  <acceptance_criteria>
    - File exists at `docs/decisions/dr-al-3-mimi-licensing.md` with sections: License Source, Three-Question Intake, Legal's Written Position, DR-AL-3 Status (adopted / adopted-with-conditions / rejected), Appendix A (full license text).
    - DR-AL-3 status in the decision doc is one of: adopted, adopted-with-conditions, rejected. Not "candidate" or "pending."
    - If status = rejected, the doc names NC-AL-10 (contingency codec) as a follow-up Phase 2 concern with a Linear issue reference (existing or to be filed).
    - Linear DEV-1039 status is "Done" (verifiable via mcp__linear-staqs__get_issue).
    - Linear DEV-1039 has a comment containing the relative path `docs/decisions/dr-al-3-mimi-licensing.md`.
  </acceptance_criteria>

  <done>
    NC-AL-9 has a written, defensible position. DR-AL-3 is no longer a candidate. Phase 2 either has a clear license path or has a flagged contingency. DEV-1039 is closed with the decision doc attached.
  </done>
</task>

<task type="checkpoint:human-action">
  <name>Task 2: NC-AL-12 — Board / team appetite for Phase 2 commitment (DEV-1040)</name>
  <files>docs/decisions/nc-al-12-board-appetite-phase-2.md</files>

  <read_first>
    - PRD §7 NC-AL-12 (the open question as stated — Eric/Kevin appetite given UMB Group bandwidth)
    - PRD §9.2 project risks — "Phase 2 is research-grade and team bandwidth is constrained"
    - PRD §10.3 (Phase 2 plan, 13-26 week window, "Owner: TBD — likely requires external research collaboration or new hire")
    - PRD §13 Open Items #4 (Bandwidth) and #5 (Mimi licensing) — they cluster
    - PRD §14 Honest Uncertainty #4 (bandwidth real) and #5 (research collaboration may be the strongest version)
    - PROJECT.md Honest Uncertainty section (mirrors PRD §14)
  </read_first>

  <action>
    1. Claude (autonomous prep): Draft a one-page board sync memo. Required sections:
       - **Ask** — single sentence: "Does Heron Labs / UMB Group leadership commit to staffing Phase 2 (3-4 months, research-grade) of the thUMBox Audio Layer, conditional on Phase 0 spike + Phase 1 production results?"
       - **Phase 2 scope summary** — three bullets pulled from PRD §2.3 and §3.3.
       - **Cost shape** — Phase 2 is 3-4 months engineering-equivalent. Three options to choose between:
         - (a) Internal headcount (existing engineers + new hire). Trade-off: pulls from receptionBOX/UMB consulting capacity.
         - (b) External research collaboration (university lab, small AI research org). Trade-off: slower coordination, IP questions, but preserves internal bandwidth.
         - (c) Defer Phase 2 indefinitely after Phase 1 ships. Trade-off: caps the project at the Phase 1 latency win; abandons the codec research bet.
       - **Decision needed by** — date that aligns with Phase 0 spike completion (target: end of Phase 0, ~2 weeks after Phase 0 starts).
       - **Kill / pause criteria** — copy from PRD §6.2 Phase 2 kill criteria so the board sees the off-ramps.

    2. Human action (Dustin): Schedule + run the board sync (Eric, Kevin, and any other Heron Labs / UMB Group decision-makers). Capture the decision verbatim.

    3. Claude (autonomous wrap-up after sync): Record in the decision document:
       - Decision: green-light / green-light-conditional / defer / no-go.
       - If green-light: named owner(s) for Phase 2, staffing path (option a/b/c above), and budget envelope if discussed.
       - If green-light-conditional: the conditions (e.g., "conditional on Phase 1 SM-AL-3 ≥ 100ms in production").
       - If defer or no-go: the trigger that would re-open the question, if any.
       - Attendees, date, and any dissent or open questions.

    4. Claude (autonomous wrap-up): Update Linear DEV-1040 — comment with link to decision doc, mark status Done.

    Why specific: PRD §7 NC-AL-12 is "appetite" — too soft to act on. The decision doc forces a concrete output: green-light vs defer, named owner if green-lit, named trigger if deferred. PRD §13.4 explicitly flags this as a board-level question, so the staffing plan must come from the board not from engineering.
  </action>

  <verify>
    <automated>test -f docs/decisions/nc-al-12-board-appetite-phase-2.md && grep -qiE 'Decision:\s*(green-light|green-light-conditional|defer|no-go)' docs/decisions/nc-al-12-board-appetite-phase-2.md</automated>
    <manual>Confirm via mcp__linear-staqs__get_issue that DEV-1040 status is "Done" with decision doc linked.</manual>
  </verify>

  <acceptance_criteria>
    - File exists at `docs/decisions/nc-al-12-board-appetite-phase-2.md` with sections: Board Sync Memo (the one-pager), Decision Recorded, Staffing Plan (if green-lit), Conditions (if conditional), Re-open Trigger (if deferred), Attendees + Date.
    - Decision field is one of: green-light, green-light-conditional, defer, no-go. Not "TBD" or "pending."
    - If green-light: at least one named owner appears. If deferred: at least one named re-open trigger appears.
    - Linear DEV-1040 status is "Done."
    - Linear DEV-1040 has a comment linking to the decision doc.
  </acceptance_criteria>

  <done>
    NC-AL-12 has a recorded board-level decision. The Phase 4 (M3) milestone in ROADMAP either has a clear path forward or a clear pause condition. DEV-1040 is closed.
  </done>
</task>

<task type="checkpoint:human-action">
  <name>Task 3: NC-AL-6 — Legal position on storing audio tokens alongside transcripts (DEV-1041)</name>
  <files>docs/decisions/nc-al-6-audio-token-storage-legal.md</files>

  <read_first>
    - PRD §7 NC-AL-6 (the open question as stated — legal-counsel position on storing audio tokens alongside text transcripts as part of the call record)
    - PRD §4.2 FR-AL-12 ("Transcripts persisted to Postgres shall include both text (from ASR) and audio token sequences (from codec) for audit completeness")
    - PRD §3.3 (Phase 2 architecture diagram showing parallel ASR + codec paths and the auditability rationale for keeping ASR)
    - PRD §4.4 (Guardrail and Observability — the "you own the data" pillar specifically)
    - PRD §12.1 inheritance from parent thUMBox PRD §8 Security & Data Architecture ("audio token persistence adds new schema (FR-AL-12)")
    - receptionBOX PRD §8 (security architecture) — Dustin to surface the receptionBOX file path; if not at hand, note "receptionBOX PRD security section" and ask Dustin to attach the relevant excerpt to the decision doc before legal review.
  </read_first>

  <action>
    1. Claude (autonomous prep): Draft a four-question intake memo for legal counsel:
       - **Q1 — Classification of audio tokens.** Are Mimi audio tokens, in the abstract, considered (a) a recording of the underlying audio, (b) a derivative or transformation of the recording, or (c) a non-audio data artifact? The legal status of recording-call audio (consent, retention, two-party-consent state laws, etc.) attaches differently in each case.
       - **Q2 — Reconstruction risk.** Mimi is an audio codec — its tokens can decode back to audible audio (this is its design). Does the ability to decode the tokens back to audio make storage of the tokens equivalent to storing the original recording, for legal purposes (consent, retention, breach disclosure)?
       - **Q3 — Retention and deletion.** receptionBOX retains text transcripts under a published retention policy. If audio tokens are stored alongside (FR-AL-12), should the retention policy treat tokens identically to transcripts, identically to source audio, or as a third class?
       - **Q4 — Disclosure and discovery.** In legal discovery scenarios (the customer is a law firm — discovery is a frequent operational concern), are audio tokens discoverable as a separate artifact from text transcripts? Does dual-storage create new disclosure exposure?

    2. Human action (Dustin): Route the intake memo to legal counsel (same counsel as NC-AL-9 if practical — both are appliance/data-handling questions). Capture the written response.

    3. Claude (autonomous wrap-up): Record in the decision document:
       - Legal's classification of audio tokens (Q1).
       - Reconstruction-risk position (Q2).
       - Retention policy verdict for FR-AL-12 (Q3) — this becomes a Phase 2 design constraint.
       - Discovery exposure verdict (Q4).
       - **Ship-gate verdict for FR-AL-12:** clear / clear-with-conditions / blocked. If blocked, document the blocker and flag it for the v0.2 PRD as a scope reduction or new NC-AL.
       - Any data-handling controls implied (encryption-at-rest scope, key handling, access control).

    4. Claude (autonomous wrap-up): Update Linear DEV-1041 — comment with link to decision doc, mark status Done.

    Why specific: PRD §7 NC-AL-6 is the "legal position on storing audio tokens." For a law-firm customer base, the four questions above are exactly what a careful counsel will ask first. Asking them in the intake means counsel returns a usable position, not a request for clarification.
  </action>

  <verify>
    <automated>test -f docs/decisions/nc-al-6-audio-token-storage-legal.md && grep -qiE 'Ship-Gate Verdict:\s*(clear|clear-with-conditions|blocked)' docs/decisions/nc-al-6-audio-token-storage-legal.md</automated>
    <manual>Confirm via mcp__linear-staqs__get_issue that DEV-1041 status is "Done" with decision doc linked.</manual>
  </verify>

  <acceptance_criteria>
    - File exists at `docs/decisions/nc-al-6-audio-token-storage-legal.md` with sections: Four-Question Intake, Legal's Written Position, FR-AL-12 Ship-Gate Verdict (clear / clear-with-conditions / blocked), Implied Controls (retention, encryption, access).
    - FR-AL-12 ship-gate verdict is one of: clear, clear-with-conditions, blocked. Not "TBD."
    - If blocked: a follow-up Linear issue is filed (or a flag is recorded in the decision doc for Plan 03 to incorporate into v0.2 as a new NC-AL or scope reduction).
    - Linear DEV-1041 status is "Done."
    - Linear DEV-1041 has a comment linking to the decision doc.
  </acceptance_criteria>

  <done>
    NC-AL-6 has a written legal position. FR-AL-12 (audio token persistence) either has a clear path or a documented blocker. Phase 2 design knows the data-handling constraints. DEV-1041 is closed.
  </done>
</task>

</tasks>

<verification_criteria>
- All three decision documents exist at the paths declared in `files_modified`.
- Each decision document has a definitive status field (no "TBD", "candidate", "pending").
- All three Linear issues (DEV-1039, DEV-1040, DEV-1041) have status = Done.
- Each Linear issue has a comment linking to its corresponding decision doc.
- DR-AL-3 in the project's decision record set has been promoted out of "candidate" status (either to adopted, adopted-with-conditions, or rejected).
- If any task ended with a blocking outcome (Mimi license rejected, board no-go, FR-AL-12 blocked), Plan 03 (PRD v0.2) MUST reflect that change in scope.
</verification_criteria>

<success_criteria>
The three external gates are closed. Plan 03 (PRD v0.2 promotion) can now run with concrete inputs for §7 NC-AL table updates, §11 DR-AL-3 promotion, and §4.2 FR-AL-12 status.
</success_criteria>

<output>
After completion, create `.planning/phases/01-prd-v0-2-pre-phase-0-resolution/01-01-SUMMARY.md` with:
- Final disposition of NC-AL-9, NC-AL-12, NC-AL-6 (one paragraph each)
- DR-AL-3 final status
- Any new NC-AL or scope changes surfaced (input to Plan 03)
- Links to the three decision documents
- Confirmation of three closed Linear issues
</output>
