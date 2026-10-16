"""Minimal runnable SciGeoGuard-X example. Run from the repository root."""
from scigeoguard_core import Artifact, Step, Intent, verify_science

artifacts = [Artifact(name="land_cover", quantity="land_cover_class", scale="nominal",
                      resolution_m=10.0, provenance="ESA WorldCover 2021 v200")]
steps = [Step("resample", {"artifact": 0, "method": "bilinear", "target_resolution_m": 10.0})]
intent = Intent(goal="preserve categorical land-cover identity")
result = verify_science(artifacts, steps, intent)
print("verdict:", result["verdict"])
for finding in result["findings"]:
    print(f"{finding['code']}: {finding['message']}")
    if finding.get("repair"):
        print("repair:", finding["repair"])
assert result["verdict"] == "REFUTED"
assert any(f["code"] == "CATEGORICAL_INTERPOLATION" for f in result["findings"])
