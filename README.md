# SciGeoGuard-X

**Proof-Carrying Scientific Verification for Earth-Observation Workflows**

SciGeoGuard-X is a research prototype for detecting *scientifically invalid but computationally executable* Earth-observation workflows. It represents scientific intent, source/product semantics, provenance, units, spatial/temporal support, quality requirements, and proof obligations explicitly, then returns **PROVEN**, **REFUTED**, or **UNPROVEN** with evidence and repair context.

## Final release status

The final v9.1 evidence merge passed all core science gates. The short FCS *Code & Data in Earth Science* evidence package is scientifically frozen. Independent v7 human review remains optional/pending and is not used to claim human-grounded system accuracy.

See [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md) and [`results/final/FINAL_EVIDENCE_TABLE.csv`](results/final/FINAL_EVIDENCE_TABLE.csv).

## Quick start

A minimal runnable example is available at [`examples/quickstart.py`](examples/quickstart.py). From the repository root:

```bash
python examples/quickstart.py
```

The example loads the frozen v3 verifier, constructs an `Artifact`, `Step`, and `Intent`, and demonstrates why bilinear interpolation of nominal land-cover classes is returned as **REFUTED** with evidence and a repair suggestion.

## Start here

- `examples/quickstart.py` — minimal executable verifier example.
- `notebooks/history/v3_controlled_benchmark.ipynb` — frozen controlled scientific-invariant benchmark.
- `notebooks/core/v6_strong_decomposed_llm_baselines.ipynb` — Qwen/Mistral 7B baseline evaluation on the blinded baseline set.
- `notebooks/core/v8_multiregion_realworld_replication.ipynb` — live Sentinel/WorldCover/IMERG/CopDEM replication.
- `notebooks/core/v8_1_robustness_corrections.ipynb` — corrected IMERG/CopDEM methodology.
- `notebooks/core/v8_2_imerg_recovery.ipynb` — resilient four-region rainy IMERG recovery.
- `notebooks/final/v9_1_final_merge_and_freeze.ipynb` — final evidence merge and freeze.

## Repository layout

```text
examples/       minimal runnable usage example
notebooks/
  core/          main scientific experiments
  final/         closure/merge notebooks
  history/       protocol and superseded experiment versions
  validation/    blinded human-validation notebook
results/
  final/         canonical v9.1 frozen evidence and publication assets
  history/       historical experiment outputs
validation/
  v7_pending/    blinded reviewer forms; no completed human labels
requirements/    reproducibility environments
```

## Evidence boundaries

1. v3 labels are a **controlled generated reference**, not independent human ground truth or an independent performance estimate.
2. Qwen/Mistral outputs are baselines, not scientific adjudication.
3. Live-data counterfactual labels encode explicit scientific rules; they are not human annotations.
4. v7 reviewer forms are pending. No human accuracy or Cohen's kappa is claimed.
5. Obsolete v9 closure figures/status files with missing earlier inputs are intentionally excluded; v9.1 is the canonical final merge.

## Reproduction

Typical CPU/Earth-observation environment:

```bash
pip install -r requirements/earth-observation.txt
```

For the v6 7B baselines, use a CUDA/T4-class runtime and:

```bash
pip install -r requirements/llm-baselines.txt
```

All Earth-observation data sources used in the notebooks are public; no paid inference API is required for the final verifier/EO experiments.

## License

Code and repository-authored materials are released under the **Apache License 2.0**. Third-party datasets retain their original provider terms; see [`DATA_SOURCES.md`](DATA_SOURCES.md). Before public release, confirm this licensing choice is compatible with any institutional/IP obligations that apply to the work.

## Citation

See [`CITATION.cff`](CITATION.cff).
