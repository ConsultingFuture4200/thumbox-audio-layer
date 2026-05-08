---
phase: 01-prd-v0-2-pre-phase-0-resolution
plan: 03
type: execute
wave: 2
depends_on:
  - 01
  - 02
files_modified:
  - docs/audiolayer-technical-prd-v0_2-2026-05-07.md
  - .planning/PROJECT.md
  - .planning/REQUIREMENTS.md
  - .planning/STATE.md
autonomous: true
requirements:
  - DEV-1044
must_haves:
  truths:
    - "PRD v0.2 exists as a new file at `docs/audiolayer-technical-prd-v0_2-<date>.md` (date = day v0.2 is committed). The v0.1 file remains untouched as the historical baseline."
    - "v0.2 incorporates the resolved status of every PRD §13 review item (the seven open items): naming finalized, three-phase scope confirmed or revised, hardware tier confirmed, bandwidth/board decision recorded, Mimi licensing position recorded, predictor corpus path stated, Path E framing reconciled."
    - "v0.2 §7 (Open Questions) has been updated: NC-AL-9, NC-AL-12, NC-AL-6 removed (now resolved with cross-references to decision docs); the remaining NC-AL items (NC-AL-1 through NC-AL-5, NC-AL-7, NC-AL-8, NC-AL-10, NC-AL-11) updated only if Plans 01/02 surfaced changes."
    - "v0.2 §11 (Decision Records) reflects the resolved status of DR-AL-3 (adopted / adopted-with-conditions / rejected) — no longer a candidate."
    - "v0.2 §1.4 reflects the final name decision."
    - "v0.2 §12.2 reflects the receptionBOX Path E reconciliation."
    - "v0.2 changelog at the top of the document explicitly lists every change from v0.1, with cross-references to the decision documents in `docs/decisions/`."
    - "If any Plan 01 or Plan 02 outcome materially changed scope (Mimi license rejected → contingency, board no-go → Phase 2/3 deferred, FR-AL-12 blocked → schema scope reduced), v0.2 reflects the scope change honestly rather than papering over it."
    - ".planning/PROJECT.md, .planning/REQUIREMENTS.md, and .planning/STATE.md are updated to reference v0.2 instead of v0.1."
    - "Linear DEV-1044 status is Done with the v0.2 PRD file linked."
    - "The Linear project (`a281ae7e-5842-4095-a1c9-2b9e6a265404`) state moves out of Backlog into In Progress (or whatever the equivalent next state is in the workspace), reflecting that scope is now committed."
  artifacts:
    - path: "docs/audiolayer-technical-prd-v0_2-2026-05-07.md"
      provides: "PRD v0.2 — committed scope rather than strawman"
      contains: "All §1 through §14 sections, with v0.2 changelog, resolved §13 items, updated §7 / §11 / §1.4 / §12.2"
    - path: ".planning/PROJECT.md"
      provides: "Updated planning context referencing v0.2"
      contains: "Source PRD line points to v0.2"
    - path: ".planning/REQUIREMENTS.md"
      provides: "Updated open-questions section reflecting NC-AL-9/12/6 closure"
      contains: "NC-AL table with resolved items removed or marked resolved with decision-doc cross-references"
    - path: ".planning/STATE.md"
      provides: "Phase 1 marked complete; Phase 2 (M1 Mimi Feasibility Spike) unblocked"
      contains: "Phase 1 row shows Complete; Recent Decisions appended; Next Action updated"
  key_links:
    - from: "docs/audiolayer-technical-prd-v0_2-2026-05-07.md (changelog, §7, §11)"
      to: "docs/decisions/dr-al-3-mimi-licensing.md"
      via: "explicit cross-reference"
      pattern: "v0.2 cites the decision file by relative path"
    - from: "docs/audiolayer-technical-prd-v0_2-2026-05-07.md (§1.4)"
      to: "docs/decisions/naming-decision.md"
      via: "explicit cross-reference"
      pattern: "v0.2 cites the decision file by relative path"
    - from: "docs/audiolayer-technical-prd-v0_2-2026-05-07.md (§7, §11)"
      to: "docs/decisions/nc-al-12-board-appetite-phase-2.md and nc-al-6-audio-token-storage-legal.md"
      via: "explicit cross-reference"
      pattern: "v0.2 cites both decision files by relative path"
    - from: "docs/audiolayer-technical-prd-v0_2-2026-05-07.md (§8.2, §13.6)"
      to: "docs/decisions/partner-corpus-path.md"
      via: "explicit cross-reference"
      pattern: "v0.2 cites the decision file by relative path"
    - from: "docs/audiolayer-technical-prd-v0_2-2026-05-07.md (§12.2)"
      to: "docs/decisions/receptionbox-path-e-reconciliation.md"
      via: "explicit cross-reference"
      pattern: "v0.2 cites the decision file by relative path"
    - from: "Linear DEV-1044"
      to: "v0.2 PRD file"
      via: "Linear issue comment with file path"
      pattern: "DEV-1044 closed with v0.2 link"
---

<objective>
Promote the PRD from v0.1 (strawman) to v0.2 (committed scope) by rolling all six resolved open items from Plans 01 and 02 into a single new versioned PRD file. The v0.1 file remains as the historical record per User CLAUDE.md §6 ("save a new file — don't overwrite").

Purpose: This is the terminal task for Phase 1 (M0). Plans 01 and 02 produced six decision documents. Plan 03 consolidates those decisions into the canonical product document, updates the GSD planning files to reference v0.2, closes the final Linear issue, and unblocks Phase 2 (Mimi Feasibility Spike, M1).

Output: New file `docs/audiolayer-technical-prd-v0_2-2026-05-07.md` (or the date of commit), updated PROJECT.md/REQUIREMENTS.md/STATE.md, closed DEV-1044, Linear project state advanced.
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
@docs/decisions/dr-al-3-mimi-licensing.md
@docs/decisions/nc-al-12-board-appetite-phase-2.md
@docs/decisions/nc-al-6-audio-token-storage-legal.md
@docs/decisions/naming-decision.md
@docs/decisions/partner-corpus-path.md
@docs/decisions/receptionbox-path-e-reconciliation.md
@.planning/phases/01-prd-v0-2-pre-phase-0-resolution/01-01-SUMMARY.md
@.planning/phases/01-prd-v0-2-pre-phase-0-resolution/01-02-SUMMARY.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Generate PRD v0.2 from v0.1 + six decision documents</name>
  <files>docs/audiolayer-technical-prd-v0_2-2026-05-07.md</files>

  <read_first>
    - The full v0.1 PRD: `docs/audiolayer-technical-prd-v0_1-2026-05-07.md`
    - All six decision documents from Plans 01 and 02 (paths in `<context>` above)
    - Both Plan SUMMARY files (01-01-SUMMARY.md, 01-02-SUMMARY.md) — they distill the outcomes
    - User CLAUDE.md §6 — "Filenames include versions... When I ask for a revision, bump the version and save a new file — don't overwrite." Confirms v0.1 stays put; v0.2 is a NEW file.
  </read_first>

  <action>
    1. Determine v0.2 filename. Pattern: `docs/audiolayer-technical-prd-v0_2-<YYYY-MM-DD>.md` where the date is today's date (the day v0.2 is committed). Do NOT reuse v0.1's date. The v0.1 file (`audiolayer-technical-prd-v0_1-2026-05-07.md`) is preserved untouched as the historical baseline.

    2. Copy v0.1 in full as the starting point for v0.2 (read v0.1, write to the new v0.2 path). Then apply the targeted edits below. Do not rewrite the entire document — preserve the prose, structure, and hard-won language of v0.1; v0.2 is a delta release.

    3. Update the front-matter block at the top:
       - Change `## v0.1` to `## v0.2`.
       - Update Status from "Draft — strawman for review and pressure-testing" to "Committed scope — pre-Phase-0. Performance numbers remain exploratory pending Phase 0 spike."
       - Update Provisional codename in front-matter to whatever Plan 02 Task 1 finalized (read `docs/decisions/naming-decision.md`).
       - **Append a new changelog entry** under v0.2:
         ```
         > - v0.2 — Promotes v0.1 from strawman to committed scope after Phase 1 (M0) coordination work. Resolves §13 open items 1, 4, 5, 6, 7. Promotes DR-AL-3 from candidate to <status from decision doc>. Removes NC-AL-6, NC-AL-9, NC-AL-12 from the open-questions table (resolved with decision documents in docs/decisions/). Other §13 items and remaining NC-ALs surfaced for Phase 0 / Phase 2 work.
         ```

    4. Edit §1.4 (Naming):
       - Read `docs/decisions/naming-decision.md` for the final decision.
       - If the name was kept: replace "Decision pending. Naming finalized at v0.2 review." with "**Decision adopted at v0.2:** thUMBox Audio Layer. Rationale: <one-sentence summary from the decision doc>. See `docs/decisions/naming-decision.md`."
       - If the name was changed: rewrite §1.4 to lead with the new name, retain the alternatives table for historical context but mark the chosen option, and reference the decision doc. Also update the document title (`# thUMBox Audio Layer — Technical PRD` → new name) and every other in-document occurrence of the old name.

    5. Edit §3.5 / §11.2 (DR-AL-3 status):
       - Read `docs/decisions/dr-al-3-mimi-licensing.md` for the final disposition.
       - Update DR-AL-3 in §3.5 from "Status: Candidate" to "Status: Adopted" (or "Adopted with conditions" or "Rejected").
       - In §11.2 (Candidate DRs), if DR-AL-3 was adopted: move it to §11.1 (Adopted DRs). If rejected: keep in §11.2 marked as "Rejected — see NC-AL-10 contingency."
       - Add a one-line cross-reference to the decision doc.

    6. Edit §4.2 FR-AL-12 (Audio token persistence):
       - Read `docs/decisions/nc-al-6-audio-token-storage-legal.md` for the ship-gate verdict.
       - **If clear:** add a footnote/sentence under FR-AL-12 noting "Legal position recorded; see `docs/decisions/nc-al-6-audio-token-storage-legal.md`. Implied controls: <retention/encryption/access constraints from the decision doc>."
       - **If clear-with-conditions:** add the conditions inline as part of the requirement and link to the decision doc.
       - **If blocked:** rewrite FR-AL-12 to acknowledge the blocker honestly. Either narrow the requirement (e.g., "transcripts persisted shall include text only; audio token persistence deferred to v3+ pending resolution of NC-AL-6") or surface FR-AL-12 as suspended with a Phase 2 ship-gate requirement to revisit. Update the Phase 2 deliverables in §10.3 accordingly. Do NOT silently leave FR-AL-12 as-is if legal blocked it.

    7. Edit §7 (Open Questions):
       - Remove rows for NC-AL-6, NC-AL-9, NC-AL-12 from the table (they're resolved).
       - Add a new subsection §7.1 "Resolved in v0.2" that lists the three resolved items with one-line summaries and decision-doc cross-references. This preserves traceability without cluttering the live open-questions table.
       - Re-check NC-AL-10 (codec contingency): if NC-AL-9 was rejected, NC-AL-10 becomes urgent — note this inline.

    8. Edit §8.2 (Internal Dependencies — Firm corpus availability):
       - Read `docs/decisions/partner-corpus-path.md` for the path chosen (A/B/C).
       - **If Path A (signed):** update §8.2 to "Firm corpus availability — signed agreement with <firm name>; see `docs/decisions/partner-corpus-path.md`."
       - **If Path B (tracked timeline):** update §8.2 to name the partner, note "agreement on tracked timeline (target: <date>; owner: <name>)" and link the decision doc.
       - **If Path C (no firm yet):** keep the dependency in §8.2 but flag it as an active blocker. Update §13.6 (Predictor corpus open item) to mark as "Open — see `docs/decisions/partner-corpus-path.md`. Phase 1 (predictive-delta ASR) entry-criterion is unmet until this resolves."

    9. Edit §12.2 (Companion Documents — receptionBOX addendum):
       - Read `docs/decisions/receptionbox-path-e-reconciliation.md` for the strategy chosen and the exact text proposed for §12.2.
       - Insert the proposed text as a new subsection or expanded entry. The decision doc carries the verbatim insertion text.

    10. Edit §10.3 / §13.4 (Bandwidth / board appetite for Phase 2):
        - Read `docs/decisions/nc-al-12-board-appetite-phase-2.md` for the decision.
        - **If green-light:** update §10.3 Phase 2 owner from "TBD — likely requires external research collaboration or new hire" to the named owner(s) and staffing plan. Update §13.4 to mark as resolved with cross-reference.
        - **If green-light-conditional:** update §10.3 to note the conditions (e.g., "conditional on Phase 1 SM-AL-3 ≥ 100ms in production"). Update §13.4 with the same.
        - **If defer or no-go:** rewrite §10.3 to reflect deferral. Move §10.4 Phase 3 to "deferred pending Phase 2 reactivation." Add a top-level note in §2 that Phase 2/3 are paused. This is a significant scope change — make it loud, not buried.

    11. Edit §13 (Open Items for Review):
        - For items 1, 4, 5, 6, 7: append "→ Resolved in v0.2; see <decision doc path>."
        - Items 2 (Scope — three-phase decomposition), 3 (Hardware tier T3-only) are not addressed by Plans 01/02 — leave as open if they were never raised; if Plan 02 SUMMARY surfaced anything, incorporate.
        - If everything in §13 is now resolved or defensibly deferred, change the section heading or add a closing note.

    12. Final pass:
        - Search v0.2 for any remaining "Decision pending", "TBD" strings, or "candidate" status that should now be definitive — if found, audit against the six decision docs.
        - Add an "END OF PRD v0.2" line replacing the v0.1 closing note.
        - Save the file. Do NOT modify v0.1.

    Why specific: The v0.1 PRD is 561 lines of carefully-written prose. v0.2 is a targeted edit, not a rewrite. The step-by-step section-by-section edit list ensures every Phase 1 outcome lands in the right place and nothing in v0.1 is silently lost or contradicted.
  </action>

  <verify>
    <automated>ls docs/audiolayer-technical-prd-v0_2-*.md >/dev/null 2>&1 && test -f docs/audiolayer-technical-prd-v0_1-2026-05-07.md && git diff HEAD -- docs/audiolayer-technical-prd-v0_1-2026-05-07.md | wc -l | grep -qE '^\s*0\s*$'</automated>
    <manual>Open v0.2 and confirm: §1.4 reflects naming decision, DR-AL-3 promoted out of candidate in §3.5/§11, §7 no longer lists NC-AL-6/9/12 in live table, §4.2 FR-AL-12 reflects legal verdict, §8.2 reflects corpus path, §12.2 reflects Path E reconciliation, §10.3 reflects board decision.</manual>
  </verify>

  <acceptance_criteria>
    - File exists at `docs/audiolayer-technical-prd-v0_2-<date>.md` (new file, NOT overwriting v0.1).
    - File at `docs/audiolayer-technical-prd-v0_1-2026-05-07.md` is unchanged (`git diff` shows no modifications to v0.1).
    - v0.2 has a `## v0.2` heading and a v0.2 changelog entry.
    - v0.2 §1.4 reflects the final naming decision (no "Decision pending" text remains).
    - v0.2 DR-AL-3 (in §3.5 and §11) is no longer "candidate" — it's adopted, adopted-with-conditions, or rejected.
    - v0.2 §7 no longer lists NC-AL-6, NC-AL-9, NC-AL-12 in the live open-questions table; resolved subsection §7.1 references decision docs.
    - v0.2 §4.2 FR-AL-12, §8.2, §10.3, §12.2, §13 all reflect the corresponding decision-doc outcomes.
    - Every reference to a decision doc uses a relative path that resolves from the repo root.
    - `grep -nE 'Decision pending|TBD|candidate' docs/audiolayer-technical-prd-v0_2-*.md` returns only intentional uses (e.g., remaining NC-AL items still legitimately open) — no stragglers from the v0.1 strawman language.
  </acceptance_criteria>

  <done>
    PRD v0.2 exists, v0.1 preserved, every Plan 01/02 decision is reflected in the right section with cross-references. Document is internally consistent and ready for use as the committed-scope source of truth.
  </done>
</task>

<task type="auto">
  <name>Task 2: Update GSD planning files (PROJECT.md, REQUIREMENTS.md, STATE.md) + close DEV-1044 + advance Linear project state</name>
  <files>.planning/PROJECT.md, .planning/REQUIREMENTS.md, .planning/STATE.md</files>

  <read_first>
    - Current `.planning/PROJECT.md` (specifically the "Source PRD" line in the Context section; check both PROJECT.md and the doctored CLAUDE.md generated from it)
    - Current `.planning/REQUIREMENTS.md` (the NC-AL open questions table at the bottom — needs NC-AL-6/9/12 marked resolved)
    - Current `.planning/STATE.md` (Phase Progress table, Recent Decisions, Next Action)
    - The new v0.2 PRD file produced in Task 1 (for the path to reference)
  </read_first>

  <action>
    1. Update `.planning/PROJECT.md`:
       - In the "Context" section, change the line `Source PRD: docs/audiolayer-technical-prd-v0_1-2026-05-07.md (drafted 2026-05-07, strawman, expecting v0.2)` to `Source PRD: docs/audiolayer-technical-prd-v0_2-<date>.md (committed scope; v0.1 preserved at audiolayer-technical-prd-v0_1-2026-05-07.md as historical baseline)`.
       - If the naming decision changed the project name, update the heading and the "What This Is" section.

    2. Update `.planning/REQUIREMENTS.md`:
       - In the "Open Questions (NC-AL-N)" table, mark NC-AL-6, NC-AL-9, NC-AL-12 as resolved. Either remove rows entirely or change the "Linear" column to indicate Done and add a new column / footnote with the decision doc path. Keep rows for unresolved NC-ALs unchanged.
       - Above the table, add a one-line note: "NC-AL-6, NC-AL-9, NC-AL-12 resolved in Phase 1 (M0); see PRD v0.2 §7.1 and `docs/decisions/`."

    3. Update `.planning/STATE.md`:
       - Phase Progress table: change Phase 1 row from `⏳ Not started` to `✅ Complete (v0.2 committed)`.
       - Phase 2 row: change `⏳ Blocked on Phase 1` to `🟢 Ready to plan` (or whatever the project's status convention is — match the existing emoji/text pattern in the table).
       - Recent Decisions: append `- 2026-05-07 PRD promoted from v0.1 (strawman) to v0.2 (committed scope). DR-AL-3 status: <final>. NC-AL-6, NC-AL-9, NC-AL-12 resolved. Naming: <kept/changed-to-X>. Partner corpus: <Path A/B/C>.` Use today's actual date.
       - Next Action: update from `/gsd-plan-phase 1` to `/gsd-plan-phase 2 — Phase 0 Mimi Feasibility Spike. M0 closed.`
       - Update the bottom-of-file `*Last updated:*` line to today's date.

    4. Close Linear DEV-1044 via mcp__linear-staqs__update_issue:
       - Status: Done.
       - Comment: "PRD v0.2 committed at `docs/audiolayer-technical-prd-v0_2-<date>.md`. Resolves §13 review items 1, 4, 5, 6, 7. v0.1 preserved as historical baseline. M0 milestone closed; Phase 0 (M1 Mimi Feasibility Spike) unblocked."

    5. Advance the Linear project state via mcp__linear-staqs__update_project (project ID `a281ae7e-5842-4095-a1c9-2b9e6a265404`):
       - First, query the project to see its current state and the available state transitions in this Linear workspace (mcp__linear-staqs__get_project).
       - Move from Backlog (or current state) into "In Progress" or the equivalent next state. If the workspace uses non-standard project states, choose the closest semantic match — log the chosen state in the SUMMARY.

    Why specific: GSD planning files are downstream consumers of the PRD. They need to point at the new v0.2 file. The Linear project state advancement is the "out of strawman" signal the project lead and other stakeholders watch for. Doing all three updates in one task keeps the v0.2 commit logically atomic.
  </action>

  <verify>
    <automated>grep -q 'audiolayer-technical-prd-v0_2' .planning/PROJECT.md && grep -q '✅ Complete' .planning/STATE.md</automated>
    <manual>Confirm via mcp__linear-staqs__get_issue that DEV-1044 is Done with v0.2 path in comment; via mcp__linear-staqs__get_project that the project state has advanced beyond Backlog.</manual>
  </verify>

  <acceptance_criteria>
    - `.planning/PROJECT.md` Source PRD line points to v0.2 (verifiable via grep for `audiolayer-technical-prd-v0_2`).
    - `.planning/REQUIREMENTS.md` open-questions table reflects NC-AL-6/9/12 resolved.
    - `.planning/STATE.md` Phase Progress shows Phase 1 complete and Phase 2 ready; Recent Decisions has a v0.2 entry; Next Action points to Phase 2.
    - Linear DEV-1044 status = Done with a comment containing the v0.2 PRD path.
    - Linear project state has advanced beyond Backlog (verifiable via mcp__linear-staqs__get_project; the SUMMARY records the from→to transition).
  </acceptance_criteria>

  <done>
    GSD planning surface is in sync with v0.2. Linear reflects Phase 1 complete and the project as committed scope. Phase 2 (Mimi Feasibility Spike) is unblocked and ready for `/gsd-plan-phase 2`.
  </done>
</task>

</tasks>

<verification_criteria>
- v0.2 PRD file exists at `docs/audiolayer-technical-prd-v0_2-<date>.md`.
- v0.1 PRD file is byte-identical to its pre-Phase-1 state (`git diff HEAD~ docs/audiolayer-technical-prd-v0_1-2026-05-07.md` is empty for that file specifically — only v0.2 should appear in the diff).
- v0.2 cross-references all six decision documents via relative paths.
- v0.2 has no remaining "candidate" / "Decision pending" strings except where a remaining NC-AL is legitimately still open.
- All six decision documents from Plans 01 and 02 exist and are non-empty (the dependency is real, not nominal).
- `.planning/PROJECT.md` references v0.2.
- `.planning/REQUIREMENTS.md` reflects NC-AL closures.
- `.planning/STATE.md` shows Phase 1 complete.
- Linear DEV-1044 status = Done.
- Linear project state advanced out of Backlog.
- All eight Phase 1 Linear issues (DEV-1037 through DEV-1044) are status = Done (or DEV-1042 = In Progress with documented blocker if Path C was chosen in Plan 02 Task 2).
</verification_criteria>

<success_criteria>
- Phase 1 (M0) closed.
- PRD v0.2 is the committed scope of record.
- DR-AL-3 promoted out of candidate status.
- All NC-AL items intended for closure in M0 are closed; remaining NC-ALs are appropriately flagged for Phase 0 / Phase 2.
- Phase 2 (M1 — Mimi Feasibility Spike) entry-criteria satisfied; project ready for `/gsd-plan-phase 2`.
</success_criteria>

<output>
After completion, create `.planning/phases/01-prd-v0-2-pre-phase-0-resolution/01-03-SUMMARY.md` with:
- v0.2 PRD path and a one-paragraph summary of changes from v0.1
- Final disposition of every §13 open item (1-7)
- DR-AL-3 final status
- NC-AL closures and any new flags for Phase 0 / Phase 2
- Naming outcome
- Partner corpus path final state
- Linear: list of all 8 Phase 1 issues with final status
- Linear project state transition (from → to)
- Confirmation Phase 2 is unblocked; recommended next command (`/gsd-plan-phase 2`)
</output>
