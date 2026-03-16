<!-- Copyright (c) Dario Pizzolante -->
# Workflow: Procurement PO

## Trigger
A purchase request is submitted for software, services, equipment, or subcontracting.

## Pod Owner
`Ops`

## Start Event
- `purchase.requested`
- manual procurement intake

## Goal
Validate budget and policy constraints, draft a purchase order, and route it for approval before any commitment.

## State Objects
- `run_state`
- `approval_state`

## Primary Agent Roles
- `Procurement Agent`: validate budget and draft purchase-order artifacts
- `Vendor / Procurement Agent`: maintain supplier, renewal, and procurement context
- `Risk / Watchdog Agent`: later surfaces threshold breaches or missing approvals

## Emitted Events
- `procurement.validated`
- `procurement.exception_detected`
- `approval.pending`
- `po.issued`

## Steps
1. intake purchase request and supplier details
2. validate category, requester, and required supporting context
3. check budget availability and approval thresholds
4. draft purchase order and internal justification summary
5. detect policy exceptions and commitment risks
6. route the PO to CEO approval
7. release PO only after approval

## Approval Gates
- no purchase order or external commitment is released without CEO approval

## AI Steps
- supplier justification drafting
- exception explanation
- negotiation note drafting

## Deterministic Steps
- budget lookup
- policy threshold checks
- PO numbering
- approval routing
- supplier handoff
- audit logging

## Failure Handling
- missing budget owner -> block and escalate
- request exceeds approved threshold -> escalate to CEO
- supplier or ERP connector failure -> retry then hold request

## Audit Data
- request id
- supplier
- requester
- budget code
- total commitment value
- policy exceptions
- approval status
