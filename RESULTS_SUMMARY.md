# Final results summary

## Scientific status

**Core experimental evidence: READY for the FCS Code & Data note.** The v9.1 science gates passed, and the v11 verification-and-repair extension has been rerun independently in Colab with byte-identical structured outputs.

### v3 controlled benchmark
- 445 cases: 145 PROVEN, 278 REFUTED, 22 UNPROVEN.
- Generated scientific-invariant reference; **not independent human ground truth**.
- The 445/445 match is treated as regression consistency, not an external accuracy estimate.

### v6 strong 7B LLM baselines
- Strong Qwen2.5-7B: accuracy 44.44%, FSCR 69.64%.
- Strong Mistral-7B: accuracy 38.33%, FSCR 69.64%.
- The LLMs are comparison baselines, not scientific adjudicators.

### Live Earth-observation counterfactuals
- Sentinel-2: regional median spectral-role MAE 0.0977.
- ESA WorldCover: median bilinear invalid-class fraction 12.99%; nearest-neighbour preserved valid class codes.
- Copernicus DEM GLO-30: 3x per axis creates 9x cells; 88.89% of fine-grid positions do not correspond to distinct source samples; corrected regional-median core p95 round-trip error 1.3998 m.
- GPM IMERG V07: 4/4 rainy regions reproduced the deterministic 2.0x overstatement when the 0.5 h duration is omitted.

### v11 EarthRefine / conservative repair
- 10/10 controlled semantic mutations detected.
- 9/10 mutation families received a safe one-edit repair.
- 9/9 found metamorphic repairs re-verified as PROVEN.
- Frozen 180-case reference agreement: 180/180 (regression consistency only).
- 112 workflows were REFUTED; 47/112 (41.96%) received a conservative one-edit repair.
- 47/47 repaired frozen workflows re-verified as PROVEN.
- Mean successful repair cost: 1 edit.
- Findings span 18 refinement-obligation families and 23 diagnostic codes.
- Unsafe repairs are refused; e.g., a vertical-datum mismatch is not 'fixed' by changing a metadata label.
- A fresh Colab rerun reproduced all seven structured v11 outputs byte-for-byte by SHA-256.

### Independent human validation
**Pending.** Blinded reviewer materials have been prepared, but completed independent reviewer verdicts are not available. Do not claim human-validated system accuracy or Cohen's kappa.

## Evidence boundary

The benchmark labels and v11 metamorphic mutations are generated/author-controlled evidence. They support regression consistency, diagnostic coverage, repair behavior, and reproducibility; they do not substitute for independent human ground truth.