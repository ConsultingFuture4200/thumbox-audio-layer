# Project Naming Decision

**Status:** KEPT
**Linear:** [DEV-1038](https://linear.app/staqs/issue/DEV-1038), [DEV-1037](https://linear.app/staqs/issue/DEV-1037) (informational)
**Resolves:** PRD §1.4, §13 Open Item #1
**Created:** 2026-05-07
**Author:** Claude (recommendation)

---

## Recommendation

**Keep "thUMBox Audio Layer" as the final name.**

Rationale:

- **Aligns with DR-AL-1** (Audio Layer is platform infrastructure, not a customer-facing pack). The name signals exactly that.
- **Follows the existing capitalization convention** (lowercase `th`, uppercase `UMB`, lowercase `ox`) used across thUMBox materials.
- **The PRD §1.4 alternatives all have stronger cons than pros** (see below).
- **Already in use** — Linear project name, GitHub repo, GSD planning artifacts, PRD title. A rename creates propagation cost without a meaningful benefit.

---

## Alternatives Ruled Out (one-line each)

| Name | Status | Reason |
|------|--------|--------|
| **thUMBox Audio Layer** | **Recommended (keep)** | Signals platform infrastructure; matches existing naming convention; already in use. |
| codecBOX | Ruled out | Implies a customer-facing pack — directly contradicts DR-AL-1 (this is *not* a pack). |
| NeuroCodec | Ruled out | No brand connection to thUMBox; would orphan the layer from the platform context. |
| Project Mimi-Delta | Ruled out | Signals research-stage only; doesn't translate to v1+ shipping; couples name to a specific codec choice (DR-AL-3 is candidate, not adopted). |
| audioLayer | Ruled out | No precedent for lowercase-camel platform-layer naming in thUMBox; capitalization breaks brand pattern. |

---

## Decision

**Decision:** **kept** — "thUMBox Audio Layer" finalized as the name.

**Confirmed by:** Dustin

**Date:** 2026-05-07

**Propagation required:** None. Linear project name, GitHub repo, GSD planning artifacts, and PRD title already use the kept name.

---

## Rename Propagation Checklist

> *Only required if decision = changed.* If decision = kept, this checklist is N/A and the doc closes here.

If the name changes to **X**, all of the following must be updated:

- [ ] Linear project name (currently "thUMBox Audio Layer", project ID `a281ae7e-5842-4095-a1c9-2b9e6a265404`) — via `mcp__linear-staqs__save_project`
- [ ] GitHub repo name (currently `https://github.com/ConsultingFuture4200/thumbox-audio-layer`) — manual rename via `gh repo rename`; updates remote URL but local clone needs `git remote set-url`
- [ ] Local repo directory (currently `~/code/thumbox-audio-layer`) — manual rename outside the repo; rotate any tooling that references the path
- [ ] `.planning/PROJECT.md` "What This Is" header
- [ ] `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` references
- [ ] PRD `docs/audiolayer-technical-prd-v0_1-2026-05-07.md` title, §1.4, and any internal references — flagged for Plan 03 to handle in v0.2 (not v0.1)
- [ ] README.md (already uses the name in title and content)
- [ ] CLAUDE.md project section
- [ ] Linear issue descriptions — any free-text references to "thUMBox Audio Layer" (low priority; can be left as historical)

---

## Action Items

- [ ] **Dustin:** Confirm "keep thUMBox Audio Layer" or pick an alternative. This is the one decision in Phase 1 that requires *your* input rather than counsel's or the board's.
- [ ] **Claude (on confirmation = keep):**
  - Update Decision section to "kept"
  - Update Linear DEV-1038 with comment "Name confirmed as thUMBox Audio Layer; no rename required" + Done
  - Update Linear DEV-1037 with comment "Informational issue tracking PRD v0.1 baseline; v0.1 lives at `docs/audiolayer-technical-prd-v0_1-2026-05-07.md`. Phase 1 work in DEV-1044 produces v0.2 as the next deliverable. Closing as the baseline is recorded." + Done
- [ ] **Claude (on confirmation = changed):**
  - Update Decision section with new name and rationale
  - Walk the propagation checklist
  - Surface PRD §1.4 rename text as Plan 03 input for v0.2
  - Update Linear DEV-1038 + DEV-1037
