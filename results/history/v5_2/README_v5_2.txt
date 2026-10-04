
SciGeoGuard-X Multi-Model Blind Validation v5.2
================================================

Judge A: Qwen/Qwen2.5-3B-Instruct
Judge B: microsoft/Phi-4-mini-instruct
Judge C: HuggingFaceTB/SmolLM3-3B

Major corrections in v5.2:
- Phi-3.5 replaced by Phi-4-mini.
- Judge models upgraded to approximately 3B–4B scale.
- Balanced 3-class calibration before blind evaluation.
- Explicit null-field semantics.
- Parse-success and verdict-collapse health gates.
- Failed judges are excluded from consensus.
- Judge C covers all test cases if A or B is unhealthy.
- Consensus requires at least two eligible model votes.
- Human audit remains the final correctness anchor.

Do NOT call multi-model consensus human expert ground truth.

Generated at UTC:
2026-10-02T10:46:27.703070+00:00
