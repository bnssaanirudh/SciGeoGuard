# Reproducibility gaps

| Gap | Required action | Owner/environment | Exit evidence |
|---|---|---|---|
| Reproduce v11 | Run `notebooks/core/v11_earthrefine_repair_confirmed.ipynb` in fresh Colab CPU; compare seven structured outputs to committed hashes | User, Colab | Run log, output hashes, differences |
| Reproduce historical/live EO experiments | Run from clean checkout; record data versions, timestamps, seeds, service responses, commit and package versions | Team; Colab for larger runs | Reproduction matrix; reruns stored separately |
| Independent human reference | Two qualified reviewers independently fill blinded forms; third adjudicates disagreements | User arranges reviewers | Locked forms, adjudicated labels, agreement and uncertainty analysis |
| Competitive conventional baselines | Narrow metadata, quantity/unit, and provenance pilots now exist; expand coverage, validate applicability, compare with established validators | Codex + Colab | Per-case predictions, applicability, expert labels, grouped metrics |
| Repair correctness | Independently specify post-repair constraints and assess side effects | Domain reviewers + Codex | Correctness measured separately from re-verification |
| Generalization | Freeze unseen workflow structures/invariant combinations before evaluation | Research team | Frozen case manifest and overlap report |
| Release integrity | Pin tested environments; add wheel build, clean install and source hash reporting | Codex/CI | Green CI and tagged source hash |
| Manuscript alignment | Tie every number to artifact/commit; remove placeholder dates; check current venue rules | Authors | Source-to-manuscript trace and journal checklist |

Synthetic labels, LLM judgments, and verifier self-checks are not independent human validation.
