# thUMBox Audio Layer — Technical PRD

## v0.2

> **Created:** 2026-05-07 (v0.1 baseline) | **Promoted:** 2026-05-07 (v0.2)
> **Author:** Dustin (UMB Group), with Claude
> **Status:** **Accepted** — Phase 1 (M0) coordination gates closed; project moves from "strawman" to "committed scope"
> **Project type:** Platform-layer capability (not a personality pack)
> **Name:** **thUMBox Audio Layer** (finalized 2026-05-07; alternatives ruled out per §1.4 historical record)
> **Parent:** `thumbox-technical-prd-v2_1-2026-04-16.md`
> **First consumer:** receptionBOX (`receptionbox-technical-prd-v0_2-2026-05-06.md`) — graduated platform-layer project; "Path E" in receptionBOX latency-unconventional addendum framing (see §12.2)
>
> **Changelog:**
> - **v0.2 (2026-05-07)** — Promotion from v0.1 strawman to Accepted scope after pressure-testing. Resolves PRD §13 Open Items #1 (naming), #4 (bandwidth), #5 (Mimi licensing), #6 (predictor corpus), #7 (Path E framing). NC-AL-6, NC-AL-9, and NC-AL-12 closed with written positions (`docs/decisions/`). DR-AL-3 promoted from candidate to adopted (Mimi is CC-BY-4.0, clean commercial appliance approval). Phase 2 staffing path = (a) internal headcount, owner = Dustin, conditional on Phase 0 + Phase 1 entry gates. Partner corpus = Path A (signed agreement; details in Heron Labs CRM). Items #2 (scope: three-phase decomposition vs Phase 1 only) and #3 (T2 hardware tier as strategic priority) remain open and tracked. **Performance numbers in this document remain exploratory and require Phase 0 validation before being relied upon.**
> - v0.1 (2026-05-07) — Initial draft. Establishes scope, three-phase roadmap, hardware targets, success criteria, and Phase 0 prototype plan. Proposes DR-AL-1 through DR-AL-6 as candidate decision records and SM-AL-1 through SM-AL-9 as candidate metrics. NC-AL-1 through NC-AL-12 captured as open questions. Historical baseline preserved at `docs/audiolayer-technical-prd-v0_1-2026-05-07.md`.

---

## §1. Project Identity

### §1.1 What This Is

The **thUMBox Audio Layer** is platform-layer infrastructure that lets thUMBox personality packs consume audio as an LLM-native token stream rather than as text transcripts produced by ASR.

It is not a personality pack. Customers do not buy it. It is a capability that *enables* receptionBOX (and future voice-bearing packs) to achieve latency, expressiveness, and cost characteristics that a conventional ASR → text → LLM cascade cannot reach.

### §1.2 What Problem It Solves

Conventional voice agent architectures use Automatic Speech Recognition to convert audio into text, then feed text to an LLM. This pattern is universal and well-supported, but it has three structural problems the cascade cannot work around:

**Lossiness.** Text discards prosody, emphasis, hesitation, emotional valence, and speaker characteristics. An LLM consuming text loses information that would help it disambiguate intent, detect distress, or recognize returning callers.

**Serial dependency.** The LLM cannot begin processing until ASR commits to a transcription. Streaming partial-hypothesis ASR mitigates this but introduces rollback complexity when partials change. The architectural shape — text as a commit boundary — limits how aggressively the cascade can be parallelized.

**Compression mismatch.** Text is roughly 10,000× more compressed than raw audio (320,000 samples per 10 seconds of 16kHz audio vs. ~30 text tokens). Neural audio codecs like Mimi (12.5 Hz, 1.1 kbps) demonstrate that LLM-comprehensible audio representations exist at densities much closer to text than to raw audio. There is unused middle ground.

The Audio Layer occupies that middle ground: a learned compression of audio into discrete tokens optimized for LLM consumption rather than for human-audible reconstruction.

### §1.3 The Asymmetry Argument

This capability matters more on a single-tenant appliance than in a multi-tenant cloud, for three reasons:

1. **Per-firm fine-tuning.** A single-firm appliance can train the codec on the firm's actual call distribution, compressing aggressively on signal regions that don't vary across the firm's case mix and preserving regions that do. Cloud voice AI cannot safely do this without per-tenant model isolation that breaks economics.

2. **Dedicated silicon.** Running a neural codec alongside an LLM and TTS engine requires VRAM that's wasteful in cloud (idle when no calls active, contended when many calls active). On a Strix Halo 128GB unified memory appliance handling 4 concurrent calls, the silicon is already paid for.

3. **Long-horizon caching.** Audio token streams enable caching strategies (compositional reconstruction from cached fragments, audio-similarity exemplar matching) that don't work at the text level. These strategies compound over months of single-firm use.

This is the same asymmetry argument receptionBOX's Path B already exploits, generalized to the codec layer.

### §1.4 Naming

**Final name: thUMBox Audio Layer.** Decided 2026-05-07 (Phase 1 / M0 closure). Rationale: signals platform infrastructure, not customer-facing pack. Capitalization follows existing thUMBox convention (lowercase *th*, uppercase *UMB*, lowercase *ox*) where applicable.

Alternatives ruled out (historical record):

| Name | Status | Reason ruled out |
|------|--------|------------------|
| codecBOX | Rejected | Implies customer-facing pack — directly contradicts DR-AL-1 |
| NeuroCodec | Rejected | No brand connection to thUMBox; would orphan from platform context |
| Project Mimi-Delta | Rejected | Signals research-stage only; couples name to specific codec choice |
| audioLayer | Rejected | No precedent for lowercase-camel platform-layer naming in thUMBox |

Full decision audit: `docs/decisions/naming-decision.md`.

### §1.5 Out of Scope

The following are explicitly out of scope for this PRD:

- TTS pipeline changes (covered in receptionBOX PRD §5.3)
- SIP edge or carrier integration (covered in receptionBOX PRD §4.2)
- Personality pack contract changes (this layer is consumed by packs, not a pack itself)
- Multi-modal extensions (vision, video) — audio only
- Replacing the ASR pipeline entirely — the Audio Layer runs *alongside* ASR in v1, not instead of it (see §3)

---

## §2. Project Scope

### §2.1 Three Composable Ideas

This project encompasses three structurally related but technically distinct ideas:

| Idea | What it is | Phase |
|------|-----------|-------|
| **Idea 1** — Predictive-delta ASR | Predict the caller's likely utterance from history/context; process incoming audio as corrections to the prediction | Phase 1 (v1) |
| **Idea 2** — LLM-targeted neural audio codec | Encode audio into discrete tokens consumable directly by an LLM, bypassing text transcription | Phase 2 (v1.5) |
| **Idea 3** — Per-firm codec fine-tuning | Specialize the codec to a single firm's call distribution for higher compression ratios and better signal preservation on firm-specific patterns | Phase 3 (v2) |

These compose: Idea 2 is the architectural substrate; Idea 1 can be implemented on top of either text or audio tokens but becomes more powerful with audio tokens; Idea 3 only matters once Idea 2 is in production.

### §2.2 Phasing Rationale

Rather than treating this as one monolithic research project, the work decomposes into three increasingly ambitious phases with clear go/no-go gates between each.

**Phase 1 (Idea 1)** is achievable in weeks using existing tools. It delivers measurable latency improvement to receptionBOX without requiring any custom model training. It validates whether the predictive-decoding analogy carries useful signal at the application layer before the team commits to the harder model-training work.

**Phase 2 (Idea 2)** is the architectural bet. It requires custom model integration, fine-tuning a small LLM to consume audio tokens, and rebuilding parts of the receptionBOX guardrail and observability layers to operate on tokens rather than text. This is research-grade work — 2-4 months of focused engineering plus GPU budget. It only proceeds if Phase 1 demonstrates that predictive decoding is a productive lens.

**Phase 3 (Idea 3)** is the differentiator. Per-firm fine-tuning makes the asymmetry argument concrete and produces the marketing-legible claim that "the appliance gets faster the more your firm uses it." This phase only matters if Phase 2 ships and produces stable production behavior.

### §2.3 What Each Phase Delivers

**Phase 0 — Prototype (2 weeks)**
- 200-line spike: mic input → Mimi encoder → log tokens → decode → audible output
- Bonus stretch: feed Mimi tokens to a small LLM (Qwen2.5-0.5B fine-tune) via custom embedding layer; observe whether the LLM produces *any* coherent behavior conditioned on audio tokens
- Deliverable: go/no-go decision for Phase 1 based on whether the basic pipeline works on Strix Halo or T3-class hardware
- **Kill criteria:** Mimi decode latency > 100ms per chunk on T3 hardware, OR LLM cannot be made to produce coherent behavior conditioned on audio tokens within the spike timebox

**Phase 1 — Predictive-Delta ASR (v1.5 of receptionBOX, 6-10 weeks)**
- Predictor model: small LLM (Qwen3-0.5B or similar) trained on the firm's 90-day intake corpus to predict the caller's next utterance given call context (ANI, time-of-day, partial transcript so far)
- Delta processor: a layer that takes streaming partial ASR output and computes the divergence from the prediction; commits prediction-aligned regions immediately, processes divergent regions through normal cascade
- Integration: shipped as an optional optimization within receptionBOX's existing cascade — no architectural changes to packs that don't opt in
- **Success metric:** ≥ 100ms p90 latency reduction on calls where prediction confidence > threshold T (T to be calibrated during Phase 1)

**Phase 2 — LLM-Targeted Audio Codec (v1.5/v2, 3-4 months)**
- Codec: Mimi (or successor) integrated into the receptionBOX agent-worker as a parallel pipeline alongside ASR
- Adapter: trained projection layer that maps audio tokens into a representation the existing Qwen3-4B can consume via cross-attention on a fine-tuned input embedding
- Guardrail layer: extended to operate on audio tokens (likely by maintaining a parallel text decode for guardrail purposes only — see §4.4)
- Integration: opt-in per-pack; receptionBOX is the first consumer
- **Success metric:** ≥ 200ms p90 latency reduction over Phase 1 baseline, with no degradation in intent classification accuracy or guardrail recall

**Phase 3 — Per-Firm Codec Fine-Tuning (v2+, 6+ months)**
- Fine-tuning pipeline: training a per-firm codec head on the firm's 90-day call corpus, with privacy-preserving training (no cross-tenant data leakage)
- Deployment: codec head is shipped as part of the firm's persona, hot-swappable with appliance restart
- Telemetry: continuous monitoring for codec drift, distribution shift in firm call patterns
- **Success metric:** ≥ 30% additional compression ratio on firm-specific call patterns vs. generic codec, with no degradation in downstream task accuracy

---

## §3. Architecture

### §3.1 High-Level Position in thUMBox Stack

```
┌──────────────────────────────────────────────────────────────────┐
│  thUMBox Platform                                                 │
│                                                                  │
│  ┌────────────────┐  ┌──────────────────┐  ┌───────────────────┐│
│  │ Personality    │  │ Personality      │  │ Personality       ││
│  │ Packs (voice)  │  │ Packs (text)     │  │ Packs (workflow)  ││
│  │ - receptionBOX │  │ - MailBOX        │  │ - financeBOX      ││
│  │ - (future)     │  │ - researchBOX    │  │ - (future)        ││
│  └───────┬────────┘  └────────┬─────────┘  └─────────┬─────────┘│
│          │                    │                      │          │
│  ┌───────▼─────────────────────────────────────────────────────┐ │
│  │ Audio Layer (NEW)                                          │ │
│  │  - Predictor (Phase 1)                                     │ │
│  │  - Codec encoder/decoder (Phase 2)                         │ │
│  │  - Per-firm fine-tuned heads (Phase 3)                     │ │
│  │  - Token-stream guardrail extension (Phase 2)              │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│  ┌───────────────────────────▼───────────────────────────────────┐│
│  │ Shared Platform Services (Ollama, Qdrant, Postgres, etc.)    ││
│  └───────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

The Audio Layer sits between the personality pack runtime and the shared platform services. Voice-bearing packs opt into Audio Layer features via configuration; non-voice packs are unaffected.

### §3.2 Phase 1 Architecture (Predictive-Delta ASR)

```
                ┌─────────────────────────────────┐
                │ Audio Layer — Phase 1            │
                │                                  │
   audio ──────►│ ASR (existing whisper-stt)      │──► partial transcript ──┐
   (existing)   │                                  │                        │
                │ Predictor (Qwen3-0.5B fine-tuned)│──► predicted utterance ┤
                │   ↑                              │                        ├──► committed text ──► LLM
                │   │ context: ANI, time, history  │                        │
                │                                  │                        │
                │ Delta Processor                  │◄───────────────────────┘
                │   - aligns partial vs prediction │
                │   - commits matched regions      │
                │   - flags divergent regions      │
                └─────────────────────────────────┘
```

Phase 1 is purely additive. The existing ASR cascade continues to work; the predictor and delta processor are inserted as a fast-path that commits text earlier when prediction confidence is high. On low-confidence calls the cascade behaves identically to today.

### §3.3 Phase 2 Architecture (Audio Codec Layer)

```
                ┌────────────────────────────────────────────────┐
                │ Audio Layer — Phase 2                          │
                │                                                │
   audio ──┬───►│ Mimi encoder ──► audio tokens ──┐              │
           │    │                                  │              │
           │    │                                  ▼              │
           │    │                          ┌────────────────┐     │
           │    │                          │ Adapter         │     │
           │    │                          │ (cross-attn,    │──┬──┼──► LLM
           │    │                          │  fine-tuned     │  │  │
           │    │                          │  embedding)     │  │  │
           │    │                          └────────────────┘  │  │
           │    │                                              │  │
           └───►│ ASR (whisper-stt)         ┌──────────────────┘  │
   (parallel)   │   ↓                        ▼                    │
                │   text ──────────────────► Guardrail Filter     │
                │              (operates on text for safety)      │
                └────────────────────────────────────────────────┘
```

Critically, the ASR cascade *does not go away* in Phase 2. It runs in parallel for two reasons: guardrail safety (text-based PII detection, UPL refusal patterns, prompt injection patterns are mature; token-based equivalents are not) and observability (transcripts remain the canonical user-readable record). The latency win comes from the LLM consuming audio tokens directly while ASR runs in parallel for audit purposes only.

This addresses the most legitimate concern about an all-token architecture: the "you own the data" story degrades if the canonical record is opaque tokens. By keeping text transcripts as a parallel artifact, we preserve auditability while still capturing the latency benefit.

### §3.4 Phase 3 Architecture (Per-Firm Fine-Tuning)

Phase 3 modifies the Mimi encoder of Phase 2. The base codec is replaced with a base-encoder-plus-firm-specific-head architecture. The base encoder is shipped with the appliance and never modified. The firm-specific head is trained on the firm's call corpus with privacy-preserving training procedures (training happens on-appliance; no audio leaves the firm).

Architecture details for Phase 3 are deliberately underspecified at v0.1. The Phase 2 work will surface constraints that determine the right Phase 3 design. **This PRD does not commit to a specific Phase 3 architecture yet.**

### §3.5 Key Design Decisions

**DR-AL-1 (candidate): Audio Layer is platform infrastructure, not a pack.**
Rationale: Customers don't buy "audio infrastructure"; they buy receptionBOX. Treating this as a pack creates artificial commercial gating on capability that benefits all voice packs.
Status: Candidate — adopted on PRD acceptance.

**DR-AL-2 (candidate): ASR cascade remains in place through all phases.**
Rationale: Guardrail maturity, audit-trail legibility, customer-facing "you own the data" pillar. Latency wins come from parallelization with ASR, not replacement of ASR.
Status: Candidate — adopted on PRD acceptance.

**DR-AL-3 (adopted v0.2): Mimi is the Phase 2 codec target.**
Rationale: Strongest published track record (Moshi, real-time inference at 12.5Hz, established LLM-input semantics). Alternatives (EnCodec, SoundStream, DAC) are similar but less proven for LLM-input use.
Status: **Adopted** (2026-05-07). Mimi is CC-BY-4.0; counsel confirmed clean approval for commercial single-tenant appliance distribution with standard attribution surfaces (NOTICE file + appliance docs). NC-AL-9 resolved (`docs/decisions/dr-al-3-mimi-licensing.md`). NC-AL-3 (Phase 0 latency validation on Strix Halo) remains open and is the binary Phase 0 gate.

**DR-AL-4 (candidate): receptionBOX is the first and only Phase 1/2 consumer.**
Rationale: Voice packs are the obvious consumers; receptionBOX is the only voice pack in the roadmap. Generalizing to other packs is a v3+ concern.
Status: Candidate — adopted on PRD acceptance.

**DR-AL-5 (candidate): Phase 0 is gated on a 2-week timeboxed prototype.**
Rationale: The strongest signal on whether Phase 1 is worth committing to is whether the basic Mimi pipeline runs at acceptable latency on target hardware. This is a pure feasibility question with a binary answer.
Status: Candidate — adopted on PRD acceptance.

**DR-AL-6 (candidate): FFmpeg/libavcodec patterns inform the streaming and timing layer; FFmpeg is not used as the neural runtime.**
Rationale: 25 years of solved problems in PTS/DTS handling, error resilience, and filter graph composition. Use the abstractions, not the codec implementations. Neural inference happens in ONNX Runtime / TensorRT / native PyTorch.
Status: Candidate — adopted on PRD acceptance.

---

## §4. Functional Requirements

> **Convention.** Functional requirements use the prefix `FR-AL-N`. Non-functional use `NFR-AL-N`. Open questions use `NC-AL-N`. Success metrics use `SM-AL-N`.

### §4.1 Phase 1 Functional Requirements

| ID | Requirement | Phase |
|----|-------------|-------|
| FR-AL-1 | The Audio Layer shall expose a `predictor.predict(context) → predicted_utterance` interface to the agent-worker | 1 |
| FR-AL-2 | The predictor shall consume call context (ANI, time-of-day, conversation history, partial transcript) and emit a predicted utterance with a confidence score | 1 |
| FR-AL-3 | The delta processor shall align streaming partial ASR output against the prediction and emit committed-text events for matched regions | 1 |
| FR-AL-4 | Predictor confidence below threshold T shall fall through to the standard ASR cascade with no behavioral change | 1 |
| FR-AL-5 | The agent-worker shall be able to disable Phase 1 features per-firm or per-call via configuration flag | 1 |
| FR-AL-6 | Predictor inference latency p90 shall be ≤ 50ms on T3 hardware | 1 |
| FR-AL-7 | The predictor shall be retrainable from updated firm corpus on a weekly schedule, with hot-swap on next call boundary | 1 |

### §4.2 Phase 2 Functional Requirements

| ID | Requirement | Phase |
|----|-------------|-------|
| FR-AL-8 | The codec encoder shall consume 16kHz PCM audio and emit Mimi-compatible audio tokens at 12.5Hz | 2 |
| FR-AL-9 | The adapter shall map audio tokens into a representation the LLM consumes via fine-tuned input embedding | 2 |
| FR-AL-10 | The ASR cascade shall continue to run in parallel for guardrail and audit purposes | 2 |
| FR-AL-11 | Guardrail filter shall continue to operate on text from the ASR cascade; token-based guardrails are out of scope for v1 | 2 |
| FR-AL-12 | Transcripts persisted to Postgres shall include both text (from ASR) and audio token sequences (from codec) for audit completeness | 2 |
| FR-AL-13 | Codec encoder/decoder shall be hot-swappable across appliance restarts | 2 |
| FR-AL-14 | The agent-worker shall be able to disable Phase 2 features per-firm or per-call via configuration flag | 2 |

### §4.3 Phase 3 Functional Requirements (Provisional)

| ID | Requirement | Phase |
|----|-------------|-------|
| FR-AL-15 | The codec architecture shall support a base encoder plus firm-specific head | 3 |
| FR-AL-16 | Firm-specific head training shall happen on-appliance; no audio leaves the firm | 3 |
| FR-AL-17 | Firm-specific heads shall be invalidatable on persona change, voice clone update, or explicit firm request | 3 |

These will be refined or replaced based on Phase 2 outcomes.

### §4.4 Guardrail and Observability

A specific concern worth calling out in detail.

The receptionBOX guardrail layer (FR-R41 in receptionBOX PRD) operates on text. It scans utterances for prompt injection patterns, UPL refusal triggers, and PII redaction needs. This works because the patterns are well-understood and the literature on text-based content safety is mature.

Token-based guardrails are not mature. Detecting prompt injection in audio tokens, scanning for PII in audio tokens, or applying UPL refusal patterns to audio tokens is research-grade work that the industry has not solved.

**The Audio Layer's resolution: ASR runs in parallel through Phase 2.** The text path exists alongside the token path, and guardrails operate on text. The token path is *only* used as the input to the LLM for latency purposes. If the guardrail layer flags an utterance for refusal, the LLM's audio-token-conditioned response is discarded and the deterministic refusal fires from the Tier-1 path (receptionBOX PRD §4.4).

This is a real cost — running ASR + codec in parallel uses more compute than either alone — but it preserves the safety story without forcing a research breakthrough on token-based content safety.

---

## §5. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-AL-1 | Phase 1 predictor inference p90 latency on T3 | ≤ 50ms |
| NFR-AL-2 | Phase 1 end-to-end latency improvement over receptionBOX v1 | ≥ 100ms p90 |
| NFR-AL-3 | Phase 2 codec encode latency on T3 | ≤ 30ms per 80ms audio chunk |
| NFR-AL-4 | Phase 2 end-to-end latency improvement over Phase 1 baseline | ≥ 200ms p90 |
| NFR-AL-5 | Memory overhead of Audio Layer on T3 (predictor + codec + adapter resident) | ≤ 8GB VRAM |
| NFR-AL-6 | Audio Layer disabled state shall add ≤ 5ms overhead to standard cascade | All phases |
| NFR-AL-7 | Phase 3 firm-specific head training time on T3 hardware (90-day corpus) | ≤ 24 hours |
| NFR-AL-8 | Predictor accuracy on held-out firm corpus | ≥ 60% utterance-level match |
| NFR-AL-9 | No degradation in intent classification accuracy vs receptionBOX v1 baseline | All phases |
| NFR-AL-10 | No degradation in guardrail recall vs receptionBOX v1 baseline | All phases |

---

## §6. Success Metrics

### §6.1 Candidate Success Metrics

| ID | Metric | Target | Measurement |
|----|--------|--------|-------------|
| SM-AL-1 (cand.) | Phase 0 prototype runs Mimi decode at < 100ms per chunk | Pass/fail | Spike measurement |
| SM-AL-2 (cand.) | Phase 0 prototype demonstrates LLM produces coherent behavior on audio tokens | Pass/fail | Manual evaluation, 20-utterance test set |
| SM-AL-3 (cand.) | Phase 1 p90 latency reduction on high-confidence prediction calls | ≥ 100ms | Production telemetry, receptionBOX |
| SM-AL-4 (cand.) | Phase 1 prediction high-confidence rate | ≥ 40% of calls | Production telemetry |
| SM-AL-5 (cand.) | Phase 2 p90 latency reduction over Phase 1 baseline | ≥ 200ms | Production telemetry |
| SM-AL-6 (cand.) | Phase 2 token-stream commit-to-LLM latency | ≤ 50ms p90 | Production telemetry |
| SM-AL-7 (cand.) | Phase 3 compression ratio improvement on firm-specific patterns | ≥ 30% | Synthetic benchmark |
| SM-AL-8 (cand.) | All phases: intent classification accuracy delta vs v1 baseline | ≥ 0% (no regression) | Daily eval against held-out corpus |
| SM-AL-9 (cand.) | All phases: guardrail recall delta vs v1 baseline | ≥ 0% (no regression) | Daily eval against guardrail test suite |

### §6.2 Kill Criteria

The project is killed at the relevant phase boundary if any of the following conditions hold:

**Phase 0 kill criteria:**
- Mimi decode latency exceeds 100ms per chunk on T3 hardware after reasonable optimization effort
- Phase 0 spike fails to produce any coherent LLM behavior on audio tokens within the 2-week timebox
- Phase 0 reveals VRAM requirements for Mimi + Qwen3-4B + Whisper concurrent that exceed Strix Halo capacity at 4 concurrent calls

**Phase 1 kill criteria:**
- Predictor accuracy plateaus below 40% utterance-level match on a representative firm corpus
- Phase 1 latency reduction p90 below 50ms after full implementation
- Predictor inference latency exceeds 100ms p90 (eats more latency than it saves)

**Phase 2 kill criteria:**
- Phase 2 latency reduction over Phase 1 below 100ms p90
- Intent classification accuracy regresses by more than 2 percentage points
- Guardrail recall regresses by any measurable amount on the receptionBOX UPL test suite
- VRAM overhead exceeds the 8GB budget after reasonable optimization effort

**Phase 3 kill criteria:**
- Per-firm fine-tuning produces less than 15% compression improvement over generic codec (half the target)
- Privacy-preserving training procedures cannot be made robust against any plausible audit
- Hot-swap of firm-specific heads cannot be made robust against state corruption

---

## §7. Open Questions (NC-)

### §7.1 Open

| ID | Question | Blocks |
|----|----------|--------|
| NC-AL-1 | What is the actual VRAM footprint of Mimi + Whisper + Qwen3-4B + adapter on Strix Halo at 4 concurrent calls? | Phase 1 go/no-go |
| NC-AL-2 | Does Pipecat / LiveKit Agents have native support for parallel audio token streams alongside ASR, or does this require custom agent-worker code? | Phase 1 scoping |
| NC-AL-3 | Does Mimi run at acceptable latency on Strix Halo, or does it require a smaller codec (a distilled Mimi or alternative)? | Phase 0 prototype |
| NC-AL-4 | What is the minimum LLM size that can be fine-tuned to consume audio tokens with acceptable behavior? | Phase 2 scoping |
| NC-AL-5 | Can the adapter be trained without per-firm data, using only generic conversational corpora? | Phase 2 scoping |
| NC-AL-7 | What is the threat model for audio-token-based prompt injection, and is it different from text-based prompt injection? | Phase 2 ship gate |
| NC-AL-8 | Is there a defensible way to do per-firm fine-tuning that survives a privacy audit? | Phase 3 ship gate |
| NC-AL-10 | If Mimi licensing is restrictive, what is the credible open-weights alternative (EnCodec, DAC, custom)? | Phase 2 contingency — defensive only after NC-AL-9 cleared |
| NC-AL-11 | Does the FFmpeg/libavcodec timing model integrate cleanly with PyTorch streaming inference, or does this introduce a new abstraction boundary that has its own latency cost? | Phase 1 implementation |

### §7.2 Resolved in v0.2

| ID | Original Question | Resolution | Decision Doc |
|----|-------------------|------------|--------------|
| NC-AL-6 | Legal-counsel position on storing audio tokens alongside text transcripts | **Clear** — tokens treated as audio-equivalent for retention, deletion, breach disclosure, and discovery. FR-AL-12 ship-gate cleared. | `docs/decisions/nc-al-6-audio-token-storage-legal.md` |
| NC-AL-9 | Mimi (Kyutai) commercial licensing | **Clear** — CC-BY-4.0 permits commercial single-tenant appliance distribution with standard attribution. DR-AL-3 promoted from candidate to adopted. | `docs/decisions/dr-al-3-mimi-licensing.md` |
| NC-AL-12 | Eric/Kevin's appetite for research-grade Phase 2 commitment | **Green-light**, internal headcount, Dustin as owner. Conditional on Phase 0 + Phase 1 entry gates. Option (b) external collaboration remains a re-open lever if bandwidth pressure surfaces. | `docs/decisions/nc-al-12-board-appetite-phase-2.md` |

---

## §8. Dependencies

### §8.1 External Dependencies

- **Mimi codec** (Kyutai) — primary Phase 2 dependency. CC-BY-4.0 (NC-AL-9 cleared in v0.2; commercial appliance distribution permitted with standard attribution). Phase 2 ship-gate attribution surfaces tracked in `docs/decisions/dr-al-3-mimi-licensing.md`.
- **PyTorch / ONNX Runtime / TensorRT** — neural inference runtime. PyTorch for prototyping, ONNX/TensorRT for production deployment on T3.
- **FFmpeg / libavcodec** — streaming audio I/O, format conversion, timing primitives. Already in receptionBOX stack via LiveKit.
- **Qwen3 base model family** — Qwen3-0.5B for Phase 1 predictor, Qwen3-4B for Phase 2 LLM (existing receptionBOX dependency).
- **whisper-stt** — existing receptionBOX dependency. Continues to run in parallel through all phases.

### §8.2 Internal Dependencies

- **receptionBOX v1 production stability** (NFR-R3 validated) — Phase 1 work begins after receptionBOX v1 is in production, not before.
- **Strix Halo benchmark data** — Phase 0 cannot meaningfully execute without representative T3 hardware.
- **Firm corpus availability** — Phase 1 predictor training requires a 90-day corpus from at least one partner firm. **Resolved in v0.2: Path A — signed data-sharing agreement landed 2026-05-07.** Partner identity, agreement terms, and corpus delivery mechanism tracked operationally in Heron Labs CRM. DEV-1053 (Phase 1 predictor training pipeline) prerequisite: read the signed agreement before training starts. See `docs/decisions/partner-corpus-path.md`.

### §8.3 Hardware Tier Targets

| Tier | Hardware | Phase 0 | Phase 1 | Phase 2 | Phase 3 |
|------|----------|---------|---------|---------|---------|
| T2 | Jetson Orin Nano (8GB) | ❌ Out of scope | ❌ Out of scope | ❌ Out of scope | ❌ Out of scope |
| T3 | Strix Halo (128GB unified) | ✅ Primary target | ✅ Primary target | ✅ Primary target | ✅ Primary target |
| T4+ | Future hardware tiers | — | — | Compatible | Compatible |

T2 is out of scope for the entire project. Voice agent workloads on 8GB unified memory are already at capacity for receptionBOX v1; adding the Audio Layer is not feasible. T2 voice support remains a v3+ research question and is not addressed here.

---

## §9. Risks

### §9.1 Technical Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Mimi license restricts commercial use | ~~High~~ → **Resolved** | NC-AL-9 cleared in v0.2 (CC-BY-4.0, standard attribution). NC-AL-10 contingency demoted to defensive-only follow-up. |
| Phase 2 LLM fine-tuning produces unstable behavior | High | Phase 0 spike validates basic feasibility before committing |
| Audio token guardrail problem turns out to be mandatory not optional | High | DR-AL-2 keeps ASR cascade in place specifically to avoid this; risk is if customer pressure forces all-token architecture later |
| Strix Halo VRAM is insufficient at 4 concurrent calls with Audio Layer active | Medium | Phase 0 measures this directly; phased rollout means we discover this before commercial commitment |
| FFmpeg/PyTorch streaming integration introduces unexpected latency | Medium | Profile early; have GStreamer as fallback abstraction |

### §9.2 Project Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Phase 2 is research-grade and team bandwidth is constrained (active UMB Group consulting contracts) | ~~High~~ → **Medium** | NC-AL-12 cleared in v0.2 with green-light + internal headcount + Dustin as owner. Risk now is execution-side — Phase 1 work must not stretch into Phase 2 staffing window. Option (b) external collaboration is the re-open lever if bandwidth pressure surfaces. |
| receptionBOX v1 ship pressure delays Phase 0 indefinitely | Medium | Phase 0 timebox is 2 weeks; can be slotted between receptionBOX milestones rather than blocking them |
| Phase 1 wins are real but small enough to not justify Phase 2 work | Medium | Honest evaluation at Phase 1 gate; willingness to ship Phase 1 and stop |
| Customer-legible value of "audio tokens" is hard to communicate vs "lower latency" | Low | Audio Layer is platform infrastructure; customer-facing claim is "your appliance is fast and gets faster" |

### §9.3 Strategic Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| End-to-end S2S models (Moshi, Hertz-dev, future) commoditize this architecture | Medium | Per-firm fine-tuning (Phase 3) is the durable differentiator; codec layer alone is not a moat |
| The asymmetry argument (single-tenant > cloud) weakens if cloud providers ship per-tenant fine-tuning | Low | The on-prem data sovereignty story is independent of latency; this risk affects only the latency narrative |
| Competing open-source projects ship a similar layer first | Low | First-mover advantage in this layer is small; the moat is the per-firm fine-tuning at Phase 3 |

---

## §10. Project Plan

### §10.1 Phase 0 — Prototype (Weeks 1-2)

**Goal:** Validate that the basic Mimi → adapter → small-LLM pipeline runs at acceptable latency on T3 hardware, and that an LLM can be made to produce coherent behavior conditioned on audio tokens.

**Deliverables:**
- Spike repository (200-500 lines) with documented setup
- Latency measurements for Mimi encode/decode on Strix Halo
- A 20-utterance qualitative evaluation of LLM behavior on audio tokens
- Go/no-go decision document for Phase 1

**Owner:** Dustin (with Claude pairing)

**Success criteria:** Mimi decode < 100ms/chunk on T3, LLM produces *any* coherent behavior on audio token input.

### §10.2 Phase 1 — Predictive-Delta ASR (Weeks 3-12)

**Gate:** Phase 0 success criteria met. receptionBOX v1 production-stable.

**Deliverables:**
- Predictor training pipeline (consumes firm corpus, produces prediction model)
- Delta processor integration into receptionBOX agent-worker
- A/B harness for measuring latency improvement on production calls
- Production deployment to first partner firm
- Phase 1 evaluation document

**Owner:** receptionBOX engineering team + Audio Layer specialist (TBD)

### §10.3 Phase 2 — Audio Codec Layer (Weeks 13-26)

**Gate:** Phase 1 success criteria met. NC-AL-9 (Mimi licensing) and NC-AL-12 (board appetite) resolved.

**Deliverables:**
- Mimi integration into receptionBOX
- Adapter training (audio tokens → Qwen3-4B input)
- Parallel ASR + codec pipeline
- Token-aware transcript persistence
- Phase 2 evaluation document

**Owner:** **Dustin** (internal headcount path; staffing path (a) per `docs/decisions/nc-al-12-board-appetite-phase-2.md`). Revisit ownership at Phase 2 mid-point if scope warrants delegation. Option (b) external research collaboration remains a re-open lever without re-litigating green-light if Phase 1 bandwidth pressure surfaces.

### §10.4 Phase 3 — Per-Firm Fine-Tuning (Weeks 27+)

**Gate:** Phase 2 in production for ≥ 60 days with stable behavior.

**Deliverables:** Architecture refined based on Phase 2 outcomes. Detailed plan deferred.

---

## §11. Decision Records

### §11.1 Adopted DRs

- **DR-AL-1:** Audio Layer is platform infrastructure, not a personality pack. *Adopted on PRD acceptance.*
- **DR-AL-2:** ASR cascade remains in place through all phases; guardrails operate on text. *Adopted on PRD acceptance.*
- **DR-AL-3:** Mimi as Phase 2 codec target. *Adopted v0.2 (2026-05-07) per CC-BY-4.0 clean approval. NC-AL-3 latency validation on Strix Halo remains the Phase 0 gate.*
- **DR-AL-4:** receptionBOX is the first and only Phase 1/2 consumer. *Adopted on PRD acceptance.*
- **DR-AL-5:** Phase 0 is a 2-week timeboxed prototype with binary go/no-go. *Adopted on PRD acceptance.*
- **DR-AL-6:** FFmpeg/libavcodec patterns inform timing layer; FFmpeg is not the neural runtime. *Adopted on PRD acceptance.*

### §11.2 Candidate DRs (gated)

*None as of v0.2.* DR-AL-3 was promoted from candidate to adopted in v0.2.

---

## §12. Cross-References and Inheritance

### §12.1 Inherited from parent thUMBox technical PRD v2.1

| Parent section | Behavior |
|----------------|----------|
| §6 Personality Pack Architecture | Audio Layer is consumed by packs but is not a pack itself |
| §8 Security & Data Architecture | Inherited; audio token persistence adds new schema (FR-AL-12) |
| §5.6 Update Mechanism | Inherited; codec hot-swap follows drain-before-restart (receptionBOX §5.6) |

### §12.2 Companion documents

| Document | Relationship |
|----------|-------------|
| `receptionbox-technical-prd-v0_2-2026-05-06.md` | Primary consumer of Audio Layer features |
| `addendum-receptionbox-latency-unconventional-v0_1-2026-05-06.md` (RBOX repo) | Enumerates three latency paths for receptionBOX (Path A — forked speculative S2S drafting; Path B — exemplar-cache-as-default; Path C — watershed routing at SIP edge). The thUMBox Audio Layer is the **graduated platform-layer realization** of what would have been "Path E" in the addendum's framing — the codec-as-LLM-input bet. Because Audio Layer is a platform capability rather than a path internal to receptionBOX, the long-term documentation home is this PRD; the addendum (when next revised) should reference Audio Layer as an external dependency rather than restating its scope. A Path E pointer patch is staged in `docs/decisions/receptionbox-path-e-reconciliation.md` for application to the addendum's home repo. |
| Phase 0 spike repository (TBD) | Authoritative source on basic feasibility findings |

### §12.3 Authority hierarchy

1. Parent thUMBox technical PRD v2.1 (platform-level)
2. This Audio Layer PRD v0.1 (platform capability layer)
3. Consuming pack PRDs (receptionBOX, future voice packs) — pack PRDs reference Audio Layer features but do not redefine them
4. Phase deliverable documents (Phase 0 evaluation, Phase 1 evaluation, etc.)

---

## §13. Open Items for Review

### §13.1 Resolved in v0.2

1. ✅ **Naming.** Final: **thUMBox Audio Layer**. Alternatives ruled out (§1.4).
2. ⏳ **Scope.** Three-phase decomposition retained. Phase 2 / Phase 3 not split into a separate PRD; gates between phases enforce honest evaluation. Item remains open for Phase 1 closure review.
3. ⏳ **Hardware tier.** T3-only retained. T2 voice support remains a v3+ research question. Item remains open for strategic review when T2 hardware questions arise (not currently active).
4. ✅ **Bandwidth.** Phase 2 staffing path = (a) internal headcount, owner = Dustin. Option (b) external collaboration remains as a re-open lever. (`docs/decisions/nc-al-12-board-appetite-phase-2.md`)
5. ✅ **Mimi licensing.** Mimi is CC-BY-4.0; commercial appliance distribution permitted with standard attribution. (`docs/decisions/dr-al-3-mimi-licensing.md`)
6. ✅ **Predictor corpus.** Path A — signed data-sharing agreement landed 2026-05-07. Details in Heron Labs CRM. (`docs/decisions/partner-corpus-path.md`)
7. ✅ **Path E framing.** Audio Layer treated as graduated platform-layer project; cross-repo Path E pointer patch staged for the receptionBOX addendum. (`docs/decisions/receptionbox-path-e-reconciliation.md`)

### §13.2 Still Open

- **Item #2 (Scope).** Carried forward as a check at Phase 1 closure: if Phase 1 alone delivers the latency win and Phase 2's incremental value looks marginal, reconsider whether to split Phases 2/3 into a separate PRD or simply ship Phase 1 and stop. PRD §14.1 honest-uncertainty framing applies.
- **Item #3 (Hardware tier T2 strategic priority).** Not active. Open as a flag if customer demand for T2 voice support surfaces.

---

## §14. Honest Uncertainty

A required section. Where I am genuinely uncertain about this proposal:

1. **The customer-legible value of this layer is mostly indirect.** Customers don't ask for "audio tokens"; they ask for "fast voice." If Phase 1 alone delivers the latency win, Phases 2 and 3 may be unjustifiable on commercial grounds even if technically successful.

2. **The asymmetry argument is real but not unique.** Per-firm fine-tuning works for any LLM, not just audio codecs. Phase 3's differentiation depends on whether per-firm codec fine-tuning specifically (not just general per-firm fine-tuning) produces effects customers can perceive.

3. **The Phase 2 research bet is genuinely speculative.** No published voice agent ships this architecture. The closest analog (Moshi) couples codec and LLM tightly in a way the cascade-with-codec-input architecture does not. We may discover during Phase 2 that the decoupling fundamentally doesn't work, and end up either (a) shipping an end-to-end S2S model anyway, or (b) abandoning Phase 2.

4. **Bandwidth is real.** UMB Group's active consulting contracts and the receptionBOX Phase 1 work will absorb most engineering capacity through 2026. Phase 2 is a serious resource commitment that this PRD does not yet have a clear staffing answer for.

5. **The strongest version of this idea may be a research collaboration.** A university lab or a small AI research org might be the right partner for Phase 2 rather than internal engineering. This is worth considering before committing to internal headcount.

6. **The codec-as-input idea may already be obsolete by the time Phase 2 ships.** The S2S model field is moving fast. Hertz-dev, Moshi, and successors may collapse the cascade entirely. The Audio Layer's bet is that the cascade-with-better-input architecture remains viable; this is not a sure bet.

---

## §15. Phase 1 (M0) Closure Log

The Phase 1 (M0 / GSD Phase 1) coordination phase produced six decision documents and resolved five PRD §13 open items. Captured here for v0.2 audit completeness:

| Linear | Decision Doc | Outcome |
|--------|--------------|---------|
| DEV-1037 | n/a (informational) | PRD v0.1 baseline acknowledged; v0.2 (this document) is the next deliverable |
| DEV-1038 | `docs/decisions/naming-decision.md` | Naming: kept "thUMBox Audio Layer" |
| DEV-1039 | `docs/decisions/dr-al-3-mimi-licensing.md` | NC-AL-9 cleared; DR-AL-3 adopted |
| DEV-1040 | `docs/decisions/nc-al-12-board-appetite-phase-2.md` | NC-AL-12 cleared; Phase 2 green-light; Dustin owner |
| DEV-1041 | `docs/decisions/nc-al-6-audio-token-storage-legal.md` | NC-AL-6 cleared; FR-AL-12 ship-gate clear |
| DEV-1042 | `docs/decisions/partner-corpus-path.md` | Partner corpus Path A; signed agreement |
| DEV-1043 | `docs/decisions/receptionbox-path-e-reconciliation.md` | Strategy 2 + cross-repo patch staged |
| DEV-1044 | This v0.2 promotion | Phase 1 complete |

Phase 1 / M0 ran 2026-05-07 with all 6 decision gates closed in a single session and zero subagent invocations beyond planning. Phase 2 (M1 — Mimi feasibility spike) is now the next active milestone.

---

**END OF PRD v0.2**

v0.2 is **Accepted** scope. v0.1 is preserved as a historical baseline at `docs/audiolayer-technical-prd-v0_1-2026-05-07.md`. The next planned PRD revision is v0.3, expected after Phase 0 spike completion (Phase 0 evaluation document will surface scope-impacting findings).
