"""SciGeoGuard-X v11: EarthRefine evidence certificates and conservative repair.

This module reuses the frozen v3 verifier from notebooks/history/v3_controlled_benchmark.ipynb
and adds named refinement obligations, machine-readable evidence certificates, conservative
one-edit repair candidates, breadth-first minimal repair synthesis, and a controlled
10-family metamorphic suite.

Evidence boundary: the frozen benchmark labels and metamorphic mutations are generated/
author-controlled evidence, not independent human ground truth.
"""
from __future__ import annotations

from dataclasses import asdict
from datetime import timedelta
from copy import deepcopy
from collections import deque
from pathlib import Path
import hashlib
import json


def _load_frozen_verifier():
    root = Path(__file__).resolve().parents[1]
    nb_path = root / "notebooks" / "history" / "v3_controlled_benchmark.ipynb"
    if not nb_path.exists():
        raise FileNotFoundError(f"Frozen verifier notebook not found: {nb_path}")

    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    namespace = {}
    selected = []
    for cell in nb.get("cells", []):
        source = "".join(cell.get("source", []))
        if "@dataclass\nclass Artifact:" in source:
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
        namespace["parse_dt"],
    )


Artifact, Step, Intent, verify_science, parse_dt = _load_frozen_verifier()

OBLIGATION_LIBRARY = {
'CATEGORICAL_INTERPOLATION': ('R-TYPE-MEASUREMENT-SCALE', 'Continuous interpolation requires a continuous measurement scale.', ['measurement_scale','method']),
'UNSUPPORTED_RESOLUTION_GAIN': ('R-SPATIAL-SUPPORT', 'A finer grid is not new observational support unless new information is evidenced.', ['native_m','target_m']),
'RATE_AVERAGED_AS_ACCUMULATION': ('R-TEMPORAL-QUANTITY', 'A rate must be integrated over time before it can be interpreted as an accumulation.', ['unit','method']),
'RATE_SUM_WITHOUT_DURATION': ('R-TEMPORAL-QUANTITY', 'Sub-hourly rates require duration-weighting for accumulation.', ['sample_duration_h']),
'RED_ROLE_MISMATCH': ('R-SPECTRAL-ROLE', 'The red operand of the requested index must have red-band semantics.', []),
'SPECTRAL_ROLE_MISMATCH': ('R-SPECTRAL-ROLE', 'The non-red operand must match the spectral role required by the index.', ['expected_role','actual_role']),
'BAND_GRID_MISMATCH': ('R-SPATIAL-ALIGNMENT', 'Spectral operands must share support or have explicit alignment.', ['red_m','other_m']),
'PROCESSING_LEVEL_MISMATCH': ('R-PROCESSING-LEVEL', 'The workflow requires surface reflectance semantics.', ['processing_level']),
'CLOUD_MASK_MISSING': ('R-QUALITY-MASK', 'Cloud-sensitive analysis requires recorded cloud handling.', []),
'DSM_USED_AS_DTM': ('R-VERTICAL-SURFACE', 'Bare-earth claims require DTM-like rather than DSM-like surface semantics.', []),
'SURFACE_MODEL_UNKNOWN': ('R-VERTICAL-SURFACE', 'Surface-model semantics are required to decide a bare-earth claim.', []),
'VERTICAL_DATUM_UNKNOWN': ('R-VERTICAL-DATUM', 'Vertical compatibility requires both vertical datums.', []),
'VERTICAL_DATUM_MISMATCH': ('R-VERTICAL-DATUM', 'Combined vertical quantities require compatible datums or an explicit transformation.', ['a','b']),
'FEATURE_TIME_UNKNOWN': ('R-CAUSALITY', 'Prediction features require known availability time relative to the decision time.', ['artifact']),
'FUTURE_INFORMATION': ('R-CAUSALITY', 'A predictive workflow must not use information unavailable at decision time.', ['feature_time','decision_time']),
'SPATIAL_DEPENDENCE_LEAKAGE': ('R-EVAL-INDEPENDENCE', 'Train/test separation must exceed the declared spatial dependence range.', ['separation_m','dependence_range_m']),
'TEMPORAL_SPLIT_OVERLAP': ('R-EVAL-INDEPENDENCE', 'Training and testing periods must be chronologically independent.', []),
'SCENE_OVERLAP_LEAKAGE': ('R-EVAL-INDEPENDENCE', 'Scene content must not overlap between train and test partitions.', ['overlap_fraction']),
'NODATA_COLLAPSED_TO_ZERO': ('R-NODATA-SEMANTICS', 'Missingness must not be collapsed into a physically meaningful zero.', []),
'MULTISENSOR_TIME_MISMATCH': ('R-TEMPORAL-SUPPORT', 'Multisensor observations must meet the declared acquisition-time tolerance.', ['gap_h','tolerance_h']),
'ACQUISITION_TIME_UNKNOWN': ('R-TEMPORAL-SUPPORT', 'Acquisition times are required to establish multisensor compatibility.', []),
'UNIT_DIMENSION_UNKNOWN': ('R-DIMENSION', 'Unit dimensions must be known before conversion.', ['from','to']),
'UNIT_DIMENSION_MISMATCH': ('R-DIMENSION', 'Unit conversion must preserve physical dimension.', ['from','to']),
'PHYSICAL_RANGE_VIOLATION': ('R-PHYSICAL-DOMAIN', 'Observed values must satisfy declared physical bounds.', ['observed','required']),
'VALUE_RANGE_UNOBSERVED': ('R-PHYSICAL-DOMAIN', 'Observed bounds are required to check a physical-domain claim.', []),
'CATEGORICAL_AGGREGATION_INVALID': ('R-TYPE-MEASUREMENT-SCALE', 'Nominal classes require label-preserving aggregation.', []),
'ANGULAR_COORDINATE_AREA': ('R-GEOMETRY', 'Area over geographic coordinates requires geodesic or suitable projected geometry.', ['crs']),
'QUALITY_METADATA_LOST': ('R-PROVENANCE-QUALITY', 'Quality evidence required downstream must be preserved.', []),
'PROVENANCE_MISSING': ('R-PROVENANCE', 'Authoritative source provenance is required for scientific auditability.', ['artifact']),
'RESOLUTION_INVALID': ('R-SPATIAL-SUPPORT', 'Spatial resolution must be positive.', ['artifact']),
'VALUE_RANGE_INVALID': ('R-PHYSICAL-DOMAIN', 'Observed minimum cannot exceed observed maximum.', ['artifact']),
'OUTPUT_DIMENSION_MISMATCH': ('R-INTENT-DIMENSION', 'Output dimension must satisfy the scientific intent.', ['required','actual']),
'RESOLUTION_UNKNOWN': ('R-INTENT-SPATIAL', 'Spatial support must be known for an intent with a resolution requirement.', ['artifact']),
'RESOLUTION_TOO_COARSE': ('R-INTENT-SPATIAL', 'Available support must meet the maximum resolution required by the intent.', ['resolution_m','required_m']),
'UNCERTAINTY_UNKNOWN': ('R-INTENT-UNCERTAINTY', 'Uncertainty evidence is required when the intent declares a limit.', []),
'UNCERTAINTY_EXCEEDS_LIMIT': ('R-INTENT-UNCERTAINTY', 'Uncertainty must remain within the declared fitness-for-purpose limit.', ['max_observed','limit']),
'INTENT_RANGE_UNPROVEN': ('R-INTENT-DOMAIN', 'Intent-specific physical bounds require observed output bounds.', []),
'INTENT_RANGE_REFUTED': ('R-INTENT-DOMAIN', 'Output values must satisfy the physical range required by the intent.', []),
}

REPAIRABLE_CODES = {
'CATEGORICAL_INTERPOLATION','UNSUPPORTED_RESOLUTION_GAIN','RATE_AVERAGED_AS_ACCUMULATION','RATE_SUM_WITHOUT_DURATION',
'RED_ROLE_MISMATCH','SPECTRAL_ROLE_MISMATCH','PROCESSING_LEVEL_MISMATCH','CLOUD_MASK_MISSING','DSM_USED_AS_DTM',
'FUTURE_INFORMATION','SPATIAL_DEPENDENCE_LEAKAGE','TEMPORAL_SPLIT_OVERLAP','SCENE_OVERLAP_LEAKAGE','NODATA_COLLAPSED_TO_ZERO',
'CATEGORICAL_AGGREGATION_INVALID','ANGULAR_COORDINATE_AREA'
}


def _fingerprint(artifacts, steps, intent):
    payload={'artifacts':[asdict(x) for x in artifacts],'steps':[asdict(x) for x in steps],'intent':asdict(intent)}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()


def evidence_certificate(artifacts, steps, intent, result=None, case_id=None):
    result=result or verify_science(artifacts,steps,intent)
    obs=[]
    for f in result['findings']:
        oid,pred,req=OBLIGATION_LIBRARY.get(f['code'],('R-UNCLASSIFIED','Workflow must satisfy the encoded scientific constraint.',[]))
        missing=[k for k in req if k not in (f.get('evidence') or {}) or (f.get('evidence') or {}).get(k) is None]
        obs.append({
            'obligation_id':oid,'code':f['code'],'status':f['verdict'],'predicate':pred,
            'step_index':f.get('step_index'),'evidence':f.get('evidence') or {},'missing_evidence':missing,
            'message':f['message'],'suggested_repair':f.get('repair'),'automatically_repairable':f['code'] in REPAIRABLE_CODES
        })
    return {
        'schema':'SciGeoGuard-X/EvidenceCertificate-v0.1',
        'case_id':case_id,
        'verdict':result['verdict'],
        'workflow_hash':_fingerprint(artifacts,steps,intent),
        'n_obligations_reported':len(obs),
        'obligations':obs
    }


def _candidate(artifacts, steps, intent, description, mutate, source_code):
    a=deepcopy(artifacts); s=deepcopy(steps); it=deepcopy(intent); mutate(a,s,it)
    return {'artifacts':a,'steps':s,'intent':it,'description':description,'source_code':source_code,'cost':1}


def repair_candidates(artifacts, steps, intent, result=None):
    result=result or verify_science(artifacts,steps,intent); out=[]
    for f in result['findings']:
        if f['verdict']!='REFUTED': continue
        code=f['code']; si=f.get('step_index'); ev=f.get('evidence') or {}
        if code=='CATEGORICAL_INTERPOLATION' and si is not None:
            out.append(_candidate(artifacts,steps,intent,'Replace continuous interpolation with nearest-neighbour.',lambda a,s,i,si=si:s[si].params.__setitem__('method','nearest'),code))
            out.append(_candidate(artifacts,steps,intent,'Replace continuous interpolation with mode aggregation.',lambda a,s,i,si=si:s[si].params.__setitem__('method','mode'),code))
        elif code=='UNSUPPORTED_RESOLUTION_GAIN' and si is not None:
            native=ev.get('native_m')
            if native is not None:
                out.append(_candidate(artifacts,steps,intent,'Keep grid spacing at the native support; do not invent finer observational support.',lambda a,s,i,si=si,n=native:s[si].params.__setitem__('target_resolution_m',float(n)),code))
        elif code in {'RATE_AVERAGED_AS_ACCUMULATION','RATE_SUM_WITHOUT_DURATION'} and si is not None:
            idx=steps[si].params.get('artifact'); duration=artifacts[idx].temporal_resolution_h if idx is not None else None
            def mut(a,s,i,si=si,d=duration):
                s[si].params['method']='duration_weighted_sum'
                if d is not None: s[si].params['sample_duration_h']=d
            out.append(_candidate(artifacts,steps,intent,'Integrate the rate using the sample duration.',mut,code))
        elif code=='RED_ROLE_MISMATCH' and si is not None:
            for j,x in enumerate(artifacts):
                if x.band_role=='red':
                    out.append(_candidate(artifacts,steps,intent,f'Use artifact {j} ({x.name}) as the red operand.',lambda a,s,i,si=si,j=j:s[si].params.__setitem__('red_artifact',j),code))
        elif code=='SPECTRAL_ROLE_MISMATCH' and si is not None:
            expected=steps[si].params.get('expected_other_role')
            for j,x in enumerate(artifacts):
                if expected and x.band_role==expected:
                    out.append(_candidate(artifacts,steps,intent,f'Use artifact {j} ({x.name}) for spectral role {expected}.',lambda a,s,i,si=si,j=j:s[si].params.__setitem__('other_artifact',j),code))
        elif code=='PROCESSING_LEVEL_MISMATCH' and si is not None:
            for j,x in enumerate(artifacts):
                if x.processing_level in {'L2A','surface_reflectance'}:
                    out.append(_candidate(artifacts,steps,intent,f'Use surface-reflectance artifact {j} ({x.name}).',lambda a,s,i,si=si,j=j:s[si].params.__setitem__('artifact',j),code))
        elif code=='CLOUD_MASK_MISSING' and si is not None:
            for j,x in enumerate(artifacts):
                if bool(x.attrs.get('cloud_mask_applied',False)):
                    out.append(_candidate(artifacts,steps,intent,f'Use artifact {j} ({x.name}) with recorded cloud masking.',lambda a,s,i,si=si,j=j:s[si].params.__setitem__('artifact',j),code))
        elif code=='DSM_USED_AS_DTM' and si is not None:
            for j,x in enumerate(artifacts):
                if x.surface_model=='DTM':
                    out.append(_candidate(artifacts,steps,intent,f'Use bare-earth artifact {j} ({x.name}).',lambda a,s,i,si=si,j=j:s[si].params.__setitem__('artifact',j),code))
        elif code=='FUTURE_INFORMATION' and si is not None:
            bad=ev.get('artifact'); features=list(steps[si].params.get('features',range(len(artifacts))))
            if bad in features and len(features)>1:
                new=[x for x in features if x!=bad]
                out.append(_candidate(artifacts,steps,intent,f'Remove feature {bad} that is unavailable at decision time.',lambda a,s,i,si=si,new=new:s[si].params.__setitem__('features',new),code))
        elif code=='SPATIAL_DEPENDENCE_LEAKAGE' and si is not None:
            dep=ev.get('dependence_range_m')
            if dep is not None:
                out.append(_candidate(artifacts,steps,intent,'Increase train/test spatial separation to the dependence range.',lambda a,s,i,si=si,d=dep:s[si].params.__setitem__('separation_m',float(d)),code))
        elif code=='TEMPORAL_SPLIT_OVERLAP' and si is not None:
            te=parse_dt(steps[si].params.get('train_end'))
            if te:
                ts=(te+timedelta(seconds=1)).isoformat()
                out.append(_candidate(artifacts,steps,intent,'Move the test period to begin after the training period.',lambda a,s,i,si=si,ts=ts:s[si].params.__setitem__('test_start',ts),code))
        elif code=='SCENE_OVERLAP_LEAKAGE' and si is not None:
            out.append(_candidate(artifacts,steps,intent,'Repartition scenes to eliminate train/test content overlap.',lambda a,s,i,si=si:s[si].params.__setitem__('scene_overlap_fraction',0.0),code))
        elif code=='NODATA_COLLAPSED_TO_ZERO' and si is not None:
            out.append(_candidate(artifacts,steps,intent,'Preserve missingness instead of filling with physical zero.',lambda a,s,i,si=si:s[si].params.__setitem__('value',None),code))
        elif code=='CATEGORICAL_AGGREGATION_INVALID' and si is not None:
            out.append(_candidate(artifacts,steps,intent,'Use mode aggregation for nominal classes.',lambda a,s,i,si=si:s[si].params.__setitem__('method','mode'),code))
        elif code=='ANGULAR_COORDINATE_AREA' and si is not None:
            out.append(_candidate(artifacts,steps,intent,'Use geodesic area for geographic coordinates.',lambda a,s,i,si=si:s[si].params.__setitem__('method','geodesic'),code))

    seen=set(); uniq=[]
    for c in out:
        fp=_fingerprint(c['artifacts'],c['steps'],c['intent'])
        if fp not in seen:
            seen.add(fp); uniq.append(c)
    return uniq


def synthesize_minimal_repair(artifacts, steps, intent, max_edits=2, max_states=500):
    initial=verify_science(artifacts,steps,intent)
    if initial['verdict']=='PROVEN':
        return {'status':'ALREADY_PROVEN','cost':0,'edits':[],'result':initial,'artifacts':deepcopy(artifacts),'steps':deepcopy(steps),'intent':deepcopy(intent)}
    q=deque([(deepcopy(artifacts),deepcopy(steps),deepcopy(intent),[],0)])
    seen={_fingerprint(artifacts,steps,intent)}
    explored=0
    while q and explored<max_states:
        a,s,it,edits,cost=q.popleft(); explored+=1
        r=verify_science(a,s,it)
        if r['verdict']=='PROVEN' and cost>0:
            return {'status':'REPAIRED','cost':cost,'edits':edits,'result':r,'artifacts':a,'steps':s,'intent':it,'states_explored':explored}
        if cost>=max_edits: continue
        for cand in repair_candidates(a,s,it,r):
            fp=_fingerprint(cand['artifacts'],cand['steps'],cand['intent'])
            if fp in seen: continue
            seen.add(fp)
            q.append((cand['artifacts'],cand['steps'],cand['intent'],edits+[cand['description']],cost+1))
    return {'status':'NO_SAFE_REPAIR_FOUND','cost':None,'edits':[],'result':initial,'states_explored':explored}


def make_metamorphic_suite():
    suite=[]
    a=[Artifact('WorldCover','land_cover',scale='categorical',resolution_m=10,provenance='ESA WorldCover')]
    valid=[Step('resample',{'artifact':0,'method':'nearest','target_resolution_m':20})]; mut=deepcopy(valid); mut[0].params['method']='bilinear'
    suite.append(('categorical_interpolation',a,valid,mut,Intent('preserve class identity')))

    a=[Artifact('B04','reflectance',band_role='red',resolution_m=10,processing_level='L2A',provenance='Sentinel-2 L2A'),Artifact('B08','reflectance',band_role='nir',resolution_m=10,processing_level='L2A',provenance='Sentinel-2 L2A'),Artifact('B11','reflectance',band_role='swir',resolution_m=20,processing_level='L2A',provenance='Sentinel-2 L2A')]
    valid=[Step('spectral_index',{'red_artifact':0,'other_artifact':1,'expected_other_role':'nir','explicit_alignment':True})]; mut=deepcopy(valid); mut[0].params['other_artifact']=2
    suite.append(('spectral_role_substitution',a,valid,mut,Intent('NDVI')))

    a=[Artifact('IMERG','precipitation_rate',unit='MM/Hr',temporal_resolution_h=0.5,provenance='GPM IMERG V07')]
    valid=[Step('temporal_aggregate',{'artifact':0,'method':'duration_weighted_sum','sample_duration_h':0.5,'declared_quantity':'accumulation'})]; mut=deepcopy(valid); mut[0].params['method']='sum'
    suite.append(('rate_to_accumulation',a,valid,mut,Intent('daily precipitation accumulation')))

    a=[Artifact('CopDEM','elevation',unit='m',scale='continuous',resolution_m=30,provenance='Copernicus DEM GLO-30')]
    valid=[Step('resample',{'artifact':0,'method':'bilinear','target_resolution_m':30})]; mut=deepcopy(valid); mut[0].params['target_resolution_m']=10
    suite.append(('unsupported_resolution_gain',a,valid,mut,Intent('terrain model')))

    a=[Artifact('past','feature',available_time='2024-06-01T00:00:00+00:00',provenance='source-A'),Artifact('future','feature',available_time='2024-07-10T00:00:00+00:00',provenance='source-B')]
    valid=[Step('predict',{'features':[0]})]; mut=deepcopy(valid); mut[0].params['features']=[0,1]
    suite.append(('future_information',a,valid,mut,Intent('forecast',decision_time='2024-07-01T00:00:00+00:00')))

    a=[Artifact('DTM','elevation',surface_model='DTM',provenance='terrain-product'),Artifact('DSM','elevation',surface_model='DSM',provenance='surface-product')]
    valid=[Step('require_bare_earth',{'artifact':0})]; mut=deepcopy(valid); mut[0].params['artifact']=1
    suite.append(('dsm_as_dtm',a,valid,mut,Intent('bare-earth slope')))

    a=[Artifact('samples','image_samples',provenance='dataset')]
    valid=[Step('split',{'mode':'spatial','separation_m':100,'dependence_range_m':50})]; mut=deepcopy(valid); mut[0].params['separation_m']=10
    suite.append(('spatial_leakage',a,valid,mut,Intent('independent evaluation')))

    a=[Artifact('classes','land_cover',scale='nominal',provenance='map')]
    valid=[Step('aggregate_categorical',{'artifact':0,'method':'mode'})]; mut=deepcopy(valid); mut[0].params['method']='mean'
    suite.append(('categorical_aggregation',a,valid,mut,Intent('dominant class')))

    a=[Artifact('L2A','reflectance',processing_level='L2A',provenance='S2'),Artifact('L1C','radiance_like',processing_level='L1C',provenance='S2')]
    valid=[Step('require_surface_reflectance',{'artifact':0})]; mut=deepcopy(valid); mut[0].params['artifact']=1
    suite.append(('processing_level',a,valid,mut,Intent('surface-reflectance analysis')))

    a=[Artifact('terrain','elevation',unit='m',vertical_datum='EGM2008',provenance='terrain'),Artifact('water','water_level',unit='m',vertical_datum='EGM2008',provenance='hydraulic')]
    valid=[Step('combine_vertical',{'a':0,'b':1})]; mut_a=deepcopy(a); mut_a[1].vertical_datum='EGM96'
    suite.append(('vertical_datum_mismatch',(a,mut_a),valid,valid,Intent('flood depth')))
    return suite


def run_metamorphic_suite():
    rows=[]; certs=[]
    for name,a,valid,mut,intent in make_metamorphic_suite():
        if name=='vertical_datum_mismatch':
            valid_a,mut_a=a; a_valid=valid_a; a_mut=mut_a
        else:
            a_valid=a_mut=a
        vr=verify_science(a_valid,valid,intent)
        mr=verify_science(a_mut,mut,intent)
        rep=synthesize_minimal_repair(a_mut,mut,intent,max_edits=2)
        rows.append({
            'family':name,
            'valid_verdict':vr['verdict'],
            'mutated_verdict':mr['verdict'],
            'detected':mr['verdict']=='REFUTED',
            'repair_status':rep['status'],
            'repair_cost':rep.get('cost'),
            'reverified_proven':rep.get('result',{}).get('verdict')=='PROVEN' if rep['status']=='REPAIRED' else False,
            'first_code':mr['findings'][0]['code'] if mr['findings'] else None
        })
        certs.append(evidence_certificate(a_mut,mut,intent,mr,case_id=name))
    return rows,certs
