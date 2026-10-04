"""Minimal runnable SciGeoGuard-X example using the frozen v3 verifier notebook.

Run from the repository root:
    python examples/quickstart.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "history" / "v3_controlled_benchmark.ipynb"


def load_verifier_from_notebook(path: Path):
    nb = json.loads(path.read_text(encoding="utf-8"))
    namespace: dict = {}
    selected = []
    for cell in nb.get("cells", []):
        source = "".join(cell.get("source", []))
        if "@dataclass\nclass Artifact:" in source:
            # BenchCase is benchmark-only; the public verifier needs Artifact/Step/Intent.
            source = source.split("@dataclass\nclass BenchCase:")[0]
            selected.append(source)
        elif "AREA_UNITS =" in source and "def artifact_copy" in source:
            selected.append(source)
        elif "def verify_science" in source:
            selected.append(source)
    prelude = (
        "from dataclasses import dataclass, field, asdict, replace\n"
        "from datetime import datetime, timezone\n"
        "from typing import Any, Dict, List, Optional\n"
    )
    exec(prelude + "\n" + "\n\n".join(selected), namespace)
    return (
        namespace["Artifact"],
        namespace["Step"],
        namespace["Intent"],
        namespace["verify_science"],
    )


Artifact, Step, Intent, verify_science = load_verifier_from_notebook(NOTEBOOK)

# Nominal land-cover identities must not be continuously interpolated.
artifacts = [
    Artifact(
        name="land_cover",
        quantity="land_cover_class",
        scale="nominal",
        resolution_m=10.0,
        provenance="ESA WorldCover 2021 v200",
    )
]
steps = [
    Step(
        "resample",
        {"artifact": 0, "method": "bilinear", "target_resolution_m": 10.0},
    )
]
intent = Intent(goal="preserve categorical land-cover identity")

result = verify_science(artifacts, steps, intent)
print("verdict:", result["verdict"])
for finding in result["findings"]:
    print(f'{finding["code"]}: {finding["message"]}')
    if finding.get("repair"):
        print("repair:", finding["repair"])

assert result["verdict"] == "REFUTED"
assert any(f["code"] == "CATEGORICAL_INTERPOLATION" for f in result["findings"])
