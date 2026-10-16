"""Run SciGeoGuard-X intent/repair ablations without reference-label access."""
from __future__ import annotations
import argparse, csv, json
from dataclasses import replace
from pathlib import Path
from scigeoguard_core import Artifact, Step, Intent, verify_science
from scigeoguard_v11 import synthesize_minimal_repair

def load_label_free_cases(path):
    fields=("case_id","workflow_intent","artifacts_json","steps_json")
    with open(path,newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        if not set(fields).issubset(reader.fieldnames or []): raise ValueError(f"Input must contain {fields}")
        for row in reader: yield {k:row[k] for k in fields}


def run(cases):
    rows=[]
    for case in cases:
        artifacts=[Artifact(**x) for x in json.loads(case['artifacts_json'])]
        steps=[Step(**x) for x in json.loads(case['steps_json'])]
        intent=Intent(**json.loads(case['workflow_intent']))
        result=verify_science(artifacts,steps,intent)
        no_intent=verify_science(artifacts,steps,Intent(goal=""))
        repair=synthesize_minimal_repair(artifacts,steps,intent,max_edits=2) if result['verdict']=='REFUTED' else None
        rows.extend([
            {'case_id':case['case_id'],'system':'full_v11','applicable':True,'prediction':result['verdict'],'repair_status':repair['status'] if repair else 'NOT_RUN','repair_cost':repair.get('cost') if repair else ''},
            {'case_id':case['case_id'],'system':'no_repair','applicable':True,'prediction':result['verdict'],'repair_status':'DISABLED','repair_cost':''},
            {'case_id':case['case_id'],'system':'no_intent_conditioning','applicable':True,'prediction':no_intent['verdict'],'repair_status':'DISABLED','repair_cost':''},
        ])
    return rows


def main():
    p=argparse.ArgumentParser(); p.add_argument('--cases',required=True); p.add_argument('--out',required=True); a=p.parse_args()
    rows=run(load_label_free_cases(a.cases)); out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['case_id','system','applicable','prediction','repair_status','repair_cost']); w.writeheader(); w.writerows(rows)
    print(json.dumps({'cases':len(rows)//3,'predictions':len(rows),'output':str(out)},indent=2))
if __name__=='__main__': main()
