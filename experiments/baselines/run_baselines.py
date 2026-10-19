"""Run conservative non-LLM comparators without reference-label access.

This script intentionally reads only case_id, workflow_intent, artifacts_json, and
steps_json. It never opens Frozen_v3_reference.csv or a label-bearing file.
Each baseline returns REFUTED only when a supported rule is explicitly violated;
otherwise it abstains as UNPROVEN. It does not certify PROVEN cases.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

INPUT_FIELDS = ("case_id", "workflow_intent", "artifacts_json", "steps_json")
LENGTH = {"m": "length", "km": "length", "cm": "length", "mm": "length"}
AREA = {"m2": "area", "km2": "area", "ha": "area"}
RATE = {"mm/h": "rate", "mm/hr": "rate", "MM/Hr": "rate"}
ACCUM = {"mm": "accumulation", "cm": "accumulation"}
DIMENSIONLESS = {"1": "dimensionless", "dimensionless": "dimensionless"}


def dim(unit):
    for table in (LENGTH, AREA, RATE, ACCUM, DIMENSIONLESS):
        if unit in table:
            return table[unit]
    return None


def _result(name, checks, violations):
    return {"system": name, "applicable": bool(checks), "supported_checks": len(checks),
            "violations": violations,
            "prediction": "REFUTED" if violations else "UNPROVEN"}


def metadata_only(artifacts, steps, intent=None):
    checks, violations = [], []
    intent=intent or {}
    for i, a in enumerate(artifacts):
        if a.get("resolution_m") is not None:
            checks.append("positive_resolution")
            if float(a["resolution_m"]) <= 0:
                violations.append({"code":"RESOLUTION_INVALID","artifact":i})
        if a.get("observed_min") is not None and a.get("observed_max") is not None:
            checks.append("ordered_observed_range")
            if float(a["observed_min"]) > float(a["observed_max"]):
                violations.append({"code":"VALUE_RANGE_INVALID","artifact":i})
        if intent.get("decision_time") and a.get("available_time"):
            checks.append("feature_available_before_decision")
            if str(a["available_time"]) > str(intent["decision_time"]):
                violations.append({"code":"FUTURE_INFORMATION","artifact":i})
    for j, step in enumerate(steps):
        p=step.get("params", {}); op=step.get("op")
        if op == "resample" and p.get("artifact") is not None:
            a=artifacts[int(p["artifact"])]
            checks.append("scale_compatible_resampling")
            if str(a.get("scale", "")).lower() in {"categorical","nominal","ordinal","binary"} and str(p.get("method", "")).lower() in {"bilinear","cubic","lanczos"}:
                violations.append({"code":"CATEGORICAL_INTERPOLATION","step":j})
        if op == "aggregate_categorical":
            checks.append("categorical_aggregation_method")
            if str(p.get("method", "")).lower() not in {"mode","majority","nearest"}:
                violations.append({"code":"CATEGORICAL_AGGREGATION_INVALID","step":j})
        if op == "split":
            train_end=p.get("train_end"); test_start=p.get("test_start")
            if train_end and test_start:
                checks.append("chronological_split")
                if str(test_start) <= str(train_end): violations.append({"code":"TEMPORAL_SPLIT_OVERLAP","step":j})
            if p.get("separation_m") is not None and p.get("dependence_range_m") is not None:
                checks.append("spatial_split_separation")
                if float(p["separation_m"]) < float(p["dependence_range_m"]): violations.append({"code":"SPATIAL_DEPENDENCE_LEAKAGE","step":j})
        if op == "compare_sensors" and not p.get("explicit_alignment",False):
            ai, bi=p.get("a"),p.get("b")
            if ai is not None and bi is not None and 0<=int(ai)<len(artifacts) and 0<=int(bi)<len(artifacts):
                a,b=artifacts[int(ai)],artifacts[int(bi)]
                if a.get("crs") and b.get("crs"):
                    checks.append("crs_alignment")
                    if a["crs"] != b["crs"]: violations.append({"code":"CRS_MISMATCH","step":j})
    return _result("metadata_only", checks, violations)


def quantity_unit(artifacts, steps):
    checks, violations = [], []
    def quantity_dim(unit, quantity):
        if unit == "mm" and quantity in {"elevation","water_level","distance","flood_depth"}: return "length"
        return dim(unit)
    for j, step in enumerate(steps):
        p=step.get("params", {}); op=step.get("op")
        if op == "convert_unit" and p.get("artifact") is not None:
            a=artifacts[int(p["artifact"])]
            source=quantity_dim(a.get("unit"),a.get("quantity")); target=quantity_dim(p.get("to"),a.get("quantity"))
            if source is not None and target is not None:
                checks.append("unit_dimension_preservation")
                if source != target: violations.append({"code":"UNIT_DIMENSION_MISMATCH","step":j,"from":a.get("unit"),"to":p.get("to")})
        if op == "temporal_aggregate" and p.get("artifact") is not None:
            a=artifacts[int(p["artifact"])]
            if a.get("quantity")=="precipitation_rate" or a.get("unit") in RATE:
                checks.append("rate_to_accumulation_semantics")
                if p.get("method") not in {"duration_weighted_sum","integrate"} or p.get("sample_duration_h") is None:
                    violations.append({"code":"RATE_SUM_WITHOUT_DURATION","step":j})
        if op == "require_bare_earth":
            idx=p.get("artifact",0)
            if idx is not None and 0<=int(idx)<len(artifacts):
                checks.append("bare_earth_surface_type")
                if artifacts[int(idx)].get("surface_model")=="DSM": violations.append({"code":"DSM_USED_AS_DTM","step":j})
    return _result("quantity_unit_aware", checks, violations)


def provenance_aware(artifacts, steps):
    checks, violations = [], []
    if artifacts:
        checks.append("source_provenance_present")
        for i, a in enumerate(artifacts):
            if not a.get("provenance"):
                violations.append({"code":"PROVENANCE_MISSING","artifact":i})
    # Check preservation claims only when quality evidence is explicitly used downstream.
    for j, step in enumerate(steps):
        p=step.get("params", {})
        if p.get("requires_quality_metadata") is True:
            checks.append("required_quality_metadata_retained")
            ai=p.get("artifact")
            if ai is not None and not artifacts[int(ai)].get("quality_metadata"):
                violations.append({"code":"QUALITY_METADATA_LOST","step":j})
    return _result("provenance_aware", checks, violations)


def load_label_free_cases(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader=csv.DictReader(f)
        if not set(INPUT_FIELDS).issubset(reader.fieldnames or []):
            raise ValueError(f"Input must contain {INPUT_FIELDS}")
        # Select a fixed allowlist so any reference/answer fields are never passed to a baseline.
        for row in reader:
            yield {k:row[k] for k in INPUT_FIELDS}


def run(cases):
    rows=[]
    for row in cases:
        artifacts=json.loads(row["artifacts_json"]); steps=json.loads(row["steps_json"])
        for fn in (metadata_only, quantity_unit, provenance_aware):
            pred=metadata_only(artifacts,steps,json.loads(row["workflow_intent"])) if fn is metadata_only else fn(artifacts,steps)
            rows.append({"case_id":row["case_id"],**pred,
                         "violations_json":json.dumps(pred["violations"],sort_keys=True)})
    return rows


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cases",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    rows=run(load_label_free_cases(args.cases))
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=["case_id","system","applicable","supported_checks","violations","prediction","violations_json"])
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps({"cases":len({r['case_id'] for r in rows}),"predictions":len(rows),"output":str(out)},indent=2))

if __name__ == "__main__": main()
