import csv, json, tempfile, unittest
from pathlib import Path
from experiments.baselines.run_baselines import load_label_free_cases, run

class BaselineLeakageTests(unittest.TestCase):
    def test_target_columns_are_dropped_before_baseline(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'cases.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=['case_id','workflow_intent','artifacts_json','steps_json','expected','answer']); w.writeheader()
                w.writerow({'case_id':'x','workflow_intent':'{}','artifacts_json':json.dumps([{'name':'a','provenance':'p','scale':'continuous'}]),'steps_json':'[]','expected':'PROVEN','answer':'secret'})
            case=next(load_label_free_cases(p))
            self.assertEqual(set(case),{'case_id','workflow_intent','artifacts_json','steps_json'})
            self.assertNotIn('secret',str(run([case])))

    def test_baselines_abstain_when_no_supported_violation_is_seen(self):
        a=[{'name':'a','provenance':'source','scale':'continuous','unit':'m'}]
        result=run([{'case_id':'x','workflow_intent':'{}','artifacts_json':json.dumps(a),'steps_json':'[]'}])
        self.assertTrue(all(r['prediction']=='UNPROVEN' for r in result))


    def test_metadata_baseline_detects_known_split_overlap(self):
        from experiments.baselines.run_baselines import metadata_only
        result=metadata_only([], [{'op':'split','params':{'train_end':'2020-03-01','test_start':'2020-02-01'}}])
        self.assertEqual(result['prediction'],'REFUTED')
        self.assertEqual(result['violations'][0]['code'],'TEMPORAL_SPLIT_OVERLAP')

    def test_quantity_baseline_detects_rate_summed_without_duration(self):
        from experiments.baselines.run_baselines import quantity_unit
        result=quantity_unit([{'quantity':'precipitation_rate','unit':'mm/hr'}], [{'op':'temporal_aggregate','params':{'artifact':0,'method':'sum','declared_quantity':'accumulation'}}])
        self.assertEqual(result['prediction'],'REFUTED')
        self.assertEqual(result['violations'][0]['code'],'RATE_SUM_WITHOUT_DURATION')

if __name__=='__main__': unittest.main()
