# Held-out generalization protocol (not yet executed)

Do not label a new structure benchmark as independent if its cases were generated from the existing verifier's rule templates. The domain team must create and freeze cases before seeing SciGeoGuard predictions.

1. Specify new workflow structures, products, and fault combinations that are absent from the v3/v11 rule-development suite.
2. Keep a private case-to-truth mapping. The runnable prediction file should contain only neutral case IDs plus workflow inputs.
3. Obtain two independent geospatial reviewers' labels and a third adjudication for disagreements.
4. Freeze manifest, case family, product/version, evidence supplied to reviewers, split, and hashes before running any system.
5. Run the full verifier, three baselines, and ablations without changing rules. Make changes only in a later version and evaluate on a new untouched split.
6. Report per-family confusion, false certification, abstention, applicability, diagnostics, and grouped uncertainty intervals. Resample at workflow-family level where possible.
7. Store original predictions before opening the mapping. Preserve disagreements and all deviations in a log.

Required cases should include novel workflow graphs and multiple interacting faults rather than just parameter mutations of known templates. Results are blocked until independent cases and labels exist.
