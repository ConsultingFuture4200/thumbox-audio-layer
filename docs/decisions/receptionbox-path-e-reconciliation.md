# receptionBOX Latency-Unconventional Addendum — "Path E" Reconciliation

**Status:** RESOLVED
**Linear:** [DEV-1043](https://linear.app/staqs/issue/DEV-1043)
**Resolves:** PRD §13 Open Item #7
**Created:** 2026-05-07
**Author:** Claude (autonomous)

---

## Finding: The Addendum Does Not Currently Exist

The PRD §12.2 Companion Documents references `addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md` as containing "Path A (forked speculative) and Path B (exemplar cache) which compose with Audio Layer; this PRD slots in as effectively 'Path E' in that addendum's framing."

A search across the local filesystem found:

```bash
find /home/bob/code /home/bob/RBOX /home/bob/Documents /home/bob/vault /home/bob/Downloads -name 'addendum-receptionbox-latency-unconventional*' 2>/dev/null
# (no results)
```

Files present in `/home/bob/RBOX/docs/`:

- `addendum-hardware-pivot-strix-halo-v0_1-2026-04-23.md`
- `addendum-receptionbox-discovery-v0_1-2026-04-22.md`
- `addendum-receptionbox-discovery-v0_2-2026-04-22.md`

The latency-unconventional addendum is referenced by PRD §12.2 as if it exists, but no copy is locatable from this environment. **The "Path E" framing is forward-looking** — the addendum is either (a) drafted but not yet committed, (b) pending creation, or (c) a planning fiction the PRD anticipated. Either way, the reconciliation question changes shape.

---

## Reconciliation Strategy

**Strategy: 2 — Annotate this PRD.**

Rationale:

- We cannot edit a document that does not exist.
- Strategy 1 (update the addendum) would require either creating the addendum or editing it cross-repo when it surfaces. Both are out of scope for Phase 1 of the Audio Layer.
- Strategy 2 (annotate v0.2 §12.2) is the correct minimum-friction action: expand the existing companion-document reference to acknowledge the framing relationship even when the addendum is absent or future.
- Strategy 3 (both) collapses to Strategy 2 until the addendum is locatable.

When the addendum eventually surfaces, a follow-up issue can be filed to add a "Path E" pointer back into it. That's not a Phase 1 deliverable.

---

## Plan 03 Input — v0.2 §12.2 Expansion Text

> The following text is to be inserted into PRD v0.2 §12.2 Companion Documents, replacing the current `addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md` line. Plan 03 (PRD v0.2 promotion) should pick this up verbatim.

**Replace:**

```
| `addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md` | Contains Path A (forked speculative) and Path B (exemplar cache) which compose with Audio Layer; this PRD slots in as effectively "Path E" in that addendum's framing |
```

**With:**

```
| `addendum-receptionbox-latency-unconventional` (forthcoming or external) | Anticipated to enumerate latency paths A–D for receptionBOX. The thUMBox Audio Layer is the **graduated platform-layer realization** of what the addendum's framing would label "Path E" — the codec-as-LLM-input bet. Because Audio Layer is a platform capability rather than a path internal to receptionBOX, the long-term documentation home is this PRD; the addendum (when authored or located) should reference Audio Layer as an external dependency rather than restating its scope. As of v0.2, the addendum is not locatable from the Audio Layer working tree; cross-reference will be added when the addendum surfaces. See `docs/decisions/receptionbox-path-e-reconciliation.md` for the audit trail. |
```

---

## Optional Follow-up (NOT a Phase 1 deliverable)

If the addendum is later located or authored, file a follow-up Linear issue to:

1. Add a "Path E" entry in the addendum pointing to this PRD.
2. Note in the addendum that Path E has graduated out of receptionBOX into a platform-layer project.

This is a low-priority cross-repo edit; do not let it block Phase 1 closure.

---

## Edits Applied

- **This document committed** to `docs/decisions/receptionbox-path-e-reconciliation.md` (Phase 1 deliverable).
- **No cross-repo edits** were made — the addendum target file does not exist (User CLAUDE.md §4: "Outside repo: ask first" rule respected).
- **PRD v0.2 §12.2 expansion** is staged here for Plan 03 to apply at v0.2 promotion.

---

## Action Items

- [x] Locate addendum (result: not found locally; framing is forward-looking).
- [x] Choose strategy (Strategy 2: annotate this PRD).
- [x] Capture v0.2 §12.2 expansion text for Plan 03.
- [ ] **Claude:** Update Linear DEV-1043 — Done; comment links to this decision doc and notes Strategy 2 chosen because the addendum target is not locatable.
- [ ] **Plan 03:** Apply the §12.2 expansion text in PRD v0.2.
- [ ] **Optional / future:** If addendum surfaces, file a follow-up Linear issue for the cross-repo edit.
