
SciGeoGuard-X Strong Decomposed LLM Baselines v6
================================================

Baseline A:
Qwen/Qwen2.5-7B-Instruct

Baseline B:
mistralai/Mistral-7B-Instruct-v0.3

Important interpretation:
- These LLMs are scientific baselines, not ground truth.
- Their final verdict is derived deterministically from decomposed proof obligations.
- Generated v3 labels are used only as the existing controlled stress-test reference.
- Frozen SciGeoGuard-X remains separate.
- Human_Audit_BLIND.csv is the independent human-review target.

Main methodological change from v5.x:
The LLM no longer produces an opaque final verdict directly.
It must separately evaluate fixed scientific obligations.

Created UTC:
2026-10-02T16:38:30.952797+00:00
