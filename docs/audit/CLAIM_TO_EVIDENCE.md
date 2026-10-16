# Claim-to-evidence map

**VERIFIED** = checked directly in this audit/local tests; **REPORTED_NOT_REPRODUCED** = repository reports it but this audit did not rerun it; **UNSUPPORTED** = insufficient evidence in reviewed artifacts; **CONTRADICTED** = reviewed evidence conflicts with the claim.

| Claim | Evidence | Status | Boundary |
|---|---|---|---|
| Encoded verifier flags bilinear interpolation of nominal land-cover classes | v3 notebook cells 6/7/9; quickstart | VERIFIED (local regression) | Tests encoded rule only |
| v3 benchmark has 445 cases (145 PROVEN, 278 REFUTED, 22 UNPROVEN) | `RESULTS_SUMMARY.md`; `results/history/v3/`; final evidence table | REPORTED_NOT_REPRODUCED | Generated reference, not independent truth |
| v11 detects 10/10 mutations; 9/10 safe repairs; 9/9 found metamorphic repairs re-verified | `results/final/v11/README.md`; result ZIP | VERIFIED (local in-process replay) | Author-controlled suite |
| v11 frozen 180-case agreement is 180/180 | Same v11 evidence | VERIFIED (local in-process replay) | Generated-reference regression consistency only |
| v11 repairs 47/112 refuted cases and re-verifies 47/47 | Same v11 evidence | VERIFIED (local in-process replay) | Self-reverification is not independent repair correctness |
| Colab rerun byte-matched seven outputs | v11 README/manifest | UNSUPPORTED as a fresh Colab claim in this audit | Local in-process replay passed; Colab not run |
| Independent human accuracy, adjudicated labels, or kappa established | `validation/v7_pending/STATUS.md` | CONTRADICTED | Repository explicitly says verdicts unavailable |
| Scientifically more accurate than conventional validators | No comparable conventional baseline in reviewed release | UNSUPPORTED | LLM comparisons do not establish this |
| All frozen notebooks reproduce from clean checkout | Not run end-to-end | UNSUPPORTED | Local smoke tests do not cover network/GPU/data workflows |
| Core imports without notebook execution | package metadata, module, tests | VERIFIED (local) | Editable install/import smoke passed |

| Built wheel installs and core/v11 imports in a clean virtual environment | Local wheel build and fresh-venv smoke test | VERIFIED (local) | Does not show GitHub CI pass yet |
