---
phase: 01-prd-v0-2-pre-phase-0-resolution
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - docs/decisions/naming-decision.md
  - docs/decisions/partner-corpus-path.md
  - docs/decisions/receptionbox-path-e-reconciliation.md
autonomous: false
requirements:
  - DEV-1037
  - DEV-1038
  - DEV-1042
  - DEV-1043
must_haves:
  truths:
    - "The project has a finalized name (either 'thUMBox Audio Layer' confirmed or one of the §1.4 alternatives selected); the decision is recorded with a rationale."
    - "If the name changed, the rename has been propagated: Linear project name, repo root (this directory's name as referenced in PROJECT.md), and any cross-document references in PRD v0.1."
    - "A named partner law firm is identified for the 90-day call corpus required by Phase 1 (DEV-1042 dependency for Phase 3); the data agreement is either signed or has a tracked path-to-signature with a named owner and target date."
    - "The receptionBOX latency-unconventional addendum's Path E framing is reconciled — either the addendum is updated to acknowledge that 'Path E' has graduated to its own PRD (this Audio Layer PRD), or this PRD is annotated to reference the addendum's framing."
    - "DEV-1037 is closed as the v0.1 PRD baseline reference (informational issue)."
    - "DEV-1038, DEV-1042, DEV-1043 are all marked Done with their decision docs / agreements / addendum updates linked."
  artifacts:
    - path: "docs/decisions/naming-decision.md"
      provides: "Finalized name + rename propagation log"
      contains: "Decision (name kept or changed-to-X), rationale, rename surfaces (Linear project, repo, PRD references), completion checklist"
    - path: "docs/decisions/partner-corpus-path.md"
      provides: "Resolution of the Phase 1 corpus dependency (DEV-1042)"
      contains: "Named partner firm, contact, agreement status (signed / drafted / negotiating), corpus delivery mechanism, target signature date"
    - path: "docs/decisions/receptionbox-path-e-reconciliation.md"
      provides: "Cross-reference fix between this PRD and the receptionBOX latency-unconventional addendum"
      contains: "Reconciliation choice (update addendum / annotate this PRD / both), file path of addendum, exact edit applied or planned"
  key_links:
    - from: "docs/decisions/naming-decision.md"
      to: "Linear DEV-1038"
      via: "Linear issue comment"
      pattern: "decision document linked from DEV-1038"
    - from: "docs/decisions/partner-corpus-path.md"
      to: "Linear DEV-1042"
      via: "Linear issue comment"
      pattern: "decision document linked from DEV-1042"
    - from: "docs/decisions/receptionbox-path-e-reconciliation.md"
      to: "Linear DEV-1043"
      via: "Linear issue comment"
      pattern: "decision document linked from DEV-1043"
    - from: "All three decision docs"
      to: "PRD v0.2 (produced in Plan 03)"
      via: "v0.2 §1.4 (naming), §8.2/§10.2 (corpus dependency), §12.2 (companion documents) updated to reflect these resolutions"
      pattern: "PRD v0.2 incorporates outcomes by section"
---

<objective>
Close the three coordination items that don't require legal counsel or board input: project naming finalization (NC-AL — implicit, PRD §1.4), Phase 1 partner corpus path (PRD §8.2 internal dependency / §13.6), and the receptionBOX addendum Path E framing reconciliation (PRD §13.7).

Purpose: These are independent of Plan 01's external gates but feed the same v0.2 PRD. Running them in parallel with Plan 01 keeps Phase 1 to a single wave of work followed by the consolidation in Plan 03. None of these require legal or board sign-off — they're project hygiene and operational coordination.

Output: Three decision documents in `docs/decisions/`, three (or four including DEV-1037) closed Linear issues, the partner-firm path either signed or on a tracked timeline, and the receptionBOX addendum cross-references reconciled.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@docs/audiolayer-technical-prd-v0_1-2026-05-07.md

Linear MCP tool: mcp__linear-staqs__* (used to update DEV-1037, DEV-1038, DEV-1042, DEV-1043).
</context>

<tasks>

<task type="checkpoint:decision">
  <name>Task 1: Finalize project naming (DEV-1038) + close DEV-1037 as informational</name>
  <files>docs/decisions/naming-decision.md</files>

  <read_first>
    - PRD §1.4 (Naming — provisional name "thUMBox Audio Layer" + alternatives table: codecBOX, NeuroCodec, Project Mimi-Delta, audioLayer)
    - PRD §13 Open Items #1 (Naming flagged for board/partner discussion)
    - PROJECT.md "What This Is" section (current name usage in committed planning)
    - User CLAUDE.md §10 entity context — confirm "thUMBox" capitalization convention (lowercase th, uppercase UMB, lowercase ox) is the existing brand pattern
    - Linear project title (current: "thUMBox Audio Layer", project ID `a281ae7e-5842-4095-a1c9-2b9e6a265404`) — verify via mcp__linear-staqs__list_projects
  </read_first>

  <action>
    1. Claude (autonomous prep): Read the §1.4 alternatives table. Surface a single recommendation to Dustin for sign-off, with one-paragraph rationale. The default recommendation is **keep "thUMBox Audio Layer"**: it follows the platform-infrastructure framing (DR-AL-1), matches the existing capitalization convention, and the PRD §1.4 alternatives all have stronger cons than pros (codecBOX implies a customer-facing pack which contradicts DR-AL-1; NeuroCodec breaks brand connection; Project Mimi-Delta is research-stage only; audioLayer has no precedent). Present the recommendation in the decision doc as "Recommended: keep" plus the alternatives ruled out with a one-line reason each.

    2. Human checkpoint (Dustin): Confirm "keep" or pick an alternative. This is a decision checkpoint — Claude pauses here and resumes on Dustin's call.

    3. Claude (autonomous wrap-up):
       - **If kept:** Record decision in the doc as "Name finalized: thUMBox Audio Layer." Confirm Linear project name and repo directory name already match — no rename actions needed. Note in the doc that no propagation work was required.
       - **If changed to X:** Record decision. Then perform rename propagation:
         - Update Linear project name via mcp__linear-staqs__update_project (project ID `a281ae7e-5842-4095-a1c9-2b9e6a265404`).
         - Note the repo rename as a separate manual step for Dustin (renaming `~/code/thumbox-audio-layer` is outside the GSD tool's reach and has git remote implications — capture as a checklist item for Dustin to execute, do not do it from inside the repo).
         - Update PROJECT.md "What This Is" header.
         - Flag for Plan 03: PRD v0.2 must rename in §1.4 and the document title.
         - Capture all rename surfaces as a checklist in the decision doc with done/pending state.

    4. Claude (autonomous): Mark Linear DEV-1038 status Done with a comment linking to the decision doc. Mark Linear DEV-1037 status Done with a comment noting "Informational issue tracking PRD v0.1 baseline; v0.1 lives at `docs/audiolayer-technical-prd-v0_1-2026-05-07.md`. Phase 1 work in DEV-1044 produces v0.2 as the next deliverable. Closing as the baseline is recorded."

    Why specific: PRD §1.4 leaves naming "decision pending." A vague task ("review naming") could chase rabbits. The recommendation-then-confirm pattern means Claude does the analysis once and Dustin makes a fast yes/no call rather than re-deriving the alternatives.
  </action>

  <verify>
    <automated>test -f docs/decisions/naming-decision.md && grep -qiE 'Decision:\s*(kept|changed)' docs/decisions/naming-decision.md</automated>
    <manual>Confirm via mcp__linear-staqs__get_issue that DEV-1037 and DEV-1038 are both "Done"; if name changed, confirm Linear project name was updated via mcp__linear-staqs__get_project.</manual>
  </verify>

  <acceptance_criteria>
    - File exists at `docs/decisions/naming-decision.md` with sections: Recommendation, Alternatives Ruled Out, Decision (kept / changed-to-X), Rename Propagation Checklist (with done/pending state for each surface).
    - The decision is recorded as definitive, not "to be revisited."
    - Linear DEV-1038 status = Done; comment links to decision doc.
    - Linear DEV-1037 status = Done; comment notes v0.1 PRD as the historical baseline.
    - If the name changed: Linear project name has been updated via Linear MCP, and a `docx-references-to-update` checklist exists for Plan 03 to consume.
  </acceptance_criteria>

  <done>
    Naming is final. Repo, Linear project, and PRD-internal references are either already aligned (kept) or have a tracked propagation checklist (changed). Plan 03 has a definitive name to use in v0.2.
  </done>
</task>

<task type="checkpoint:human-action">
  <name>Task 2: Identify partner firm for Phase 1 90-day call corpus (DEV-1042)</name>
  <files>docs/decisions/partner-corpus-path.md</files>

  <read_first>
    - PRD §8.2 Internal Dependencies — "Firm corpus availability — Phase 1 predictor training requires a 90-day corpus from at least one partner firm. Discovery-phase firm partnerships (receptionBOX addendum) are the dependency path."
    - PRD §10.2 Phase 1 Project Plan — corpus is required to train the predictor
    - PRD §13 Open Items #6 (Predictor corpus — "Phase 1 requires a 90-day call corpus from a partner firm... Is there urgency mismatch?")
    - PRD §1 (consumer is receptionBOX, customer is law firms — the partner is a law firm using receptionBOX's discovery-phase pilot)
    - User CLAUDE.md entity context (Heron Labs, UMB Group, receptionBOX) — confirm receptionBOX has named pilot partners; if not, this task surfaces that gap.
  </read_first>

  <action>
    1. Claude (autonomous prep): Draft a "what we need" one-pager describing the corpus requirement for the partner firm:
       - **Volume:** 90 days of inbound call audio (and any matched text transcripts the firm already has).
       - **Format:** Source audio (PCM WAV or compressed; Mimi will re-encode), call metadata (ANI, time-of-day, duration), any existing text transcripts.
       - **Privacy:** Audio stays under the firm's control; on-appliance training (Phase 3 architecture); for Phase 1 predictor training, transcripts may suffice without raw audio if PII handling is the blocker. Note this as an alternative path in the doc.
       - **Term:** Phase 1 development window (estimated 6-10 weeks active use; long-term retention TBD per the firm's retention policy).
       - **Reciprocity:** What the firm gets — early access to the predictor latency improvement, named pilot status, etc. (Dustin to fill in the commercial side.)

    2. Human action (Dustin): Identify the candidate partner firm. The natural candidates are existing receptionBOX discovery-phase pilots — Dustin to surface the list and pick one (or rank them).

    3. Human action (Dustin): Initiate data agreement. Either:
       - **Path A — agreement signed within Phase 1:** legal review of agreement template, send to firm, sign. Capture the signed agreement (or its tracked location) as Appendix A.
       - **Path B — agreement on a tracked timeline:** if signature won't land before Phase 1 closes, document the named owner, target signature date, and any blockers. The Phase 0 spike (GSD Phase 2) can proceed without the corpus; Phase 1 (GSD Phase 3) cannot. The decision doc must make this gating explicit.
       - **Path C — no firm identified yet:** if no candidate exists, document this as a project-level risk and surface to Plan 03 for v0.2 to acknowledge. The risk is real and should not be papered over — PRD §13.6 already flags it.

    4. Claude (autonomous wrap-up): Record the path chosen (A/B/C), the named firm (if any), the contact, the agreement status, the corpus delivery mechanism (secure drop, on-appliance ingestion, etc.), and any privacy/retention constraints surfaced during negotiation. Update Linear DEV-1042 with status Done if Path A or B is reached, or status In Progress if Path C and surface as a Phase 1 outcome blocker for Plan 03.

    Why specific: PRD §8.2 names the dependency but the path isn't operationalized. The Path A/B/C structure forces an honest answer — Phase 1 (GSD Phase 3) genuinely cannot start without this, so we either have it, have a date for it, or have to acknowledge a real project blocker. No middle ground.
  </action>

  <verify>
    <automated>test -f docs/decisions/partner-corpus-path.md && grep -qiE 'Path Chosen:\s*[ABC]\b' docs/decisions/partner-corpus-path.md</automated>
    <manual>Confirm via mcp__linear-staqs__get_issue that DEV-1042 reflects reality (Done for Path A/B; In Progress with surfaced blocker for Path C).</manual>
  </verify>

  <acceptance_criteria>
    - File exists at `docs/decisions/partner-corpus-path.md` with sections: Corpus Requirement One-Pager, Candidate Partner Firm, Path Chosen (A/B/C), Agreement Status, Corpus Delivery Mechanism, Privacy/Retention Constraints, Appendix A (signed agreement or its tracked location).
    - The "Path Chosen" field is one of A, B, or C — explicit, not "TBD."
    - If Path A: signed agreement (or signed copy reference) is appended.
    - If Path B: named owner + target signature date are recorded.
    - If Path C: a Phase 1 (GSD Phase 3) entry-criterion blocker is flagged and surfaced for Plan 03 to incorporate into v0.2.
    - Linear DEV-1042 status = Done (Path A or B) or In Progress with a tracked blocker (Path C); comment links to decision doc.
  </acceptance_criteria>

  <done>
    Phase 1 (GSD Phase 3) entry-criterion has a definitive path forward, even if that path is "blocked, here's the owner and date." DEV-1042 reflects reality.
  </done>
</task>

<task type="auto">
  <name>Task 3: Reconcile receptionBOX latency-unconventional addendum Path E framing (DEV-1043)</name>
  <files>docs/decisions/receptionbox-path-e-reconciliation.md</files>

  <read_first>
    - PRD §12.2 Companion Documents — "addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md ... contains Path A (forked speculative) and Path B (exemplar cache) which compose with Audio Layer; this PRD slots in as effectively 'Path E' in that addendum's framing"
    - PRD §13 Open Items #7 (the explicit reconciliation question — should the addendum be updated, or this PRD annotated, or both?)
    - The receptionBOX addendum file itself: search for it by filename pattern `addendum-receptionbox-latency-unconventional-*.md`. Likely lives in the receptionBOX repo or a sibling docs location, not in this repo. If not findable from this repo, surface that as a finding in the decision doc (the reconciliation may require cross-repo coordination).
  </read_first>

  <action>
    1. Claude (autonomous): Locate the receptionBOX latency-unconventional addendum. Use Bash `find ~/code -name 'addendum-receptionbox-latency-unconventional*' -type f 2>/dev/null` to locate it across the broader code tree. If found, read its current Path A through Path D (or whatever paths it enumerates) and confirm whether "Path E" is a name the addendum explicitly uses or a forward-looking placeholder PRD §12.2 chose.

    2. Claude (autonomous): Choose a reconciliation strategy from these options and record the rationale:
       - **Strategy 1 — Update addendum.** Add a "Path E" entry to the receptionBOX addendum that points to this PRD as a graduated platform-layer project, with a sentence explaining why it's no longer a path inside receptionBOX but an external dependency. Best when the addendum is actively maintained and readers come from receptionBOX-side.
       - **Strategy 2 — Annotate this PRD.** In v0.2 §12.2, expand the existing reference into a fuller "Relationship to receptionBOX latency addendum" subsection. Cheaper, no cross-repo edit required. Best when the addendum is mostly historical.
       - **Strategy 3 — Both.** A short pointer in the addendum and a fuller annotation here. Best when both documents are actively read by different audiences (engineering vs. board/strategy).

    3. Claude (autonomous): Apply the strategy:
       - If Strategy 1 or 3: locate the addendum, draft the Path E entry, capture exact insertion text in the decision doc. If the addendum is in a sibling repo (User CLAUDE.md §4 — "Outside repo: ask first"), do NOT edit directly. Instead capture the proposed edit as a patch in the decision doc and surface to Dustin as a manual cross-repo step.
       - If Strategy 2 or 3: capture the v0.2 §12.2 expansion text as a "Plan 03 input" block in the decision doc — Plan 03 reads this and applies it to v0.2.

    4. Claude (autonomous): Update Linear DEV-1043 with status Done; comment links to decision doc and notes which strategy was chosen.

    Why specific: PRD §13.7 asks the reconciliation question but doesn't pick. The strategy 1/2/3 framing forces an explicit choice. The cross-repo edit caveat (don't write to a sibling repo without asking) respects the User CLAUDE.md file-and-repo behavior rule.
  </action>

  <verify>
    <automated>test -f docs/decisions/receptionbox-path-e-reconciliation.md && grep -qiE 'Reconciliation Strategy:\s*[123]\b' docs/decisions/receptionbox-path-e-reconciliation.md</automated>
    <manual>Confirm via mcp__linear-staqs__get_issue that DEV-1043 status is "Done" with decision doc linked.</manual>
  </verify>

  <acceptance_criteria>
    - File exists at `docs/decisions/receptionbox-path-e-reconciliation.md` with sections: Addendum Location (path or "not found from this repo"), Reconciliation Strategy (1/2/3), Rationale, Edits Applied (or proposed if cross-repo), Plan 03 Input (text v0.2 §12.2 should incorporate).
    - The strategy is one of 1, 2, 3 — explicit.
    - If Strategy 1 or 3 and addendum is in this repo: the addendum file is updated with the Path E entry.
    - If Strategy 1 or 3 and addendum is cross-repo: the proposed edit is captured as a patch in the decision doc, with a note for Dustin to apply manually in the addendum's home repo.
    - If Strategy 2 or 3: the v0.2 §12.2 expansion text exists in the decision doc as a clearly-labeled "Plan 03 input" block.
    - Linear DEV-1043 status = Done; comment links to decision doc.
  </acceptance_criteria>

  <done>
    The Path E framing is reconciled. Plan 03 has explicit text to insert into v0.2 §12.2. Any cross-repo edits are captured as patches for Dustin to apply, not silently written to other repos.
  </done>
</task>

</tasks>

<verification_criteria>
- All three decision documents exist at the paths declared in `files_modified`.
- Each decision document has a definitive choice/path (no "TBD", no "to be revisited").
- Linear issues DEV-1037, DEV-1038, DEV-1042, DEV-1043 have status reflecting the work:
  - DEV-1037 = Done (informational closure)
  - DEV-1038 = Done
  - DEV-1042 = Done (Path A/B) or In Progress (Path C, with surfaced blocker)
  - DEV-1043 = Done
- Each closed Linear issue has a comment linking to its corresponding decision doc.
- If naming changed: Linear project name updated, repo rename surfaced as Dustin checklist item.
- If receptionBOX addendum was edited cross-repo: edit was captured as a patch, NOT silently applied.
</verification_criteria>

<success_criteria>
The three coordination items are closed. Plan 03 has explicit inputs from each: (a) the final name to use throughout v0.2, (b) the corpus path status to reflect in v0.2 §8.2 / §13, (c) the §12.2 expansion text for the Path E reconciliation.
</success_criteria>

<output>
After completion, create `.planning/phases/01-prd-v0-2-pre-phase-0-resolution/01-02-SUMMARY.md` with:
- Naming decision (kept / changed-to-X) and rename propagation status
- Partner corpus path (A/B/C) with named firm and agreement state
- Path E reconciliation strategy (1/2/3) and where edits landed
- Inputs for Plan 03 v0.2 production: explicit text blocks v0.2 should incorporate
- Confirmation of four closed (or one in-progress) Linear issues
</output>
