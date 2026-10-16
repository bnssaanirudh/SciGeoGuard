# SciGeoGuard-X submission checklist

## Evidence and science
- [ ] Reproduce v11 in fresh Colab; compare structured output hashes and investigate differences.
- [ ] Rerun targeted frozen notebooks from a pinned commit and record skips/failures.
- [ ] Complete blinded review with two qualified reviewers and adjudication.
- [x] Implement and run conservative baseline/ablation pilots on identical frozen cases.
- [ ] Expand to competitive conventional validators and independently assessed test cases.
- [ ] Assess repair correctness independently from verifier self-reverification.
- [ ] Add unseen workflow structures and grouped uncertainty analysis.

## Software and reproducibility
- [x] Provide importable core verifier module.
- [x] Add basic deterministic regression tests and CI configuration.
- [x] Build wheel and smoke-test install/import in a clean virtual environment.
- [ ] Add notebook/package parity fixture and confirm CI on GitHub.
- [ ] Pin experiment dependencies; record Python/platform, commit, timestamps, seeds, and hashes.
- [ ] Document data licenses, availability, and version snapshots.

## Manuscript
- [ ] Reconcile every result with exact artifact and commit.
- [ ] Distinguish generated-reference agreement from independent accuracy.
- [ ] Report failures, non-applicability, abstentions, refusals, and limitations.
- [ ] Remove placeholders; check citations, figures, captions, and supplements.
- [ ] Confirm current journal article type, formatting, and data/code policies.

Current gate: **not ready as a validated full-length methodological paper**. A narrow software/resource note may be viable after reproduction, formatting, and release-integrity checks. This assessment does not imply submission or acceptance.
