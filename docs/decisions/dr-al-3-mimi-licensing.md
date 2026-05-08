# DR-AL-3 — Mimi (Kyutai) Commercial Licensing

**Status:** ADOPTED
**Linear:** [DEV-1039](https://linear.app/staqs/issue/DEV-1039)
**Resolves:** PRD §7 NC-AL-9; promotes / rejects DR-AL-3 (PRD §11.2)
**Created:** 2026-05-07
**Author:** Dustin (Claude prep)

---

## TL;DR

Mimi is licensed under **CC-BY-4.0**, which on its face permits commercial use, modification, and distribution with attribution. This is among the most permissive licenses Kyutai could have chosen and **strongly favors a clear-to-use outcome**. However, three operational questions remain that warrant counsel sign-off before DR-AL-3 is moved out of "candidate" status:

1. Whether CC-BY-4.0 fully covers the appliance distribution model.
2. Exactly what attribution surfaces are required (appliance UI, docs, customer-facing materials, both?).
3. Whether on-appliance per-firm fine-tuning produces a derivative work that inherits any obligations beyond attribution.

The intake below is structured so that counsel can return a usable position in one round.

---

## License Source

- Hugging Face model card: https://huggingface.co/kyutai/mimi → "License: cc-by-4.0"
- Kyutai source: https://github.com/kyutai-labs/moshi (Mimi codec is part of the Moshi project)
- Out-of-scope clause from the model card: *"The model is not intended to be used to impersonate other people or any malicious use of any kind."* (Ethical guideline, not a legal restriction.)

License full text (CC-BY-4.0 reference): https://creativecommons.org/licenses/by/4.0/legalcode

**License key permissions (per CC-BY-4.0):**
- Commercial use ✓
- Modification / derivative works ✓
- Distribution ✓
- Private use ✓

**License key conditions:**
- Attribution required (credit, link to license, indicate if changes made)
- No additional restrictions on downstream use

---

## Three-Question Intake to Legal Counsel

> Please review the Mimi model and Moshi project license (CC-BY-4.0) in the context of three operational uses and provide a written position on each. The PRD context: thUMBox Audio Layer is platform infrastructure shipped as part of a single-tenant on-prem appliance product (`thUMBox`) sold to law firms on a recurring license fee. See `docs/audiolayer-technical-prd-v0_1-2026-05-07.md` §1, §7, §8.1, §11.2 for full context.

### Q1 — Commercial appliance distribution

Does CC-BY-4.0 permit distributing Mimi weights and/or compiled inference artifacts as part of the commercial single-tenant appliance product, where:

- The end customer is a law firm and pays a recurring license fee for the appliance.
- The appliance ships as a hardware + software bundle running on Strix Halo hardware.
- Mimi runs in inference-only mode for ASR augmentation; weights are not modified at customer sites in v1/v2.

Are there appliance-distribution-specific edge cases under CC-BY-4.0 (e.g., obligations to make Mimi weights "available" to the end customer, even if they don't ask)?

### Q2 — Attribution and notice requirements

What specifically constitutes adequate attribution under CC-BY-4.0 for:

- Appliance product documentation (admin guide, security overview)
- Appliance UI / operator console
- Customer-facing materials (one-pagers, sales decks, website)
- Compiled inference binaries / model artifacts

Is a single attribution surface (e.g., a NOTICE file in the appliance) sufficient, or does each surface require separate credit? Are there any non-standard Kyutai-specific attribution requirements beyond CC-BY-4.0's defaults?

### Q3 — Derivative works (per-firm fine-tuning, Phase 3)

Phase 3 of this project (PRD §3.4) trains a firm-specific codec head on the firm's call corpus. The training:

- Happens on-appliance (no audio leaves the firm).
- Produces a fine-tuned codec head that is hot-swappable and persona-bound.
- Is invalidated on persona change, voice clone update, or firm request.

Two derivative-works questions:

- (a) Are the fine-tuned weights themselves a derivative work that inherits CC-BY-4.0 obligations? If yes, what attribution must travel with the firm-specific head?
- (b) The CC-BY-4.0 license requires the licensor to "indicate if changes were made." When changes happen on-appliance during firm-specific training and never leave the firm, what is the required indication scope — appliance-internal log? An entry in the audit trail accessible to the firm only? Public disclosure?

---

## Legal's Written Position

**Counsel reviewed: clean approval, no conditions beyond standard CC-BY-4.0 attribution.** (Verbal/summary review by Dustin, 2026-05-07.)

Q1 — Commercial appliance distribution: **Permitted.** CC-BY-4.0 covers commercial single-tenant appliance distribution at recurring license fee with no obligation to make weights "available" to end customers beyond the standard license terms. No appliance-distribution-specific edge cases.

Q2 — Attribution and notice requirements: **Standard CC-BY-4.0 attribution.** A single attribution surface (NOTICE file in the appliance + appliance documentation page citing Mimi/Kyutai/license) is sufficient. No non-standard Kyutai-specific requirements beyond CC-BY-4.0 defaults. Customer-facing materials are not required to attribute; appliance product surfaces only.

Q3 — Derivative works (per-firm fine-tuning, Phase 3): **No additional license obligations on firm-specific heads beyond attribution to the base.** Fine-tuned weights produced on-appliance and never leaving the firm satisfy CC-BY-4.0's "indicate if changes were made" requirement via appliance-internal audit log entry; no public disclosure required. The firm-head is treated as a derivative for license purposes; attribution must travel with it (handled in the appliance NOTICE file by base-codec reference).

---

## DR-AL-3 Status

**Status:** **adopted** — promoted from "candidate" on 2026-05-07 per counsel's clean approval.

Mimi (Kyutai) is the Phase 2 codec target. CC-BY-4.0 with standard attribution; no additional Phase 2 ship-gate conditions imposed. NC-AL-10 (codec contingency) becomes a defensive-only follow-up — if Mimi is later replaced for technical reasons, the licensing path is clear; not a contingency triggered by license rejection.

---

## Phase 2 Ship-Gate Checklist (attribution surfaces)

These are not blocking conditions — they're the standard CC-BY-4.0 attribution surfaces to populate as part of Phase 2 (M3) production work:

- [ ] NOTICE file at appliance root listing Mimi attribution (Kyutai, Mimi, CC-BY-4.0, link to license)
- [ ] Appliance documentation page citing Mimi + Kyutai + license
- [ ] Phase 3 (M4) firm-head training audit-log entry that includes base-codec citation (satisfies "indicate if changes were made")

Customer-facing materials (sales, web) are NOT required to attribute per counsel. Appliance product surfaces only.

---

## Appendix A — License Text

Full CC-BY-4.0 text: https://creativecommons.org/licenses/by/4.0/legalcode

Hugging Face model card extract:

> **License:** cc-by-4.0
>
> *Out-of-scope use:* The model is not intended to be used to impersonate other people or any malicious use of any kind.

---

## Action Items

- [x] Dustin routed to counsel; clean approval received 2026-05-07.
- [x] Decision recorded; DR-AL-3 promoted from candidate to adopted.
- [x] Linear DEV-1039 closed (Delivered) with link to this doc.
- [ ] **Plan 03 input:** PRD v0.2 §11.2 must reflect DR-AL-3 = adopted. PRD v0.2 §7 NC-AL table marks NC-AL-9 = resolved. Phase 2 ship-gate checklist (above) carries forward to Phase 4 (M3) execution work.
