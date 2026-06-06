# Architecture Governance

Frameworks for maintaining architectural coherence, making design decisions transparent, and ensuring the technology organization operates with aligned standards.

## Architecture Standards

Standards exist to reduce cognitive load and ensure consistency. They should be few, well-justified, and enforced through automation, not manual review.

### What Should Be Standardized

| Tier | Category | Example Standards | Enforcement |
|------|----------|-------------------|-------------|
| **Tier 1: Mandatory** | Security, compliance, legal | Data encryption, auth patterns, audit logging | Automated (CI pipeline blocks) |
| **Tier 2: Expected** | Architecture, deployment | Service boundaries, API design, container patterns | Reviewed (RFC approval required for exceptions) |
| **Tier 3: Recommended** | Tooling, patterns | CI/CD tool, monitoring approach, logging format | Documented (teams may deviate with justification) |

### Writing Architecture Standards

Each standard should contain:

1. **Title.** What the standard governs.
2. **Rationale.** Why this standard exists. If you can't articulate the benefit, question the standard.
3. **Scope.** What systems/teams this applies to (and what it explicitly does not).
4. **The standard.** The specific requirement. Measurable, testable, unambiguous.
5. **Exception process.** How to request an exception and who can grant it.
6. **Review date.** When this standard will be re-evaluated.

### Standards Anti-Patterns

- **Too many standards.** If everything is a standard, nothing is. Limit Tier 1 and Tier 2 to 15-20 items total.
- **Standards without automation.** If compliance requires a human reviewer, the standard will be applied inconsistently. Automate everything possible.
- **Stale standards.** A standard that hasn't been reviewed in 2+ years is likely causing harm. Sunset or update.
- **The "we've always done it this way" standard.** Justify every standard independently. Past practice is not a rationale.

---

## Architecture Review Board (ARB)

An ARB provides governance for significant architecture decisions. It is not a bottleneck — it is a quality gate and knowledge-sharing mechanism.

### When to Involve the ARB

| Level | Decision Type | Review Process |
|-------|--------------|----------------|
| **L1: Team-level** | Service internal design, API endpoints, database schema | No ARB needed. Team decides. |
| **L2: Cross-team** | New service, shared library, API contract change | ARB notified, lightweight review (1-2 reviewers) |
| **L3: Organization-wide** | New technology, platform change, infrastructure redesign | Full ARB review (RFC + meeting) |
| **L4: Strategic** | Architecture paradigm shift (monolith → microservices, cloud migration) | Executive + ARB joint review |

### ARB Composition

| Role | Responsibility | Count |
|------|---------------|-------|
| **Chair** | Manages agenda, drives decisions, maintains standards | 1 |
| **Principal Architects** | Technical authority, deep domain expertise | 2-4 |
| **Rotating Members** | Cross-functional representation, bring team context | 2-3 (rotating quarterly) |
| **Decision Author** | Presents the proposal, answers questions | 1 per proposal |

### Effective ARB Practices

- **Time-boxed meetings.** One hour max. Decisions should be prepared before the meeting, not debated from scratch.
- **Written proposals required.** No "let's whiteboard it" in the ARB. Proposals must be submitted as RFCs at least 48 hours in advance.
- **Decisions, not discussions.** The ARB's job is to make a decision: approve, approve with conditions, or reject with feedback. Not to explore options.
- **Rotating membership.** Fixed members create an insular culture. Rotate members quarterly to distribute knowledge and prevent groupthink.
- **Appeals process.** Any rejected RFC can be appealed to the CTO or VP Engineering. This prevents the ARB from becoming a bottleneck.

---

## RFC Process

Request for Comments (RFC) is a lightweight process for making significant technical decisions transparent and documented.

### The RFC Lifecycle

1. **Draft.** Author writes the RFC using the template below. Collaborate with stakeholders.
2. **Review.** RFC is open for comments for a minimum period (typically 3-5 business days).
3. **Decision.** The decision-maker (tech lead, ARB chair, CTO) approves, conditionally approves, or rejects.
4. **Implementation.** Approved RFCs are implemented. The RFC becomes the source of truth for the decision.
5. **Retrospective.** After implementation, close the RFC with a summary of what changed from the original design.

### RFC Template

```markdown
# RFC: [Title]

## Status
[Draft | Review | Approved | Rejected | Implemented]

## Summary
[2-3 sentence overview of the proposal]

## Motivation
[Why this change is needed. What problem does it solve? What happens if we don't do it?]

## Design
[The proposed solution. Architecture diagrams, API contracts, data models.]

## Alternatives Considered
[Other approaches and why they were not chosen. Include the runner-up.]

## Trade-offs
[What are we giving up? Performance vs maintainability? Speed vs correctness?]

## Migration Plan
[How do we get from current state to proposed state? Phased approach, timeline, rollback plan.]

## Open Questions
[What we don't know yet. Decisions that are deferred.]

## Appendix
[Any additional context, benchmarks, or references.]
```

### RFC Principles

- **Write-first, talk-second.** Discussions happen on the document. Meetings are for resolving deadlocked issues, not for initial review.
- **Disagree and commit.** Once a decision is made, the team commits to implementing it. Continued debate after a decision undermines the process.
- **Explicit deferral.** "Let's discuss this in the meeting" is fine. "Let's discuss this later" without a specific time is delay. Set a deadline for every deferred question.
- **Retrospectives on rejected RFCs.** If an RFC is rejected, document why. The analysis may be valuable if conditions change later.

### Common RFC Failures

- **The design-by-committee RFC.** Too many authors, too many opinions, no clear vision. RFCs should have one primary author and 1-2 reviewers.
- **RFC as a rubber stamp.** If the decision is already made and the RFC is just documentation, that's fine — but be explicit. "Decision made: we're moving to X. This RFC documents the design and migration plan."
- **Too much detail, too late.** An RFC that describes a fully detailed implementation is harder to change than one that starts with the high-level approach. Get alignment on the approach before diving into implementation details.
- **Death by process.** If every minor change requires an RFC, engineers will stop writing RFCs. Define the threshold clearly.
