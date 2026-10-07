# SciGeoGuard-X v11 confirmed results

This folder documents the v11 EarthRefine experiment: named scientific refinement obligations, evidence certificates, conservative minimal repair, and re-verification.

## Confirmed rerun

A fresh Colab rerun supplied on 2026-10-07 reproduced all seven structured result outputs byte-for-byte by SHA-256.

- Metamorphic mutation families: 10
- Mutations detected: 10/10
- Safe repairs found: 9/10
- Found repairs re-verified PROVEN: 9/9
- Frozen 180-case reference agreement: 180/180
- REFUTED workflows in frozen subset: 112
- Conservative one-edit repairs: 47/112 = 41.96%
- Repaired frozen workflows re-verified PROVEN: 47/47
- Mean successful repair cost: 1 edit
- Obligation families observed: 18
- Diagnostic codes observed: 23

The vertical-datum mismatch is intentionally not automatically repaired: changing a datum label would not perform a scientifically valid coordinate transformation.

## Evidence boundary

These results use a generated scientific-invariant reference and author-controlled metamorphic mutations. They demonstrate regression consistency, counterexample generation, conservative repair behavior, and reproducibility. They are not independent human ground truth.

## Public artifacts

- `../../notebooks/core/v11_earthrefine_repair_confirmed.ipynb`
- `../../src/scigeoguard_v11.py`
- `../scigeoguard_v11_results.zip`
