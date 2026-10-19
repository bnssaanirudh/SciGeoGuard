# Scientific threats to validity

- **Construct validity:** PROVEN means predicates encoded in the verifier passed; it does not establish physical truth or universal fitness for purpose.
- **Reference circularity:** v3/v11 references are generated or author-defined. Agreement measures consistency with the specification, not expert-grounded accuracy.
- **Repair circularity:** the same verifier proposes and checks candidate edits; passing it cannot independently establish correctness.
- **Benchmark leakage:** rules and controlled cases are author-developed together. Freeze future cases independently and report family overlap.
- **Case dependence:** synthetic cases may share templates. Confidence intervals should cluster by workflow family/template rather than treat all cases as independent.
- **Baseline fairness:** Qwen/Mistral are not conventional metadata, unit, type, or provenance validators. Equalize inputs and report applicability.
- **External validity:** selected products, regions, sensors, and author-defined faults do not represent arbitrary EO workflows.
- **Repair search bias:** finite candidate templates favor anticipated faults. Report coverage, refusal, cost, incorrect proposals, and unrepairable cases separately.
- **Reproducibility drift:** datasets, packages, notebooks, and endpoints change; capture snapshots/versions, hashes, seeds, commit, and timestamps.
- **Human review:** no completed independent reviewer verdicts were found. Human accuracy and inter-rater agreement remain unestablished.
