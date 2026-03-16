<!-- Copyright (c) Dario Pizzolante -->
# Lead Intake and Materialization Model

## Purpose
Define how raw commercial signals become structured leads in the platform, especially when the source is not manual.

## Why This Exists
The current Growth flow already assumes `lead.received`, but the platform also needs a governed upstream model for:

- where lead signals come from
- how they are normalized
- when they become a real platform lead
- when they require human review instead of automatic creation

## Core Principle
Not every inbound signal is immediately a lead.

The platform should distinguish:

- `lead_signal`: raw inbound commercial evidence
- `lead_candidate`: normalized candidate record derived from one or more signals
- `lead`: a materialized platform lead that can enter Growth workflows through `lead.received`

`lead.received` should remain the canonical event that starts the normal opportunity workflow after materialization has succeeded.

## Lead Source Classes
The platform should support these main source classes:

- `manual_entry`
- `inbound_email`
- `website_form`
- `calendar_booking`
- `meeting_note`
- `referral`
- `partner_channel`
- `crm_import`
- `document_intake`
- `chat_message`
- `web_research`

## Source Examples
Typical examples include:

- manual operator entry after a phone call or networking event
- inbound email asking for consulting help
- website contact form or inbound RFP form
- discovery-call booking with enough context to indicate demand
- meeting note or transcript that identifies a new opportunity
- referral from an existing client or partner
- imported lead list from another CRM or spreadsheet
- inbound document such as an RFP, tender, or requirements pack
- inbound chat or messaging request
- externally researched company or account signal that still needs qualification

## Materialization Rule
Automatic materialization should be allowed only when the signal or normalized candidate contains enough evidence to create a bounded lead record.

Minimum useful fields:

- source class
- source reference
- contact or company identity
- problem or need signal
- timestamp

Helpful but optional fields:

- urgency
- budget hint
- service area hint
- geography
- referral source
- meeting or document reference

If the minimum useful fields are missing, the system should not silently create a real lead. It should create a reviewable candidate or operator task instead.

## Recommended Flow
The preferred lead intake sequence is:

1. detect or receive a `lead_signal`
2. normalize source metadata into a `lead_candidate`
3. deduplicate against existing contacts, clients, and open opportunities
4. score confidence and completeness
5. either materialize the lead automatically or route to review
6. if materialized, create or update `opportunity_state`
7. emit `lead.received`

## Automatic vs Review-Bound Materialization
Recommended rules:

- `manual_entry`: usually materialize immediately
- `inbound_email`: auto-materialize when sender, company or contact, and consulting need are reasonably extractable
- `website_form`: auto-materialize when required fields are present
- `calendar_booking`: auto-materialize when booking metadata includes problem context or service intent
- `meeting_note`: review-bound unless the note clearly indicates a new account opportunity
- `referral`: auto-materialize if referrer plus target account and need are present
- `partner_channel`: review-bound unless the partner feed is already normalized
- `crm_import`: materialize through batch validation and dedupe, not blind direct insert
- `document_intake`: review-bound unless linked to a known account and explicit request
- `chat_message`: review-bound unless identity and need are clear
- `web_research`: never auto-materialize straight to an active lead without review

## Dedupe and Merge Rule
Before creating a new lead, the platform should check for:

- existing client
- existing prospect or contact
- open opportunity for the same company or mission
- recent similar inbound signal

Possible outcomes:

- create new lead
- merge into existing opportunity
- attach as new source evidence to an existing prospect
- route to human review
- discard as noise

## Operational Objects
Useful lead-intake operating objects are:

- `lead_signal`
- `lead_candidate`
- `lead_source_ref`
- `materialization_decision`

These may begin as documentation and event payload concepts before becoming first-class database tables.

## Event Model
Recommended pre-opportunity event sequence:

- `lead.signal.detected`
- `lead.candidate.created`
- `lead.review.requested`
- `lead.materialized`

Canonical Growth workflow entry remains:

- `lead.received`

That means:

- `lead.materialized` marks successful conversion from signal or candidate into a real lead record
- `lead.received` remains the stable start event for the downstream Growth workflow

## State Mapping
Once materialized, the lead should create or update `opportunity_state`.

Suggested early fields:

- `prospect_id`
- `source_refs`
- `service_type`
- `next_action`
- `qualification_status`

## Agent Responsibilities
The `Lead Intake Agent` should:

- watch supported source classes
- normalize signals into candidates
- check completeness and dedupe
- materialize safe high-confidence leads
- route borderline cases to review

The `Account Research Agent` and `Qualification Agent` should operate after a lead is materialized, not on raw noise by default.

## Track Model
Lead spotting and materialization should happen in Track A because it belongs to the consulting firm's commercial pipeline.

- Track A owns prospecting, lead intake, qualification, proposal, SOW, and contract progression
- Track B begins only after a client or engagement is sufficiently real to justify mission setup and tenant-scoped delivery execution

## Planned Implementation Direction
This model implies later work for:

- source-specific lead ingestion connectors and adapters
- candidate normalization and dedupe rules
- automatic materialization thresholds
- operator review queue for ambiguous lead candidates
- conversion from qualified opportunity and signed scope into mission planning and later agent dispatch
