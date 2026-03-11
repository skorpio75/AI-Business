# Workflow: Quality Testing Gate

## Trigger
A deliverable is marked ready for release, handoff, or internal acceptance.

## Goal
Run definition-of-done checks, summarize test evidence, and block release until quality gates are satisfied.

## Steps
1. collect release candidate metadata and test evidence
2. validate required artifacts and coverage expectations
3. classify defects by severity and release impact
4. generate release-readiness summary and residual risk note
5. decide pass, conditional pass, or fail
6. route conditional or failed outcomes for review
7. release only after gate conditions are satisfied

## AI Steps
- defect clustering
- residual risk summarization
- release note drafting

## Deterministic Steps
- evidence collection
- gate checklist validation
- severity thresholds
- approval routing for exceptions
- audit logging

## Failure Handling
- missing test evidence -> fail gate
- unresolved critical defect -> block release
- CI/test connector failure -> retry then mark gate inconclusive

## Audit Data
- release candidate id
- test run ids
- defect counts by severity
- gate decision
- exception rationale
- approval status
