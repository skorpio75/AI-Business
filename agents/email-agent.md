# Agent: Email Agent

## Purpose
Classify inbound emails, retrieve relevant context, and draft suggested replies.

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

## Current Runtime Note
- mailbox access can be backed by configured Gmail or Microsoft Graph fetch connectors
- outbound send/write actions remain approval-gated and are not automated by default

## Human Approval
Required before any outbound response.

## Constraints
- never send directly in MVP
- never invent facts when knowledge is missing
- escalate on ambiguity
