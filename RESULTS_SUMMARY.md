# Final results summary

## Scientific status

**Core experimental evidence: READY.** All final v9.1 science gates passed.

### v3 controlled benchmark
- 445 cases
- 145 PROVEN
- 278 REFUTED
- 22 UNPROVEN
- Controlled/generated scientific-invariant reference; **not independent human ground truth**.

### v6 strong 7B LLM baselines
- Strong Qwen2.5-7B: accuracy 44.44%, FSCR 69.64%
- Strong Mistral-7B: accuracy 38.33%, FSCR 69.64%
- The LLMs are baselines, not adjudicators.

### Live Earth-observation counterfactuals
- Sentinel-2: regional median spectral-role MAE 0.0977; 95% region-bootstrap CI 0.0732–0.1242.
- ESA WorldCover: median bilinear invalid-class fraction 12.99%; nearest-neighbour valid-class fraction 100%.
- Copernicus DEM GLO-30: 3x per axis creates 9x cells; 88.89% of fine-grid positions do not correspond to distinct source samples; corrected regional-median core p95 round-trip error 1.3998 m.
- GPM IMERG V07: rainy live cases recovered in 4/4 regions; omitting the 0.5 h duration gives exactly 2.0x numeric overstatement; full-day mean-rate-as-accumulation gives 1/24 of the correct accumulation.

### v7 independent human validation
**Pending.** Reviewer forms are included under `validation/v7_pending/`, but completed independent human verdicts are not available. Do not claim human-validated system accuracy.
