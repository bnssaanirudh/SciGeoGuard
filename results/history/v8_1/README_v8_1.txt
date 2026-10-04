
SciGeoGuard-X Robustness Corrections v8.1
==========================================

LIVE_DATA = True
PUBLICATION_READY = False

Preserved from completed live v8:
- Sentinel-2 results
- ESA WorldCover results

Corrected in v8.1:
- GPM IMERG V07 temporal semantics
- Copernicus DEM aligned resampling

Statistical synthesis:
- region-level aggregation
- 10,000-sample percentile cluster bootstrap
- geographic region is the bootstrap unit

Primary publication files:
- FINAL_PUBLICATION_RESULTS_TABLE_v8_1.csv
- Region_cluster_bootstrap_95CI.csv
- FINAL_REALDATA_COUNTERFACTUALS_v8_1.csv
- FINAL_COMPOSITE_FIGURE_v8_1.png
- MANUSCRIPT_READY_RESULTS_v8_1.txt
- PUBLICATION_GATES_v8_1.csv
- CORRECTION_AND_PROVENANCE_MANIFEST.json

Interpretation:
Real-data paired counterfactual replication.
Not independent human ground truth.
Human validation remains the v7 stage.
