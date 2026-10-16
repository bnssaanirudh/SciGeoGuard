# Scientific validity audit

This audit supports a software verification/resource contribution around explicit scientific constraints and auditable evidence. Current experiments establish behavior against encoded constraints and selected author-controlled counterfactuals. They do not establish general scientific accuracy.

## Claims supported by local replay

The v11 notebook assertions passed against committed repository inputs in a fresh Python process: mutation detection 10/10; repairs 9/10; found metamorphic repairs re-verified 9/9; frozen 180-case reference agreement 180/180; 47 of 112 refuted workflows yielded a one-edit repair; 47/47 re-verified. Reproduction artifacts and hashes are in `reports/reproduction_20261016/`.

## Limits

- The 180-case target is a generated frozen reference, not independent expert judgment.
- The verifier's rule set and benchmark are author-defined; matching the target can reflect shared assumptions.
- Repairs are evaluated by re-running the same rules that selected them.
- Cases may be correlated by workflow family; case-level independent confidence intervals would overstate precision.
- A selected set of real products plus author-defined perturbations does not demonstrate generalization across sensors, regions, processing stacks, or real operational mistakes.
- Current repository evidence lacks conventional rule-based baselines, external expert labels, and a held-out new-structure benchmark.

## Publication framing

Present the current result as an evidence-carrying software prototype with controlled consistency, repair behavior, and reproducibility evidence. Avoid “scientific accuracy,” “human validated,” superiority, or broad generalization claims until the missing independent evaluations are completed.
