# Workflow: Email Operations

## Trigger
A new inbound email is received.

## Goal
Produce a grounded draft reply and route it for approval.

## Steps
1. ingest inbound email
2. classify intent
3. retrieve relevant knowledge
4. generate draft reply
5. assign confidence score
6. route to approval queue
7. send only after approval

## AI Steps
- intent classification
- reply drafting
- confidence estimation

## Deterministic Steps
- email ingestion
- retrieval call
- approval routing
- outbound send
- audit logging

## Failure Handling
- missing knowledge -> manual review
- low confidence -> escalate
- connector failure -> retry then manual review

## Audit Data
- inbound message id
- workflow id
- prompt version
- model used
- confidence score
- approval status
