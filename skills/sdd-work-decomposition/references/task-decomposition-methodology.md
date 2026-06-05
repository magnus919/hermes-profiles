# Task Decomposition Methodology

Translating specification requirements into independently implementable and verifiable tasks.

## The Extraction Pattern

SDD task decomposition is an **extraction**, not an invention. Every task must trace directly to a section of the specification. If a task cannot be linked to a specific acceptance criterion or user story, the task is not derived from the spec — it is speculation.

### Step 1: Map Stories to Task Groups

Each user story defines a logical grouping of behavior. Create one task group per user story. The story's acceptance criteria define the task boundaries within that group.

### Step 2: Identify Foundation Tasks

Foundation tasks are not directly implementable features — they create the conditions for feature implementation. Examples: scaffolding, data model schemas, interface stubs, configuration, CI setup. These are extracted from the spec's data contracts and NFRs, not from user stories.

### Step 3: Decompose Acceptance Criteria into Tasks

For each user story, each acceptance criterion maps to one or more tasks. The mapping is:
- One AC → one task for simple conditions
- One AC → multiple tasks only when the AC requires multi-step implementation (e.g., "user can register, verify email, and log in" is three tasks, one AC)
- Multiple ACs → one task only when the ACs are trivially related (e.g., two input validation rules that share the same implementation surface)

### Step 4: Derive Dependencies from Contracts, Not Intuition

A dependency is real only when task B requires task A's output — a file, a schema, a function signature — that cannot be stubbed. Dependencies that can be satisfied by an interface contract encoded in the spec are not real dependencies. Document the contract in the spec and both tasks can proceed in parallel against it.

### Step 5: Size Tasks for Single-Session Implementation

Each task should be completable in one AI coding agent session (30-120 minutes). The size heuristic:

| Size | Estimate | Characteristic |
|------|----------|---------------|
| Small | < 1 hour | Single function, simple validation, config change |
| Medium | 1-2 hours | Feature with 2-3 ACs, new endpoint, data transformation |
| Large | 2-4 hours | Multi-AC feature with state management, integration work |

If a task exceeds Large, the spec section is too coarse. Refine the spec before decomposing further.

## The Atomicity Test

A task is atomic if all of the following are true:
1. It can be implemented independently (its dependencies are limited to contracts and stubs)
2. It can be verified independently (its ACs can be tested without other tasks completing)
3. It produces an atomic commit (the diff is self-contained and reviewable)
4. If the commit is rolled back, no other task's implementation is broken

## Spec Traceability

Every task card MUST include:
- The SPEC.md section it implements
- The specific ACs it satisfies
- The user story it belongs to

This traceability chain is what enables verification: the VERIFICATION.md can map each test result back to a task back to an AC back to a spec requirement. Without it, a failing verification creates ambiguity about what was supposed to happen.
