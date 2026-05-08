# Phase 0 Test Utterances

This directory holds 3-5 short test WAV files used by the Mimi encode/decode roundtrip spike (Plan 02-01 Task 4) and the decode-latency benchmark (Plan 02-02 Task 1).

## Hard constraints (no exceptions)

1. **No real client audio.** Per PRD §8.3 and operator CLAUDE.md "no client audio" rule. Phase 0 uses synthetic or open-licensed audio only.
2. **Format:** 16 kHz mono PCM WAV at the source. The spike resamples to 24 kHz internally for Mimi (Mimi's native sample rate).
3. **Length:** 3-10 seconds per utterance. Short enough to iterate quickly; long enough to exercise streaming token generation.
4. **Count:** 3-5 utterances minimum. The full LLM-on-tokens stretch (Plan 02-04) uses a separate, larger 20-utterance corpus at `spike/assets/llm-eval/`.

## Acceptable sources

| Source | Status | Notes |
|--------|--------|-------|
| **Mozilla CommonVoice** (English short clips) | Recommended | Pinned clip IDs + SHA256 verification preferred for reproducibility |
| **TTS synthesis** (Kokoro-82M ONNX, Chatterbox-Turbo, etc.) | Recommended | Deterministic regeneration is a feature; record TTS config + seed |
| **LibriSpeech** (open-licensed) | Acceptable | Larger corpus; pick short utterances; cite license in this README |
| **Synthetic noise / silence** | Acceptable for smoke tests | Useful for verifying the pipeline doesn't crash on edge inputs |
| **Real client / receptionBOX call recordings** | **FORBIDDEN** | Privilege exposure; never use these |

## Reproducibility

If using TTS synthesis: commit a `generate_test_utterances.sh` script that regenerates the audio deterministically (fixed seed, pinned model SHA, fixed voice). Same pattern as `spike/assets/llm-eval/` per Plan 02-04.

If using CommonVoice: commit `SHA256SUMS` so a clean checkout can verify byte-identical files.

## Linkage

- Plan 02-01 Task 4 (Mimi encode/decode loop) — uses these utterances for end-to-end smoke test.
- Plan 02-02 Task 1 (decode latency benchmark) — uses these utterances as the input corpus for the 1000-chunk latency measurement.
