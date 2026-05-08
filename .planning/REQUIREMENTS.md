# Requirements

Derived from PRD v0.1 §4 (Functional) and §5 (Non-Functional). All requirements are **hypotheses** until shipped and measured against PRD §6 success metrics. PRD-defined IDs (FR-AL-N, NFR-AL-N) are preserved as REQ-IDs.

## v1 Requirements

### M0 — Pre-Phase-0 (GSD Phase 1)

No functional requirements. Exit criteria are coordination outcomes captured in Linear DEV-1037 through DEV-1044:

- Naming finalized
- NC-AL-9 (Mimi licensing) resolved
- NC-AL-12 (board appetite) resolved
- NC-AL-6 (legal position on token storage) resolved
- Partner firm 90-day corpus path identified
- receptionBOX Path E framing reconciled
- PRD v0.1 → v0.2 promoted

### Phase 0 — Mimi Feasibility Spike (GSD Phase 2)

Binary go/no-go gate. No FRs ship; success/kill signals only.

- [ ] **SM-AL-1**: Phase 0 prototype runs Mimi decode at < 100ms per chunk on T3 (pass/fail; spike measurement)
- [ ] **SM-AL-2**: Phase 0 prototype demonstrates LLM produces *any* coherent behavior on audio tokens (pass/fail; manual eval, 20-utterance test set)
- [ ] **NC-AL-1**: VRAM footprint of Mimi + Whisper + Qwen3-4B + adapter on Strix Halo at 4 concurrent calls measured (open question resolved)

### Phase 1 — Predictive-Delta ASR (GSD Phase 3)

- [ ] **FR-AL-1**: Audio Layer exposes `predictor.predict(context) → predicted_utterance` interface to the agent-worker
- [ ] **FR-AL-2**: Predictor consumes call context (ANI, time-of-day, conversation history, partial transcript) and emits prediction + confidence score
- [ ] **FR-AL-3**: Delta processor aligns streaming partial ASR output against the prediction and emits committed-text events for matched regions
- [ ] **FR-AL-4**: Predictor confidence below threshold T falls through to standard ASR cascade with no behavioral change
- [ ] **FR-AL-5**: Agent-worker can disable Phase 1 features per-firm or per-call via configuration flag
- [ ] **FR-AL-6**: Predictor inference latency p90 ≤ 50ms on T3 hardware
- [ ] **FR-AL-7**: Predictor retrainable from updated firm corpus weekly, with hot-swap on next call boundary
- [ ] **NFR-AL-1**: Phase 1 predictor inference p90 latency on T3 ≤ 50ms
- [ ] **NFR-AL-2**: Phase 1 end-to-end latency improvement over receptionBOX v1 ≥ 100ms p90
- [ ] **NFR-AL-8**: Predictor accuracy on held-out firm corpus ≥ 60% utterance-level match
- [ ] **SM-AL-3**: p90 latency reduction on high-confidence prediction calls ≥ 100ms (production telemetry)
- [ ] **SM-AL-4**: Prediction high-confidence rate ≥ 40% of calls (production telemetry)

### Phase 2 — Audio Codec Layer (GSD Phase 4)

- [ ] **FR-AL-8**: Codec encoder consumes 16kHz PCM and emits Mimi-compatible audio tokens at 12.5Hz
- [ ] **FR-AL-9**: Adapter maps audio tokens into LLM-consumable representation via fine-tuned input embedding
- [ ] **FR-AL-10**: ASR cascade continues to run in parallel for guardrail and audit purposes
- [ ] **FR-AL-11**: Guardrail filter operates on text from the ASR cascade; token-based guardrails out of scope for v1
- [ ] **FR-AL-12**: Persisted transcripts include both text (ASR) and audio token sequences (codec) for audit completeness
- [ ] **FR-AL-13**: Codec encoder/decoder hot-swappable across appliance restarts
- [ ] **FR-AL-14**: Agent-worker can disable Phase 2 features per-firm or per-call via configuration flag
- [ ] **NFR-AL-3**: Phase 2 codec encode latency on T3 ≤ 30ms per 80ms audio chunk
- [ ] **NFR-AL-4**: Phase 2 end-to-end latency improvement over Phase 1 baseline ≥ 200ms p90
- [ ] **NFR-AL-5**: Memory overhead of Audio Layer on T3 (predictor + codec + adapter resident) ≤ 8GB VRAM
- [ ] **SM-AL-5**: Phase 2 p90 latency reduction over Phase 1 baseline ≥ 200ms (production telemetry)
- [ ] **SM-AL-6**: Phase 2 token-stream commit-to-LLM latency ≤ 50ms p90 (production telemetry)

### Phase 3 — Per-Firm Codec Fine-Tuning (GSD Phase 5)

Provisional — refined based on Phase 2 outcomes.

- [ ] **FR-AL-15**: Codec architecture supports base encoder + firm-specific head
- [ ] **FR-AL-16**: Firm-specific head training happens on-appliance; no audio leaves the firm
- [ ] **FR-AL-17**: Firm-specific heads invalidatable on persona change, voice clone update, or explicit firm request
- [ ] **NFR-AL-7**: Phase 3 firm-specific head training time on T3 (90-day corpus) ≤ 24 hours
- [ ] **SM-AL-7**: Phase 3 compression ratio improvement on firm-specific patterns ≥ 30% (synthetic benchmark)

### Cross-Phase Invariants (apply to GSD Phases 3-5)

- [ ] **NFR-AL-6**: Audio Layer disabled state shall add ≤ 5ms overhead to standard cascade (all phases)
- [ ] **NFR-AL-9**: No degradation in intent classification accuracy vs receptionBOX v1 baseline (all phases)
- [ ] **NFR-AL-10**: No degradation in guardrail recall vs receptionBOX v1 baseline (all phases)
- [ ] **SM-AL-8**: All phases: intent classification accuracy delta vs v1 baseline ≥ 0% (no regression; daily eval)
- [ ] **SM-AL-9**: All phases: guardrail recall delta vs v1 baseline ≥ 0% (no regression; daily eval against guardrail test suite)

## v2 Requirements

Deferred — surfaced after Phase 2 ships.

- Token-based guardrails (FR-AL-11 explicitly defers this)
- Audio Layer for non-receptionBOX voice packs (DR-AL-4 limits Phase 1/2 to receptionBOX)
- T2 (Jetson Orin Nano 8GB) voice support

## Out of Scope

- TTS pipeline changes — covered in receptionBOX PRD §5.3
- SIP edge / carrier integration — covered in receptionBOX PRD §4.2
- Personality pack contract changes — Audio Layer is consumed by packs, not a pack
- Multi-modal extensions (vision, video) — audio only
- Replacing the ASR pipeline entirely — Audio Layer runs *alongside* ASR through Phase 2 (DR-AL-2)
- End-to-end S2S model integration (e.g., Moshi-style coupled codec/LLM) — explicit architectural divergence

## Open Questions (NC-AL-N)

These block phase progression. Tracked in Linear; surfaced here for traceability.

| ID | Question | Blocks | Linear |
|----|----------|--------|--------|
| NC-AL-1 | Mimi + Whisper + Qwen3-4B + adapter VRAM at 4 concurrent on Strix Halo | Phase 1 go/no-go | DEV-1049 |
| NC-AL-2 | Pipecat / LiveKit Agents native parallel-stream support | Phase 1 scoping | DEV-1050 |
| NC-AL-3 | Mimi acceptable latency on Strix Halo or smaller codec needed | Phase 0 prototype | DEV-1048 |
| NC-AL-4 | Minimum LLM size for audio-token consumption | Phase 2 scoping | DEV-1069 |
| NC-AL-5 | Adapter trainable on generic corpus or per-firm required | Phase 2 scoping | DEV-1068 |
| NC-AL-6 | Legal position on storing audio tokens alongside transcripts | Phase 2 ship gate | DEV-1041 |
| NC-AL-7 | Audio-token prompt-injection threat model | Phase 2 ship gate | DEV-1067 |
| NC-AL-8 | Privacy-preserving training defensibility | Phase 3 ship gate | DEV-1074 |
| NC-AL-9 | Mimi (Kyutai) commercial licensing | Phase 2 ship gate | DEV-1039 |
| NC-AL-10 | Codec contingency if Mimi licensing fails | Phase 2 contingency | DEV-1070 |
| NC-AL-11 | FFmpeg/libavcodec ↔ PyTorch streaming integration | Phase 1 implementation | DEV-1051 |
| NC-AL-12 | Board / team appetite for Phase 2 commitment | Project go/no-go | DEV-1040 |

## Traceability

Maintained in `.planning/ROADMAP.md` (phase → REQ-ID mapping) and Linear (issue → FR/NC/SM IDs in description).
