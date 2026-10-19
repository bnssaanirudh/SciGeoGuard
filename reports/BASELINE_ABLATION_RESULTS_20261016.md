# Baseline and ablation pilot results — 2026-10-16

These results use the frozen 180-case subset and the repository's generated reference. The baseline prediction runner reads a strict allowlist and does not load expected labels. Scoring occurs in a separate script after predictions are written. These results are a pilot of narrow conservative comparators; they are not a comprehensive comparison to mature GIS validators. All three comparators abstain on any case where their implemented checks do not find a supported violation, and they never return PROVEN. This design drives high abstention and means raw accuracy is not a balanced measure of system quality. No case-independent confidence interval is reported because cases may share workflow templates.

## Conservative baselines

| System | Accuracy | Refuted recall | Abstention | Applicable cases |
|---|---:|---:|---:|---:|
| metadata_only | 0.222 | 0.321 | 0.800 | 1.000 |
| provenance_aware | 0.094 | 0.134 | 0.906 | 1.000 |
| quantity_unit_aware | 0.117 | 0.152 | 0.906 | 0.183 |

False certification was 0 for all three on this reference, partly by construction because the baselines never issue PROVEN. The descriptive result should be read together with per-class recall, applicability and abstention in the adjacent JSON metrics.

## Ablations

| System | Accuracy vs generated reference | Refuted recall | False certification |
|---|---:|---:|---:|
| full_v11 | 1.000 | 1.000 | 0.000 |
| no_intent_conditioning | 0.972 | 0.964 | 0.034 |
| no_repair | 1.000 | 1.000 | 0.000 |


The intent-disabled ablation loses exact agreement on 5 of 180 cases (3.4 percentage points); this is a descriptive difference on a generated reference, not evidence of scientific validity. Repair/no-repair have identical verdict metrics because the frozen target is the pre-repair verifier verdict; the repair effect must be evaluated through separate repair outcomes (coverage/cost/correctness), not classification accuracy.

Raw outputs: `experiments/baselines/results_20261016/` and `experiments/ablations/results_20261016/`.
