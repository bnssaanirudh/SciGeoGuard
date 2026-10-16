"""Score already-frozen predictions against a reference in a separate step."""
import argparse, csv, json
from collections import Counter, defaultdict
from pathlib import Path

CLASSES=("PROVEN","REFUTED","UNPROVEN")

def score(prediction_path, reference_path):
    # Predictions are loaded first; the baseline process itself cannot access targets.
    refs={}
    with open(reference_path,newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f): refs[r["case_id"]]=r["generated_expected"]
    groups=defaultdict(list)
    with open(prediction_path,newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["case_id"] not in refs: continue
            groups[r["system"]].append((refs[r["case_id"]],r["prediction"],r["applicable"]=="True"))
    result={}
    for system, rows in groups.items():
        cm=Counter((y,p) for y,p,_ in rows)
        per={c:{"support":sum(y==c for y,_,_ in rows),"recall":(sum(y==c and p==c for y,p,_ in rows)/sum(y==c for y,_,_ in rows) if any(y==c for y,_,_ in rows) else None)} for c in CLASSES}
        result[system]={"n":len(rows),"accuracy":sum(y==p for y,p,_ in rows)/len(rows) if rows else None,
          "abstention_rate":sum(p=="UNPROVEN" for _,p,_ in rows)/len(rows) if rows else None,
          "false_certification_rate":sum(y!="PROVEN" and p=="PROVEN" for y,p,_ in rows)/sum(y!="PROVEN" for y,_,_ in rows) if any(y!="PROVEN" for y,_,_ in rows) else None,
          "applicable_rate":sum(a for _,_,a in rows)/len(rows) if rows else None,
          "per_class":per,"confusion_matrix":{f"{y}->{p}":n for (y,p),n in cm.items()}}
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--predictions",required=True); ap.add_argument("--reference",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    result=score(a.predictions,a.reference); Path(a.out).parent.mkdir(parents=True,exist_ok=True); Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,indent=2))
if __name__=="__main__": main()
