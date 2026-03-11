# Workflow: Procurement PO

## Trigger
A purchase request is submitted for software, services, equipment, or subcontracting.

## Goal
Validate budget and policy constraints, draft a purchase order, and route it for approval before any commitment.

## Steps
1. intake purchase request and supplier details
2. validate category, requester, and required supporting context
3. check budget availability and approval thresholds
4. draft purchase order and internal justification summary
5. detect policy exceptions and commitment risks
6. route the PO to CEO approval
7. release PO only after approval

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
