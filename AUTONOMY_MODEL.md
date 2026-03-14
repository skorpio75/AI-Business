# Autonomy Model

## Purpose
Define the autonomy classes used to constrain what an agent may do inside a workflow.

## Core Rule
Autonomy is granted to an agent instance in context, not to an agent family universally.

## Classes

### `assistant`
May:
- analyze
- classify
- draft
- summarize
- recommend next actions

May not:
- commit sensitive external actions
- update authoritative business state outside bounded draft paths
- bypass approval or policy checks

### `supervised_executor`
May:
- perform bounded operational writes
- update allowed workflow state
- generate artifacts
- execute low-risk tools inside workflow rules

May not:
- independently commit sensitive external actions
- change approval outcomes
- escape assigned tool profile or tenant scope

### `bounded_autonomous`
May:
- execute low-risk recurring actions within explicit guardrails
- update bounded state and complete repeatable subflows

May not:
- create external commitments outside delegated policy
- access unrestricted tools
- operate beyond defined domain boundaries

### `approval_gated`
May:
- prepare sensitive actions
- request approval
- assemble all required context for a human decision

May not:
- finalize the gated action without recorded approval
- treat approval intent as approval result

## MVP Default
The platform currently defaults most execution-capable agents to `assistant` or `supervised_executor`, with sensitive actions resolved through the approval-first model.
