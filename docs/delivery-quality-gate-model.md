<!-- Copyright (c) Dario Pizzolante -->
# Delivery Quality Gate Model

## Purpose
Define how mission-specific quality gates should operate during delivery, from planning through implementation, milestone acceptance, and final handoff.

## Why This Matters
Real consulting engagements do not move straight from implementation to client release.

Depending on the mission and deliverable type, the platform should insert explicit quality gates that can review:

- documents and analysis packs
- requirements and architecture artifacts
- code or automation outputs
- test evidence
- handover packs

These gates should be agent-run, AI-assisted, and grounded in the mission context rather than treated as one generic late-stage checklist.

## Core Principle
Quality gates should be mission-scoped and phase-aware.

They should derive their rubric from:

- the SOW
- the mission statement
- the project plan
- deliverable definitions
- acceptance criteria
- applicable implementation or testing evidence

## Gate Objects
Useful operating objects are:

- `quality_gate_plan`
- `quality_gate_checkpoint`
- `quality_gate_result`
- `quality_evidence_pack`

These may begin as documentation and workflow contracts before becoming first-class persisted objects.

## Quality Gate Plan
Each mission should have a `quality_gate_plan` as part of delivery startup.

It should define:

- mission phase gates
- deliverable classes
- required review depth
- applicable review agents
- acceptance thresholds
- escalation conditions
- handoff release conditions

Example deliverable classes:

- `document_deliverable`
- `code_deliverable`
- `configuration_deliverable`
- `analysis_deliverable`
- `test_evidence_deliverable`
- `handover_deliverable`

## Recommended Gate Types
The platform should support at least these gate types:

- `document_review_gate`
- `requirements_traceability_gate`
- `architecture_review_gate`
- `implementation_review_gate`
- `test_readiness_gate`
- `milestone_release_gate`
- `handover_readiness_gate`

## Mission Phase Mapping
Recommended phase mapping:

### Planning phase
- review SOW deliverables
- validate that the project plan, milestones, and acceptance criteria reflect the agreed scope
- create the initial `quality_gate_plan`

### Analysis and design phase
- review requirements quality, completeness, and traceability
- review architecture deliverables against constraints, risks, and assumptions

### Implementation phase
- review code, automation flows, scripts, configuration, and generated technical artifacts
- verify implementation evidence against requirements and design
- trigger test-readiness checks where applicable

### Pre-milestone phase
- assemble milestone evidence
- validate that required deliverables and quality checks are complete
- decide whether the milestone is ready for client acceptance routing

### Final handoff phase
- review documentation completeness
- review operational handover content
- verify that acceptance, residual risks, and next-step ownership are explicit

## Agent Roles
The main quality-gate families should be:

- `QA / Review Agent` for deliverable quality, completeness, and consistency
- `Testing / QA Agent` for test evidence, defect summary, and release-readiness checks
- `Documentation Agent` for documentation and handoff completeness
- `Risk / Watchdog Agent` when a mission needs stronger escalation or contradiction checks
- `Mission Control Agent` for visibility, checkpoint routing, and escalation tracking

## AI and LLM Role
Quality gates should be genuinely agent-run and LLM-assisted where that adds value.

Examples:

- review a document against the SOW and project plan
- review code or automation output against requirements and architecture notes
- detect missing acceptance criteria, contradictions, or weak evidence
- summarize defects, risks, and revise-or-escalate actions

But the gate should remain workflow-bound:

- explicit inputs
- explicit rubric
- explicit outcome
- explicit evidence links

## Gate Outcomes
Quality gate results should return finite outcomes such as:

- `approve`
- `revise`
- `escalate`
- `human_review`
- `blocked`

## Gate Inputs
Each gate should be able to consume:

- mission statement
- SOW excerpts
- project plan sections
- deliverable payload or artifact refs
- acceptance criteria
- test evidence
- prior gate results
- relevant internal or client retrieval context

## Release Rule
Client-facing milestone acceptance or final handoff should not proceed unless required quality gates have passed or have been explicitly escalated and resolved under policy.

## Billing Link
Quality gates should sit upstream of milestone acceptance and billing.

Recommended chain:

1. implementation or deliverable produced
2. quality gate runs
3. if approved, milestone evidence pack is assembled
4. client acceptance is requested
5. once accepted, billing can trigger according to the `billing_plan`

This keeps internal delivery quality, client acceptance, and billing as separate but linked control points.

## Recommended Runtime Pattern
The best pattern is:

- define gates at mission startup inside the `quality_gate_plan`
- activate checkpoints from the project plan as the mission enters each phase
- run the relevant review agents only when the deliverable type and mission phase justify them
- persist gate results so Track A and Track B can both see delivery readiness

## Real-World Recommendation
My recommendation is not to run every gate on every artifact.

Instead:

- planning and requirements missions should emphasize document and traceability gates
- implementation-heavy missions should emphasize code, test, and release gates
- advisory-only missions may use lighter document and consistency gates
- handoff should always have an explicit final readiness gate

This mirrors real consulting work better than one fixed QA stage at the end.

## Planned Implementation Direction
This model implies later work for:

- a `quality_gate_plan` contract per mission
- phase and deliverable specific gate checkpoints
- AI-assisted review prompts tied to SOW, project plan, and acceptance criteria
- milestone-release gating before client acceptance routing
- handoff-readiness gating before mission closeout

## Current Contract Mapping
The current backend and config contract layer now maps this model through:

- `app/models/delivery_quality.py`
- `config/base/quality_gates.yaml`
- `app/models/operating_state.py` via `project_state` links to active gate plans and results
