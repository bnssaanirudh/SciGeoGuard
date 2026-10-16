# Baseline experiment

`run_baselines.py` reads only a fixed allowlist of case input columns and never opens the reference labels. The three comparators make narrow checks: metadata consistency, selected unit/quantity semantics, and source provenance. They return `REFUTED` only for explicit supported violations; otherwise they abstain as `UNPROVEN`. They never return `PROVEN`, so their accuracy must be interpreted alongside abstention and applicability.

`score_predictions.py` is a separate process for scoring already-written predictions against the generated frozen reference. This preserves the prediction/target boundary in the baseline implementation. Current generated-reference scores are descriptive; the targets are not independent scientific truth. The current baseline coverage is deliberately incomplete and should not be described as a comprehensive state-of-the-art comparison.

Run the pinned CPU Colab notebook `SciGeoGuard_Baseline_Ablation_Pilot.ipynb` for a clean-runtime run that records environment metadata and downloads a ZIP. The notebook pins the commit containing the runners.

Reproduce locally:

```bash
python experiments/baselines/run_baselines.py --cases results/history/v6/Blinded_180_cases.csv --out experiments/baselines/results/predictions.csv
python experiments/baselines/score_predictions.py --predictions experiments/baselines/results/predictions.csv --reference results/history/v6/Frozen_v3_reference.csv --out experiments/baselines/results/metrics.json
```

The dated results in `results_20261016/` are a local author-controlled benchmark comparison.
