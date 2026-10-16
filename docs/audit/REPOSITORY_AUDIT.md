# Repository audit (2026-10-16)

## Scope

Reviewed public `main` at `0e74b70` (`origin/main`), root documentation, v11 source/results/archive, quickstart, requirements, v3 verifier notebook, release status, and pending v7 reviewer materials. Ran the original quickstart before changes. This is a source/artifact audit; historical notebooks, live EO downloads, and the Colab rerun were not executed here.

## Findings

1. Canonical v3 rules are in cells 6, 7, and 9 of `notebooks/history/v3_controlled_benchmark.ipynb`. Before this branch, the quickstart and v11 module extracted and executed notebook cells at runtime, coupling imports to notebook structure.
2. Frozen v3/v9.1 and v11 outputs, manifests, source notebooks, and explicit evidence limitations are present. The v11 archive contains structured CSV/JSON outputs and a manifest.
3. Independent validation is blocked: `validation/v7_pending/STATUS.md` says completed independent reviewer A/B verdicts are unavailable. The files are reviewer forms and internal selection/mapping material, not completed validation results.
4. Repair candidates are checked by the same verifier that proposes them. This shows consistency with encoded rules, not independent scientific correctness.
5. The result summaries report 445 generated-reference cases, v6 model baselines, live-product author-defined counterfactuals, and v11 repair statistics. The v11 notebook code cells were replayed in a fresh Python process and their assertions passed against committed inputs. This was not a Jupyter-kernel or Colab run. The v3 count, live-product experiments, and fresh Colab/hash claim remain unrerun here.
6. `requirements/core.txt` is a broad notebook environment. The extracted core module uses only Python's standard library.

## Changes made

Added `src/scigeoguard_core.py` as a static extraction of frozen notebook cells 6/7/9, routed quickstart and v11 imports through it, added package metadata, core and baseline regression tests, GitHub Actions configuration, label-isolated baseline/ablation runners, local pilot outputs, and the accompanying evidence/validity/roadmap documents. Built a wheel and installed it in a new virtual environment; core and v11 imports and a verifier smoke case passed.

## Assessment

The package/import reproducibility issue is locally addressed. CI has not yet run on GitHub; wheel build and clean virtual-environment install/import smoke passed locally. The v11 assertions passed in a local in-process replay, while full Colab and all other frozen experiments remain unverified until notebooks are run cleanly and outputs compared with committed hashes.
