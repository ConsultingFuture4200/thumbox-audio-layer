# DR-AL-3 — Mimi (Kyutai) Commercial Licensing

**Status:** PENDING-LEGAL-REVIEW
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

> *To be inserted after counsel review. Replace this section with counsel's verbatim response (or a faithful summary with counsel's review noted) before changing the Status field.*

Q1 response: _pending_

Q2 response: _pending_

Q3 response: _pending_

---

## DR-AL-3 Status

**Status:** candidate (pending legal review)

To be promoted to one of the following on counsel response:

- **adopted** — license clearly permits commercial appliance distribution with no material conditions; promote DR-AL-3 from "candidate" to "adopted" with citation to legal's response.
- **adopted-with-conditions** — permitted with attribution / notice obligations; document the obligations as a Phase 2 ship-gate checklist (which appliance surfaces require attribution, what NOTICE format, etc.). Most likely outcome given CC-BY-4.0.
- **rejected** — license restricts commercial use in a way that breaks the appliance model; mark DR-AL-3 rejected and trigger NC-AL-10 contingency planning (alternative codec — EnCodec / DAC / custom). NC-AL-10 contingency is a Phase 2 scoping concern, not a Phase 1 deliverable; flag it in this doc and file a follow-up Linear issue if needed.

---

## Phase 2 Ship-Gate Checklist (populated on adoption-with-conditions)

> *To be filled if Q2 returns specific attribution requirements.*

- [ ] NOTICE file at appliance root listing Mimi attribution
- [ ] Appliance documentation page citing Mimi + Kyutai + license
- [ ] Customer-facing material attribution (if required)
- [ ] (Q3 follow-on) firm-head training audit-log entry citing base codec

---

## Appendix A — License Text

Full CC-BY-4.0 text: https://creativecommons.org/licenses/by/4.0/legalcode

Hugging Face model card extract:

> **License:** cc-by-4.0
>
> *Out-of-scope use:* The model is not intended to be used to impersonate other people or any malicious use of any kind.

---

## Action Items

- [ ] **Dustin:** Route this document to legal counsel. Same counsel as NC-AL-6 if practical (both are appliance/data-handling questions for the same product).
- [ ] **Claude (on counsel response):** Insert verbatim response into "Legal's Written Position" section. Update Status field. Update Linear DEV-1039 with comment + Done status.
- [ ] **Claude (on counsel response):** If status = rejected, file follow-up Linear issue against NC-AL-10 contingency.
