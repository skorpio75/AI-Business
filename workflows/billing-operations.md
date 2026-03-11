# Workflow: Billing Operations

## Trigger
Approved timesheet entries, milestone completion, or a manual billing run request.

## Goal
Generate an invoice-ready billing package and route it for CEO approval before external release.

## Steps
1. collect approved delivery and time records
2. validate billable items against contract scope
3. calculate invoice line items, tax assumptions, and due date
4. draft invoice summary and customer-facing note
5. flag anomalies such as missing rates, duplicate items, or budget overruns
6. route invoice package to approval queue
7. release invoice only after approval

## AI Steps
- anomaly explanation
- invoice note drafting
- collection reminder drafting

## Deterministic Steps
- source data retrieval
- line-item calculation
- contract/rate validation
- approval routing
- ERP/accounting handoff
- audit logging

## Failure Handling
- missing approved source records -> block and escalate
- contract mismatch -> manual review
- accounting connector failure -> retry then queue for ops follow-up

## Audit Data
- client id
- project id
- billing period
- source record ids
- invoice total
- anomaly flags
- approval status
