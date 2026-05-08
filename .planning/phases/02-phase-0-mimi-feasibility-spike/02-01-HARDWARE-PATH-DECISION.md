# Phase 2 — Hardware Path Decision

**Decision:** **Path Cloud** — TensorWave MI300X (ROCm) with explicit Strix Halo derating per RBOX §7 methodology.
**Operator:** Dustin
**Date:** 2026-05-07
**Plan:** [02-01-PLAN.md](./02-01-PLAN.md) Task 1 (`checkpoint:decision`)
**Linear:** [DEV-1045](https://linear.app/staqs/issue/DEV-1045)
**Status:** Resolved.

---

## Rationale

**Constraint stack:** PRD §8.3 specifies T3 (Strix Halo, AMD Ryzen AI Max+ 395, 128 GB unified memory) as the primary target. No local Strix Halo dev unit is currently available (per `/home/bob/RBOX/CLAUDE.md` — receptionBOX Phase 0 is gated by the same hardware question). Phase 0 has a 2-week timebox (DR-AL-5) and a binary go/no-go deliverable (PRD §10.1, ROADMAP Phase 2 success criteria).

**Path Cloud chosen because:**

1. **Executable now.** receptionBOX Phase 0 already validated this provisioning path (RBOX/CLAUDE.md §1.2). The spike can start within hours, not weeks.
2. **Bounded cost.** RBOX §13 reference budget puts MI300X spike subtotal at ~$54; the Audio Layer Phase 0 spike is narrower than receptionBOX Phase 0, so total Phase 0 spend stays under the $200 cap (see Cost Ceiling below).
3. **Toolchain alignment.** Same `rocm/pytorch` image, same HF revision pinning, same `uv` lockfile discipline that the broader project will use later. Reuse, not reinvent.
4. **Preserves the timebox.** Path Hardware would block Phase 0 on hardware procurement timeline, defeating the 2-week timebox semantics and stalling Phase 1 indefinitely.
5. **Derating methodology already developed.** RBOX §7 already articulates the derating approach (memory-bandwidth ratio for decode-bound work, Strix Halo prompt-processing penalty for compute-bound work). Reuse the methodology; don't invent a new one.

**Path Hardware was considered and rejected** because the wait-cost compounds (Phase 1, Phase 2, Phase 3 all gated downstream of Phase 0) and PRD §6.2 Phase 0 kill criteria are honest about MI300X-versus-Strix-Halo derating uncertainty: a pass on cloud is a *prediction*, not a guarantee. The Phase 0 evaluation document (Plan 02-05) will surface this uncertainty as a first-class risk in §3.5 and §7, not as a footnote.

---

## Derating Commitment (Path Cloud)

Per RBOX §7 methodology, the Plan 02-05 evaluation document **must** publish:

1. **Raw MI300X measurements** — p50, p90, p99 with confidence intervals, n_samples, runtime configuration (image digest, ROCm version, vLLM version where applicable).
2. **Derated Strix Halo predictions** — applied separately for:
   - **Bandwidth-bound stages** (Mimi decode, LLM decode tokens/sec): use the memory-bandwidth ratio. MI300X realized ~80% of 5.3 TB/s = ~4.24 TB/s. Strix Halo realized ~212 GB/s. Ratio ~20×. Apply this to per-chunk decode latency.
   - **Compute-bound stages** (Mimi encode prefill, adapter forward pass): use the Strix Halo prompt-processing penalty. Phoronix Nov 2025 data shows Strix Halo HIP backend at "barely beats CPU" for prompt processing — derating factor 10–15× rather than the bandwidth ratio.
3. **Confidence intervals on derated numbers.** Bootstrap the raw measurements; propagate the derating factor with explicit upper/lower bounds. Do not present a single derated number as if it were measured.
4. **Honest uncertainty section.** What we do NOT know: production Ollama overhead vs vLLM, real PSTN audio vs synthetic μ-law, ROCm 7 stability under sustained load, BIOS-configurable Strix Halo VRAM allocation (96 GB conservative; up to ~120 GB at higher BIOS settings). RBOX §7 already documents this list — reuse verbatim where applicable.

A pass on raw MI300X with the derate predicting < 100ms/chunk decode (PRD §6.2 kill criterion) is a **conditional pass** — it triggers Phase 1, but the Phase 1 evaluation document (downstream) must re-validate against real Strix Halo if hardware lands by then.

---

## Switch Criterion

The spike can switch from Cloud to Hardware (or vice versa) **mid-flight** under any of these conditions:

- **Strix Halo dev unit lands during the spike.** Switch to Path Hardware immediately. Re-run measurements directly. The two-week timebox runs against either path, not against both.
- **MI300X provisioning is blocked.** If TensorWave + Vultr both fail to provision within 24 hours of Task 2 start, escalate to operator and consider Path Hardware as fallback even if it extends the timebox. Document the timebox extension explicitly in the Phase 0 evaluation document.
- **Cloud spend approaches ceiling.** If projected Phase 0 spend exceeds $200 (see Cost Ceiling below), pause the spike, re-confirm budget with the operator, and consider switching to Path Hardware if hardware ETA is now visible.

The decision to switch is the operator's (Dustin's). Claude-side: surface the trigger with evidence (provisioning logs, spend trajectory, hardware ETA) — do not switch autonomously.

---

## Cost Ceiling

**Default cap: $200 across all of Phase 0.**

This matches RBOX precedent (Phase 0 of receptionBOX is the same dollar order). Audio Layer Phase 0 is narrower in scope (4 measurement battery + 1 stretch experiment + 1 evaluation doc), so the spend should land closer to $50–100 actual.

**Hard stop:** TensorWave/Vultr dashboard-side spending limit of $200 monthly applied during Task 2 provisioning. A runaway pod cannot exceed this.

**Soft trigger:** At $150 actual spend, pause and reconfirm with operator before continuing. Document the reason (extra runs, idle time, contingency benchmarks).

**Contingency budget:** RBOX §13 allocates ~$17 for re-runs. Audio Layer plans should treat this as a floor — if the first measurement run fails (provisioning, image, model download), there's $17 to retry. If multiple retries fail, escalate.

---

## Open Items / Carry-Forward

These were not resolved in this decision but must be tracked through Phase 0 execution:

- **NC-AL-3** (Mimi decode latency on Strix Halo) — Path Cloud measures on MI300X with derating; the un-derated raw number is a *ceiling*, not the answer. The PRD §6.2 kill criterion targets Strix Halo directly. Plan 02-05 must call this out explicitly.
- **NC-AL-1** (VRAM at 4 concurrent calls on Strix Halo) — VRAM derating is qualitatively different from latency derating. MI300X has 192 GB HBM3; Strix Halo allocates up to ~96–120 GB to GPU depending on BIOS. The derate is a capacity-fit check, not a bandwidth/compute ratio. Plan 02-02 Task 2 handles this via the `derate_vram_to_strix` function with parameterized allocation.
- **AMD ROCm 7 stability** — Phoronix Nov 2025 data is on ROCm 7 / Strix Halo; cloud measurement uses ROCm 6.4 (RBOX-validated). The derate must acknowledge a possible ROCm-version delta. Document in Plan 02-05.

---

## Linkage

- **Linear:** DEV-1045 (env setup) — this decision unblocks Task 2 (provisioning).
- **Plan 02-01 Task 1** (`checkpoint:decision` blocking gate) — resolved by this document.
- **Plan 02-02 Task 2** — must read this decision's "Derating Commitment" section before publishing VRAM derate.
- **Plan 02-05 Task 1** — must surface "Open Items / Carry-Forward" above as first-class risks in the Phase 0 evaluation doc, NOT as footnotes.
- **RBOX §7** — reused derating methodology; cross-reference: `/home/bob/RBOX/CLAUDE.md`.

---

*Resolves Plan 02-01 Task 1 (checkpoint:decision). Task 2 (cloud provisioning) is unblocked.*
