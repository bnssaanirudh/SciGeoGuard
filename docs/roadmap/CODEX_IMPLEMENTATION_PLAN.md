# Codex implementation plan

## Completed in this branch

1. Extract frozen v3 verifier into `src/scigeoguard_core.py` without intended rule changes.
2. Route quickstart and v11 imports through module; add package metadata.
3. Add deterministic regression tests and Python 3.10/3.12 CI configuration.
4. Document evidence mapping, reproducibility gaps, and validity threats.
5. Implement label-isolated conservative metadata, quantity/unit, and provenance baselines plus separate scoring.
6. Implement no-intent and no-repair ablations; run both on the 180-case frozen subset.
7. Add a pinned Colab CPU notebook that packages pilot outputs and environment metadata.

## Next phases

### A. Provenance and release integrity
- Add parity tests comparing package output with frozen notebook source on public fixtures.
- Pin tested experiment environments separately from minimal core runtime.
- Add CI wheel build, fresh virtualenv install, import, tests, quickstart, and source hashes.

### B. Fair baselines
- Pilot metadata-only, quantity/unit-aware, and provenance-aware validators; expand their narrow rules and validate applicability against domain-reviewed cases.
- Implemented intent-conditioning and repair ablations; add complementary repair outcome metrics.
- Prediction runners use allowlisted inputs and separate scoring; extend leakage checks and assess all outputs against independent labels.

### C. Evaluation harness
- Emit per-case predictions, confusion matrices, per-class recall, false certification, abstention, diagnostic coverage, grouped intervals, manifests, and failures.
- Preserve frozen outputs; write reruns to timestamped/commit-addressed folders.

### D. Repair and generalization
- Evaluate correctness independently of self-reverification.
- Analyze multi-fault, multi-edit, refusal, unsafe proposal, and unrepairable cases.
- Freeze unseen workflow structures before comparative evaluation.

### E. Manuscript release
- Generate reported values from verified artifacts where possible.
- Label evidence as generated-reference, author-controlled, external data counterfactual, or independent human review.
- Check article category, references, figures, supplement, and journal rules before submission.

## Blocked external inputs

Independent domain reviewers and fresh Colab/live-data experiments require the research team. This branch does not fabricate those outputs.
