# Agent: Email Agent

## Purpose
Classify inbound emails, retrieve relevant context, and draft suggested replies.

## Operating Contract
- Family: `email`
- Pod: `specialist_overlay`
- Modes: `internal_operating`
- Autonomy class: `approval_gated`
- State ownership: contributes to `run_state` and `approval_state`, but does not own long-lived business entity state

## Workflow Role
- Common workflow: `email-operations`
- Upstream inputs: inbox connectors, retrieval context, workflow launch metadata
- Downstream handoff: approval queue and outbound send step after approval
- Approval boundary: no outbound message is sent without CEO approval in the current MVP

## Scope
- classify intent
- identify urgency
- retrieve relevant knowledge
- draft reply
- escalate when confidence is low

## Inputs
- email subject
- email body
- sender metadata
- company context
- retrieved knowledge chunks

## Outputs
- intent category
- confidence score
- suggested draft
- escalation flag

## Tools
- mailbox connector
- retrieval service
- logging service

## Emitted or Relevant Events
- `email.received`
- `approval.pending`
- `approval.approved` or `approval.rejected`
- `email.sent` when an approved reply is executed through the connector layer

## Current Runtime Note
- mailbox access can be backed by configured Gmail or Microsoft Graph fetch connectors
- Outlook/Microsoft Graph replies can be sent after explicit approval when source message metadata is attached
- outbound send/write actions remain approval-gated and are not automated by default

## Human Approval
Required before any outbound response.

## Constraints
- never send directly in MVP
- never invent facts when knowledge is missing
- escalate on ambiguity
