# Experiment matrix — SciGeoGuard-X current evidence

| Workstream | Evidence/status | Interpretation / next gate |
|---|---|---|
| v3 controlled benchmark | **Reproduced locally**: 445-case count is reported in repository; v11's frozen 180-case subset replayed with 180/180 agreement | Generated reference; not human-grounded accuracy |
| v11 metamorphic checks | **Reproduced locally**: 10/10 detected, 9/10 repaired, 9/9 found repairs re-verified | Author-controlled stress suite |
| v11 frozen subset repair | **Reproduced locally**: 112 refuted, 47 repaired (41.96%), 47/47 re-verified; 18 obligation families, 23 codes | Re-verification uses same verifier; not independent scientific validation |
| Fresh Colab rerun/hash identity | Reported by repository for 2026-10-07; **not independently repeated here** | Run in Colab and compare outputs |
| Independent expert validation | **BLOCKED / pending** | Reviewer forms exist; no completed independent verdicts |
| Conventional scientific baselines | **NOT IMPLEMENTED in reviewed branch** | Implement metadata, quantity/unit, provenance baselines fairly |
| Ablations | **NOT IMPLEMENTED in reviewed branch** | Intent conditioning and repair ablations |
| Robustness combinations | Partial author-controlled mutations only | Add missing/contradictory metadata, multi-fault and combination cases |
| Repair correctness | Self-reverification only | Independent correctness assessment required |
| New-structure generalization | **NOT RUN** | Freeze separately specified benchmark before test |
| Live EO experiments | Reported in archived results; not rerun in this pass | Reproduce separately with pinned data/product versions |

Local replay details and per-case records: `reports/reproduction_20261016/`. It executed notebook code cells in a fresh Python process, not a Jupyter kernel or Colab; the local Jupyter kernel could not initialize because socket setup is blocked in this execution environment.
