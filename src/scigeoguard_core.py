"""Importable frozen SciGeoGuard-X v3 scientific verifier.

This module is extracted without semantic edits from the frozen benchmark notebook
(`notebooks/history/v3_controlled_benchmark.ipynb`, cells 6, 7, and 9).
Benchmark labels and rule outcomes remain encoded assumptions, not ground truth.
"""
from dataclasses import dataclass, field, replace, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

@dataclass
class Artifact:
    name: str
    quantity: str
    unit: Optional[str] = None
    scale: str = "continuous"
    crs: Optional[str] = None
    resolution_m: Optional[float] = None
    temporal_resolution_h: Optional[float] = None
    processing_level: Optional[str] = None
    surface_model: Optional[str] = None
    vertical_datum: Optional[str] = None
    acquisition_time: Optional[str] = None
    available_time: Optional[str] = None
    provenance: Optional[str] = None
    band_role: Optional[str] = None
    nodata_semantics: Optional[str] = None
    uncertainty: Optional[float] = None
    allowed_values: Optional[List[float]] = None
    observed_min: Optional[float] = None
    observed_max: Optional[float] = None
    attrs: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Step:
    op: str
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Intent:
    goal: str
    required_quantity: Optional[str] = None
    required_unit: Optional[str] = None
    decision_time: Optional[str] = None
    max_resolution_m: Optional[float] = None
    requires_bare_earth: bool = False
    requires_cloud_mask: bool = False
    max_uncertainty: Optional[float] = None
    temporal_tolerance_h: Optional[float] = None
    required_value_range: Optional[List[float]] = None



AREA_UNITS = {"m2", "km2", "ha"}
LENGTH_UNITS = {"m", "km", "cm", "mm"}
RATE_UNITS = {"mm/h", "mm/hr", "MM/Hr"}
ACCUM_UNITS = {"mm", "cm", "m"}
DIMENSIONLESS = {"dimensionless", "1"}
CATEGORICAL_SCALES = {"categorical", "nominal", "ordinal", "binary"}
CONTINUOUS_INTERPOLATORS = {"bilinear", "cubic", "lanczos"}

UNIT_DIMENSION = {
    "m2": "area", "km2": "area", "ha": "area",
    "m": "length", "km": "length", "cm": "length", "mm": "length_or_accum",
    "mm/h": "rate", "mm/hr": "rate", "MM/Hr": "rate",
    "dimensionless": "dimensionless", "1": "dimensionless",
    "K": "temperature", "degC": "temperature",
}

def parse_dt(x):
    if not x:
        return None
    d = datetime.fromisoformat(str(x).replace("Z", "+00:00"))
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d

def unit_dimension(u):
    return UNIT_DIMENSION.get(u)

def artifact_copy(x):
    return replace(x, attrs=dict(x.attrs))

def verify_science(artifacts: List[Artifact], steps: List[Step], intent: Intent):
    A = [artifact_copy(x) for x in artifacts]
    findings = []

    def add(code, verdict, message, step_index=None, evidence=None, repair=None):
        findings.append({
            "code": code,
            "verdict": verdict,
            "message": message,
            "step_index": step_index,
            "evidence": evidence or {},
            "repair": repair
        })

    # ---------- source evidence ----------
    for i, x in enumerate(A):
        if not x.provenance:
            add("PROVENANCE_MISSING", "UNPROVEN",
                f"Provenance is missing for artifact {i}: {x.name}.",
                evidence={"artifact": i},
                repair="Attach authoritative product/version/acquisition metadata.")

        if x.resolution_m is not None and x.resolution_m <= 0:
            add("RESOLUTION_INVALID", "REFUTED",
                "Spatial resolution must be positive.", evidence={"artifact": i})

        if x.observed_min is not None and x.observed_max is not None:
            if x.observed_min > x.observed_max:
                add("VALUE_RANGE_INVALID", "REFUTED",
                    "Observed minimum exceeds observed maximum.",
                    evidence={"artifact": i})

    # ---------- workflow semantics ----------
    for si, s in enumerate(steps):
        p = s.params
        op = s.op

        if op == "resample":
            i = p["artifact"]
            method = str(p.get("method", "nearest")).lower()
            target = float(p["target_resolution_m"])
            x = A[i]

            if x.scale in CATEGORICAL_SCALES and method in CONTINUOUS_INTERPOLATORS:
                add("CATEGORICAL_INTERPOLATION", "REFUTED",
                    f"{method} interpolation does not preserve {x.scale} identity.",
                    si,
                    {"measurement_scale": x.scale, "method": method},
                    "Use nearest-neighbour for identity preservation or mode/majority for aggregation.")

            if x.resolution_m is not None and target < x.resolution_m:
                gain = x.resolution_m / target
                if gain > 1.25 and not p.get("evidence_of_new_information", False):
                    add("UNSUPPORTED_RESOLUTION_GAIN", "REFUTED",
                        f"Grid spacing improves {gain:.2f}x without evidence of new information.",
                        si,
                        {"native_m": x.resolution_m, "target_m": target})
            x.resolution_m = target

        elif op == "temporal_aggregate":
            i = p["artifact"]
            x = A[i]
            method = str(p.get("method", "")).lower()
            duration_h = p.get("sample_duration_h")
            declared = p.get("declared_quantity")

            if x.unit in RATE_UNITS and declared == "accumulation":
                if method in {"mean", "average"}:
                    add("RATE_AVERAGED_AS_ACCUMULATION", "REFUTED",
                        "A rate is averaged but the result is declared as an accumulation.",
                        si,
                        {"unit": x.unit, "method": method})
                elif method == "sum" and duration_h not in {1, 1.0}:
                    add("RATE_SUM_WITHOUT_DURATION", "REFUTED",
                        "Sub-hourly rates are summed without multiplying by interval duration.",
                        si,
                        {"sample_duration_h": duration_h})
                elif method in {"integrate", "duration_weighted_sum"}:
                    x.quantity = "precipitation_accumulation"
                    x.unit = "mm"

        elif op == "area":
            i = p["artifact"]
            x = A[i]
            method = p.get("method", "planar")
            if x.crs in {"EPSG:4326", "OGC:CRS84", "CRS84"} and method == "planar":
                add("ANGULAR_COORDINATE_AREA", "REFUTED",
                    "Planar area is computed directly from angular coordinates.",
                    si,
                    {"crs": x.crs},
                    "Use geodesic area or an appropriate projected/equal-area CRS.")
            x.quantity = "area"
            x.unit = p.get("output_unit", "km2")

        elif op == "spectral_index":
            red = A[p["red_artifact"]]
            other = A[p["other_artifact"]]
            expected_other = p.get("expected_other_role")

            if red.band_role != "red":
                add("RED_ROLE_MISMATCH", "REFUTED",
                    f"Red-band role required; got {red.band_role}.", si)

            if expected_other and other.band_role != expected_other:
                add("SPECTRAL_ROLE_MISMATCH", "REFUTED",
                    f"{expected_other} role required; got {other.band_role}.", si)

            if (red.resolution_m is not None and other.resolution_m is not None
                and red.resolution_m != other.resolution_m
                and not p.get("explicit_alignment", False)):
                add("BAND_GRID_MISMATCH", "REFUTED",
                    "Spectral operands have different native resolutions without explicit alignment.",
                    si,
                    {"red_m": red.resolution_m, "other_m": other.resolution_m})

            if p.get("output_artifact") is not None:
                out = A[p["output_artifact"]]
                out.quantity = p.get("output_quantity", out.quantity)
                out.unit = "dimensionless"

        elif op == "require_surface_reflectance":
            x = A[p["artifact"]]
            if x.processing_level not in {"L2A", "surface_reflectance"}:
                add("PROCESSING_LEVEL_MISMATCH", "REFUTED",
                    f"Surface reflectance required; got {x.processing_level}.", si)

        elif op == "require_cloud_mask":
            x = A[p["artifact"]]
            if not bool(x.attrs.get("cloud_mask_applied", False)):
                add("CLOUD_MASK_MISSING", "REFUTED",
                    "Cloud-sensitive analysis has no recorded cloud mask.", si)

        elif op == "require_bare_earth":
            x = A[p["artifact"]]
            if x.surface_model == "DSM":
                add("DSM_USED_AS_DTM", "REFUTED",
                    "Bare-earth analysis is requested from a DSM.", si)
            elif x.surface_model is None:
                add("SURFACE_MODEL_UNKNOWN", "UNPROVEN",
                    "DSM/DTM semantics are not known.", si)

        elif op == "combine_vertical":
            x = A[p["a"]]
            y = A[p["b"]]
            if not x.vertical_datum or not y.vertical_datum:
                add("VERTICAL_DATUM_UNKNOWN", "UNPROVEN",
                    "Vertical-datum compatibility cannot be established.", si)
            elif x.vertical_datum != y.vertical_datum:
                add("VERTICAL_DATUM_MISMATCH", "REFUTED",
                    "Vertical quantities use incompatible datums.", si,
                    {"a": x.vertical_datum, "b": y.vertical_datum})

        elif op == "predict":
            decision = parse_dt(intent.decision_time)
            for i in p.get("features", range(len(A))):
                t = parse_dt(A[i].available_time or A[i].acquisition_time)
                if decision is not None and t is None:
                    add("FEATURE_TIME_UNKNOWN", "UNPROVEN",
                        "Feature availability time is unknown.", si, {"artifact": i})
                elif decision is not None and t > decision:
                    add("FUTURE_INFORMATION", "REFUTED",
                        "A model feature becomes available after the decision time.",
                        si,
                        {"artifact": i, "feature_time": str(t), "decision_time": str(decision)})

        elif op == "split":
            mode = p.get("mode")
            if mode == "spatial":
                sep = float(p.get("separation_m", 0))
                corr = float(p.get("dependence_range_m", 0))
                if corr > 0 and sep < corr:
                    add("SPATIAL_DEPENDENCE_LEAKAGE", "REFUTED",
                        "Train/test separation is below the estimated spatial dependence range.",
                        si,
                        {"separation_m": sep, "dependence_range_m": corr})
            elif mode == "temporal":
                train_end = parse_dt(p.get("train_end"))
                test_start = parse_dt(p.get("test_start"))
                if train_end and test_start and train_end >= test_start:
                    add("TEMPORAL_SPLIT_OVERLAP", "REFUTED",
                        "Training and testing periods overlap or are not chronologically ordered.", si)
            elif mode == "scene":
                overlap = float(p.get("scene_overlap_fraction", 0))
                if overlap > 0:
                    add("SCENE_OVERLAP_LEAKAGE", "REFUTED",
                        "The same scene content appears in both train and test partitions.",
                        si, {"overlap_fraction": overlap})

        elif op == "fill_nodata":
            x = A[p["artifact"]]
            fill = p.get("value")
            if (x.nodata_semantics in {"missing", "masked"}
                and fill == 0
                and p.get("zero_is_physically_valid", True)):
                add("NODATA_COLLAPSED_TO_ZERO", "REFUTED",
                    "Missing data are replaced by a physically meaningful zero.", si)

        elif op == "compare_sensors":
            x = A[p["a"]]
            y = A[p["b"]]
            tx = parse_dt(x.acquisition_time)
            ty = parse_dt(y.acquisition_time)
            tol = float(p.get("tolerance_h", intent.temporal_tolerance_h or 0))
            if not tx or not ty:
                add("ACQUISITION_TIME_UNKNOWN", "UNPROVEN",
                    "Multisensor acquisition-time compatibility is unknown.", si)
            else:
                gap = abs((tx - ty).total_seconds()) / 3600
                if gap > tol:
                    add("MULTISENSOR_TIME_MISMATCH", "REFUTED",
                        "Acquisition gap exceeds the declared scientific tolerance.",
                        si, {"gap_h": gap, "tolerance_h": tol})

        elif op == "convert_unit":
            x = A[p["artifact"]]
            src = x.unit
            dst = p["to"]
            ds, dd = unit_dimension(src), unit_dimension(dst)
            if ds is None or dd is None:
                add("UNIT_DIMENSION_UNKNOWN", "UNPROVEN",
                    "Unit dimensionality is not known.", si, {"from": src, "to": dst})
            elif ds != dd and not ({ds,dd} <= {"length","length_or_accum"}):
                add("UNIT_DIMENSION_MISMATCH", "REFUTED",
                    "Requested conversion changes physical dimension.", si,
                    {"from": src, "to": dst})
            else:
                x.unit = dst

        elif op == "assert_value_range":
            x = A[p["artifact"]]
            lo, hi = p["min"], p["max"]
            if x.observed_min is None or x.observed_max is None:
                add("VALUE_RANGE_UNOBSERVED", "UNPROVEN",
                    "Required physical bounds cannot be checked because observations are missing.", si)
            elif x.observed_min < lo or x.observed_max > hi:
                add("PHYSICAL_RANGE_VIOLATION", "REFUTED",
                    "Observed values violate declared physical bounds.",
                    si,
                    {"observed": [x.observed_min, x.observed_max], "required": [lo, hi]})

        elif op == "aggregate_categorical":
            x = A[p["artifact"]]
            method = p.get("method")
            if x.scale in CATEGORICAL_SCALES and method in {"mean", "median"}:
                add("CATEGORICAL_AGGREGATION_INVALID", "REFUTED",
                    f"{method} is not label-preserving for nominal classes.", si)

        elif op == "drop_quality_metadata":
            x = A[p["artifact"]]
            if p.get("required_downstream", False):
                add("QUALITY_METADATA_LOST", "REFUTED",
                    "A downstream-required quality flag is discarded.", si)

        elif op == "declare_uncertainty":
            A[p["artifact"]].uncertainty = p.get("value")

    # ---------- purpose / postconditions ----------
    if intent.required_unit:
        result_like = [x for x in A if x.quantity == intent.required_quantity] if intent.required_quantity else A
        if result_like:
            known_units = {x.unit for x in result_like if x.unit}
            if known_units and intent.required_unit not in known_units:
                req_dim = unit_dimension(intent.required_unit)
                actual_dims = {unit_dimension(u) for u in known_units}
                if req_dim not in actual_dims:
                    add("OUTPUT_DIMENSION_MISMATCH", "REFUTED",
                        "Output physical dimension is incompatible with the scientific intent.",
                        evidence={"required": intent.required_unit, "actual": sorted(known_units)})

    if intent.max_resolution_m is not None:
        for i,x in enumerate(A):
            if x.resolution_m is None:
                add("RESOLUTION_UNKNOWN", "UNPROVEN",
                    "Required spatial support cannot be checked.", evidence={"artifact": i})
            elif x.resolution_m > intent.max_resolution_m:
                add("RESOLUTION_TOO_COARSE", "REFUTED",
                    "Available spatial resolution is coarser than the declared requirement.",
                    evidence={"artifact": i, "resolution_m": x.resolution_m,
                              "required_m": intent.max_resolution_m})

    if intent.max_uncertainty is not None:
        known = [x.uncertainty for x in A if x.uncertainty is not None]
        if not known:
            add("UNCERTAINTY_UNKNOWN", "UNPROVEN",
                "The intent defines an uncertainty limit but no uncertainty evidence is available.")
        elif max(known) > intent.max_uncertainty:
            add("UNCERTAINTY_EXCEEDS_LIMIT", "REFUTED",
                "Output uncertainty exceeds the declared fitness-for-purpose limit.",
                evidence={"max_observed": max(known), "limit": intent.max_uncertainty})

    if intent.required_value_range:
        lo,hi = intent.required_value_range
        relevant = [x for x in A if x.quantity == intent.required_quantity] if intent.required_quantity else A
        for x in relevant:
            if x.observed_min is None or x.observed_max is None:
                add("INTENT_RANGE_UNPROVEN", "UNPROVEN",
                    "Intent-specific physical bounds cannot be checked.")
            elif x.observed_min < lo or x.observed_max > hi:
                add("INTENT_RANGE_REFUTED", "REFUTED",
                    "Output violates the physical range required by the declared scientific intent.")

    if any(f["verdict"] == "REFUTED" for f in findings):
        verdict = "REFUTED"
    elif any(f["verdict"] == "UNPROVEN" for f in findings):
        verdict = "UNPROVEN"
    else:
        verdict = "PROVEN"

    return {"verdict": verdict, "findings": findings, "final_artifacts": [asdict(x) for x in A]}
