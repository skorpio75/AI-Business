# TODO

## Current Focus
- Active phase: `Phase 3 - Track A Internal MVP Workflows`
- Active cross-cutting stream: `AI-Business IDE handoff integration`
- Immediate goal: finish the handoff-alignment documentation and contract layer, then continue provider auth/bootstrap and secret handling

## Now
- [x] `H-T01` Create the missing meta-model docs from `AI-Business_IDE_Handoff.md`
- [x] `H-T02` Update governance docs to adopt the 4-pod model and normalized event/state/tool/autonomy language
- [x] `P3-T01` Scaffold React mission-control app
- [x] `P3-T02` Build workflow monitor page
- [x] `P3-T03` Build approval queue page
- [x] `P3-T04` Build agent activity page
- [x] `P3-T05` Implement email operations workflow end-to-end
- [x] `P3-T06` Implement knowledge Q&A workflow end-to-end
- [x] `P3-T07` Implement proposal generation workflow baseline
- [x] `P3-T08` Connect approval actions from UI to API

## Next
- [ ] `H-T03` Align markdown agent/workflow specs more fully with the new contracts and cross-agent handoff choreography
- [ ] `P2-T15` Align agent registry and base contracts with pod model and family/mode/instance identity
- [ ] `P3-T16` Add OAuth/bootstrap and secret handling for Gmail, Google Calendar, and Microsoft Graph

## Soon After
- [ ] `P2-T16` Define normalized event names, approval classes, autonomy classes, and tool permission profiles in backend contracts/config
- [ ] `P3-T12` Add CTO/CIO panel (customer scope insights, strategy options, internal tech improvement queue)
- [ ] `P3-T13` Add finance cockpit panels (accounting exceptions, close status, CFO scenario cards)
- [ ] `P3-T14` Add Chief AI/Digital Strategy panel (opportunity portfolio, AI/data roadmap, delivery guidance cards)

## Recently Finished
- [x] Carry the PMO split into runtime-facing registry/config/contracts and surface pod/family/mode metadata in the agent activity view
- [x] Clarify the distinction between PMO governance/control and project-management execution coordination
- [x] `P3-T01A` Adopt `shadcn/ui` + Tailwind foundation and migrate shared mission-control UI primitives
- [x] `P3-T20` Add explicit routing badges for local model, cloud route, fallback-rule execution, and local LLM invocation status

## Watchlist
- [ ] Keep `ROADMAP.md` as the full source of truth
- [ ] Keep `TODO.md` short and execution-oriented
- [ ] Keep Track A internal instances and Track B client instances isolated even when they share an agent family
- [ ] Avoid adding UI logic before API/contracts are stable enough to consume
