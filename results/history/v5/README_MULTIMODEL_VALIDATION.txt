
SciGeoGuard-X Multi-Model Blind Validation v5
=============================================

Frozen verifier:
{
  "frozen_at_utc": "2026-10-02T08:19:38.747739+00:00",
  "verifier_version": "SciGeoGuard-X-v3",
  "v3_notebook": "/mnt/data/SciGeoGuard_X_Publication_Experiments_v3.ipynb",
  "v3_results_zip": "/mnt/data/SciGeoGuard_X_v3_All_Results.zip",
  "v3_notebook_sha256": "afdb1ad9c2cb8742b3d26638067e80fb8619afd6aa019a58769e5acbdc2c15d2",
  "v3_results_zip_sha256": "8cb3f200453e8018f5afd0ce3c95130f6efdee4733f819727b5b16fc159ef992",
  "freeze_status": "VERIFIER_NOTEBOOK_HASHED"
}

Judge models:
A = Qwen/Qwen2.5-1.5B-Instruct
B = microsoft/Phi-3.5-mini-instruct
C = HuggingFaceTB/SmolLM2-1.7B-Instruct

Protocol:
- A and B independently evaluate the same blinded workflows.
- They see no generated label or SciGeoGuard-X output.
- C runs only when A/B disagree or parsing fails.
- C does not see A/B decisions.
- Consensus requires a majority.
- No-majority cases remain UNRESOLVED.
- Multi-model consensus is NOT described as human expert ground truth.
- A targeted blind human-audit CSV is exported separately.

Recommended manuscript terminology:
1. generated stress-test reference;
2. frozen SciGeoGuard-X output;
3. independent LLM Judge A;
4. independent LLM Judge B;
5. blind three-model consensus;
6. targeted human audit.

RUN_MODELS = True
Created UTC = 2026-10-02T09:03:39.025779+00:00
