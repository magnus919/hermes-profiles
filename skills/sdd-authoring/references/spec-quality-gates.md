# Spec Quality Gates

Seven gates a specification must pass before it is ready for downstream SDD phases. These are validation checks, not editorial preferences — a failing gate means the spec is incomplete for its purpose as an executable input to AI code generation.

## Gate 1: Testability

Every acceptance criterion must produce a CLEAR PASS or CLEAR FAIL. An AC that requires human judgment ("the UI should look clean") is not testable — rephrase it as a measurable condition.

**Test:** Read each AC aloud. Can you check "yes or no" against it? If the check requires interpretation (what counts as "responsive"? what counts as "efficient"?), the AC fails this gate.

**Failures caught here:** "The system should handle errors gracefully" → what errors? what does graceful look like?

## Gate 2: Edge Case Completeness

Edge cases must be explicitly enumerated, not implied by "normal case" examples. For every input parameter, every API call, every state transition: what happens at the boundaries?

**Test:** For each user story, list five things that could go wrong. If the spec doesn't address at least three of them, edge cases are underspecified.

**Failures caught here:** "User uploads a file" → what if the file is empty? corrupt? wrong format? too large? a symlink? a directory?

## Gate 3: Scope Boundary Clarity

Out-of-scope must be as explicit as in-scope. Ambiguous scope boundaries are the most common source of downstream friction — the implementation agent cannot distinguish "out of scope" from "the spec forgot to mention this."

**Test:** Read the in-scope list. For each item, ask: "Could someone reasonably include broader functionality under this description?" If yes, the scope boundary is not tight enough.

**Failures caught here:** "In-scope: user authentication" → does this include password reset? social login? MFA? session management? API tokens?

## Gate 4: Non-Functional Requirement Measurability

NFRs must state a specific, measurable threshold and a verification method. "Fast" is not an NFR. "<200ms at P95 under 1000 simultaneous connections" is an NFR.

**Test:** For each NFR, ask: "Can I write a test that fails if this is not met?" If the test is impossible to write, the NFR is not measurable.

**Failures caught here:** "The system should be secure" → what threat model? what controls? what compliance standard?

## Gate 5: Data Contract Sufficiency

Any interface between components — API endpoints, event schemas, function signatures, database schemas — must be specified at a level of detail that enables independent implementation of both sides.

**Test:** Could two implementation agents build the producer and consumer independently using only this spec and their shared contracts? If they would need to coordinate in real time, the data contracts are insufficient.

**Failures caught here:** "API endpoint: POST /orders" → what's the request body? response body? status codes? error format? auth? rate limiting?

## Gate 6: Assumption Inventory

Every assumption made during specification must be explicitly documented with an impact assessment and resolution plan. Undocumented assumptions are not shared understanding — they are future surprises.

**Test:** Count the undocumented assumptions in the spec. If you can find any that aren't in the Assumptions section, the inventory is incomplete. Ask "what would have to be true for this spec to be wrong?" for each section.

**Failures caught here:** "Users will have a stable internet connection" → undocumented assumption that affects offline behavior, retry logic, error handling. Belongs in the Assumptions section.

## Gate 7: Implementation Agent Readiness

The spec must be consumable by an AI coding agent without requiring the agent to ask clarifying questions. SDD's premise is that agents do not ask follow-ups — they implement one interpretation of whatever ambiguity exists.

**Test:** Read the spec as if you cannot ask for clarification. Mark every phrase that could be interpreted in more than one way. Each marked phrase is a spec defect.

**Failures caught here:** "The system should handle common file formats" → the agent must guess what "common" means. Specify exactly which formats.
