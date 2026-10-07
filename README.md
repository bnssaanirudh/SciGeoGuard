# SciGeoGuard-X

**Evidence-Carrying Scientific Verification and Conservative Repair for Earth-Observation Workflows**

SciGeoGuard-X detects Earth-observation workflows that can execute successfully while violating the scientific meaning of the requested product or claim. It represents scientific intent, source/product semantics, provenance, units, spatial/temporal support, spectral roles, quality requirements, vertical semantics, leakage constraints, and uncertainty explicitly, then returns **PROVEN**, **REFUTED**, or **UNPROVEN** with auditable evidence.

The v11 EarthRefine layer adds named scientific refinement obligations, machine-readable evidence certificates, conservative minimal-repair synthesis, and re-verification. Unsafe edits that would invent scientific evidence are deliberately refused.

## Current scientific status

The v9.1 evidence freeze passed all core science gates. The confirmed v11 rerun extends that evidence with verification-and-repair experiments:

- 10/10 controlled semantic mutations detected.
- 9/10 mutation families received a safe one-edit repair.
- 9/9 found metamorphic repairs re-verified as **PROVEN**.
- Frozen 180-case reference agreement: 180/180 (regression consistency only).
- 47/112 **REFUTED** workflows received a conservative one-edit repair (41.96%).
- 47/47 repaired frozen workflows re-verified as **PROVEN**.
- Findings span 18 refinement-obligation families and 23 diagnostic codes.
- A fresh Colab rerun reproduced all seven structured v11 outputs byte-for-byte by SHA-256.

These are generated-reference and author-controlled metamorphic results, **not independent human accuracy estimates**.

See `RESULTS_SUMMARY.md`, `results/final/v11/README.md`, and `results/final/FINAL_EVIDENCE_TABLE.csv`.

## Quick start

For the original verifier:

```bash
python examples/quickstart.py
```

For the confirmed v11 repair experiment, open `notebooks/core/v11_earthrefine_repair_confirmed.ipynb`.

The reusable v11 repair layer is in `src/scigeoguard_v11.py`.

## Start here

- `examples/quickstart.py` - minimal executable verifier example.
- `src/scigeoguard_v11.py` - evidence certificates and conservative repair synthesis.
- `notebooks/core/v11_earthrefine_repair_confirmed.ipynb` - compact public v11 reproduction notebook.
- `notebooks/history/v3_controlled_benchmark.ipynb` - frozen 445-case controlled scientific-invariant benchmark.
- `notebooks/core/v6_strong_decomposed_llm_baselines.ipynb` - Qwen/Mistral 7B baseline evaluation.
- `notebooks/core/v8_multiregion_realworld_replication.ipynb` - live Sentinel/WorldCover/IMERG/CopDEM replication.
- `notebooks/core/v8_1_robustness_corrections.ipynb` - corrected IMERG/CopDEM methodology.
- `notebooks/core/v8_2_imerg_recovery.ipynb` - resilient four-region rainy IMERG recovery.
- `notebooks/final/v9_1_final_merge_and_freeze.ipynb` - final pre-v11 evidence merge.
- `results/final/scigeoguard_v11_results.zip` - confirmed v11 result archive.

## Evidence boundaries

1. v3 labels are a **controlled generated reference**, not independent human ground truth.
2. v11 metamorphic mutations are author-controlled scientific stress tests.
3. Repair success measures conservative repairability under the encoded rules, not real-world accuracy.
4. Qwen/Mistral outputs are baselines, not scientific adjudicators.
5. Live EO counterfactuals use real public products but author-defined semantic faults.
6. Independent human review remains pending; no human-validated accuracy or kappa is claimed.

## Reproduction

Typical CPU/Earth-observation environment:

```bash
pip install -r requirements/earth-observation.txt
```

For the v6 7B baselines, use a CUDA/T4-class runtime and:

```bash
pip install -r requirements/llm-baselines.txt
```

No paid inference API is required for the final verifier, v11 repair layer, or EO experiments.

## License

Code and repository-authored materials are released under the **Apache License 2.0**. Third-party datasets retain their original provider terms; see `DATA_SOURCES.md`.

## Citation

See `CITATION.cff`.