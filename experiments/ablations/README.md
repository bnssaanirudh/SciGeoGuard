# Ablations

`run_ablations.py` runs the full v11 system, a verification-only variant with repair disabled, and an intent-disabled variant on the same input cases. The intent-disabled system receives an empty `Intent`; this removes explicit intent constraints but leaves workflow metadata and verifier rules in place. Prediction code has no reference-label input. Score the output separately with `experiments/baselines/score_predictions.py`.
