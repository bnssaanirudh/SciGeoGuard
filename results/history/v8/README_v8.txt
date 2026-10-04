
SciGeoGuard-X Multi-Region Real-World Replication v8
====================================================

LIVE_DATA = True

Sources:
- Sentinel-2 L2A via Microsoft Planetary Computer
- ESA WorldCover via Microsoft Planetary Computer
- GPM IMERG V07 2024 via NOAA/AOML ERDDAP
- Copernicus DEM GLO-30 via AWS Open Data

Regions:
Bengaluru_India, Rotterdam_Netherlands, CentralValley_USA, Manaus_Brazil

Interpretation:
This package contains real-data counterfactual scientific stress tests.
It does not contain human expert ground truth.

Invalid variants:
1. Sentinel-2 spectral-role substitution: B11 used where B08 NIR is required for NDVI.
2. Bilinear interpolation of nominal WorldCover classes.
3. IMERG precipitation rate summed without duration or averaged and mislabeled as accumulation.
4. CopDEM ~30 m DSM interpolated to 10 m and falsely claimed as native 10 m information.

Publication wording:
Use "real-data counterfactual replication" or "real-input scientific stress testing".
Do not call these independent human validation cases.

Created UTC:
2026-10-02T18:46:31.233522+00:00
