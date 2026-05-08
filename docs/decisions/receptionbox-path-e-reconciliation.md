# receptionBOX Latency-Unconventional Addendum — "Path E" Reconciliation

**Status:** RESOLVED (Strategy 2 applied; cross-repo Strategy 1 patch staged for Dustin)
**Linear:** [DEV-1043](https://linear.app/staqs/issue/DEV-1043) (Delivered)
**Resolves:** PRD §13 Open Item #7
**Created:** 2026-05-07
**Updated:** 2026-05-07 — addendum located in `/home/bob/RBOX/docs/`; staged cross-repo patch
**Author:** Claude (autonomous)

---

## Addendum Location

`/home/bob/RBOX/docs/addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md` (309 lines).

The addendum is in the **receptionBOX repo**, not the thUMBox Audio Layer repo. Per User CLAUDE.md §4 ("Outside repo: ask first"), the addendum is **not** edited automatically from this repo — instead, the proposed insertion is staged below as a patch for Dustin to apply manually in the RBOX repo.

---

## Addendum Structure (read on 2026-05-07)

The addendum's §4 enumerates **three paths**: Path A (forked speculative S2S drafting), Path B (exemplar-cache-as-default), Path C (watershed routing at SIP edge). There is no Path D or Path E in the document. The PRD §12.2's "Path E" framing is therefore a **forward-looking name for a graduated platform-layer concept**, not a reference to an existing entry.

This means the reconciliation can be **either Strategy 1, 2, or 3** — all are now feasible. We chose Strategy 2 + 1 (annotate this PRD AND stage a cross-repo patch) because:

- The Audio Layer needed v0.2 §12.2 expansion regardless (Strategy 2).
- Adding a Path E pointer in the addendum is cheap, reads naturally, and gives RBOX-side readers an explicit handoff to the Audio Layer project (Strategy 1).
- The cross-repo edit is staged as a patch, not silently applied, per User CLAUDE.md §4.

---

## Reconciliation Strategy (final)

**Primary: Strategy 2 — Annotate this PRD's §12.2.** Applied via Plan 03 (PRD v0.2 promotion).

**Secondary: Strategy 1 — Cross-repo patch to addendum.** Staged below; Dustin to apply manually in the RBOX repo.

---

## Plan 03 Input — v0.2 §12.2 Expansion Text

> The following text is to be inserted into PRD v0.2 §12.2 Companion Documents, replacing the current `addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md` line. Plan 03 (PRD v0.2 promotion) should pick this up verbatim.

**Replace:**

```
| `addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md` | Contains Path A (forked speculative) and Path B (exemplar cache) which compose with Audio Layer; this PRD slots in as effectively "Path E" in that addendum's framing |
```

**With:**

```
| `addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md` (RBOX repo) | Enumerates three latency paths for receptionBOX (Path A — forked speculative S2S drafting; Path B — exemplar-cache-as-default; Path C — watershed routing at SIP edge). The thUMBox Audio Layer is the **graduated platform-layer realization** of what would have been "Path E" in the addendum's framing — the codec-as-LLM-input bet. Because Audio Layer is a platform capability rather than a path internal to receptionBOX, the long-term documentation home is this PRD; the addendum (when next revised) should reference Audio Layer as an external dependency rather than restating its scope. A Path E pointer patch is staged in `docs/decisions/receptionbox-path-e-reconciliation.md` for application to the addendum's home repo. |
```

---

## Cross-Repo Patch (staged for Dustin to apply manually in RBOX repo)

> **Where to apply:** `/home/bob/RBOX/docs/addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md`
> **Section:** End of §4 (after Path C). Insert before §5 (Tradeoff Analysis Across Paths).

Insert the following block as a new subsection at the end of §4:

````markdown
### Path E — LLM-Native Audio Tokens (Graduated to Platform Layer)

**Status:** Graduated to its own platform-layer project as of 2026-05-07.

**Source:** thUMBox Audio Layer technical PRD — `audiolayer-technical-prd-v0_*.md` in the `thumbox-audio-layer` repo. Linear project `thUMBox Audio Layer` (M0–M4 milestones). Inception: receptionBOX latency-unconventional addendum framing (this document).

**The bet:** Replace the lossy ASR → text → LLM cascade with an LLM consuming neural audio tokens directly. Adds the codec layer as a parallel pipeline alongside ASR (which continues for guardrails + audit), then progressively specializes the codec per-firm.

**Three sub-phases:**

- **Phase 0 (2 weeks)** — Mimi feasibility spike on Strix Halo. Binary go/no-go.
- **Phase 1 (6-10 weeks)** — Predictive-delta ASR. Predictor + delta processor inside the existing cascade. Composable with Path A (forked speculative S2S drafting) and Path B (exemplar cache) — they're complementary.
- **Phase 2 (3-4 months)** — Mimi codec integration as parallel pipeline; LLM consumes audio tokens via fine-tuned adapter. Research-grade; gated on board appetite + Mimi licensing.
- **Phase 3 (6+ months)** — Per-firm codec fine-tuning on the firm's call corpus, on-appliance. The differentiator: "appliance gets faster the more your firm uses it."

**Composes with this addendum's paths:**

- Stacks on top of Path A (forked speculative): the audio-token input layer is upstream of speculative draft generation; either path's win compounds with the other.
- Stacks on top of Path B (exemplar cache): audio-similarity exemplar matching becomes possible at the token level (currently only text-level cache hits in this addendum).
- Independent of Path C (watershed routing): admission control operates at SIP edge, before either text-cascade or token-cascade has run.

**Reason for graduation out of receptionBOX:** Audio Layer is platform infrastructure consumed by voice packs (receptionBOX first, future voice packs later), not a path internal to receptionBOX. Per DR-AL-1 in the Audio Layer PRD: customers don't buy "audio infrastructure"; they buy receptionBOX. Treating the codec layer as a graduated platform project means the latency wins extend to all future voice packs without re-implementation per pack.

**Latency win estimate:**

- Phase 1 (predictive-delta ASR): 80-150ms p90 reduction
- Phase 2 (audio codec input): +150-300ms p90 reduction (research-grade estimate)
- Phase 3 (per-firm codec): marginal raw latency, but median experience drops below human perception threshold consistently

Combined with this addendum's Paths A + B, the realistic p90 floor falls to ~300-450ms.

**Where to track Path E from receptionBOX-side:** Cross-reference to thUMBox Audio Layer PRD only; do not duplicate scope here.
````

---

## Edits Applied

- **This document committed** to `docs/decisions/receptionbox-path-e-reconciliation.md` (Phase 1 deliverable).
- **No silent cross-repo edits** — the addendum patch is staged above for Dustin to apply manually (User CLAUDE.md §4 respected).
- **PRD v0.2 §12.2 expansion** is staged here for Plan 03 to apply at v0.2 promotion.

---

## Action Items

- [x] Locate addendum (result: found at `/home/bob/RBOX/docs/addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md`).
- [x] Read addendum structure; confirm Path E is forward-looking, not pre-existing.
- [x] Choose strategy (Strategy 2 + 1).
- [x] Capture v0.2 §12.2 expansion text for Plan 03.
- [x] Stage cross-repo Path E patch for the addendum.
- [x] Linear DEV-1043 closed (Delivered) with link to this doc.
- [ ] **Plan 03:** Apply the §12.2 expansion text in PRD v0.2.
- [ ] **Dustin (cross-repo, non-blocking):** Apply the staged Path E patch to `/home/bob/RBOX/docs/addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md`. This is a one-time manual edit; not a Phase 1 blocker.
