# Decision Sustainability Framework

A framework for evaluating whether an Architecture Decision Record (ADR) will survive contact with reality. Based on the InfoQ article "Sustainable Architectural Design Decisions" and documented in the community ADR repository.

**Concept origin:** https://www.infoq.com/articles/sustainable-architectural-design-decisions/ — also at `locales/en/documents/decision-sustainability-criteria/` and `locales/en/documents/guidelines-to-achieve-sustainable-decisions/` in the ADR community repo.

## Five Sustainability Criteria

Every ADR should be evaluated against these criteria before acceptance. They form a quality gate checklist for the ADR review process.

### 1. Strategic

**Question:** Does this decision consider long-term impact?

A strategic decision accounts for future operations, maintenance, and evolution — not just the immediate problem. It explicitly addresses the downstream consequences of the choice.

**Checklist:**
- [ ] What is the projected lifespan of this decision? (6 months? 2 years? 10 years?)
- [ ] How will this decision affect future maintenance burden?
- [ ] Does this decision lock the team into a specific technology or pattern?
- [ ] Are the switching costs documented?

**Pitfall:** A decision that optimizes for today at the expense of the next 6-12 months may still be correct — but only if the short-term horizon is explicit in the rationale.

### 2. Measurable and Manageable

**Question:** Can this decision be objectively evaluated over time?

A sustainable decision has measurable outcomes. You should be able to look back in 6 months and determine whether the decision was correct.

**Checklist:**
- [ ] Are the criteria for success or failure defined?
- [ ] Are numeric targets specified where possible? (latency p99 < 200ms, cost < $500/mo)
- [ ] Is the decision granular enough to be traceable? (too fine-grained = noise, too coarse = ambiguity)
- [ ] Are dependencies between this decision and other decisions documented?

**Pitfall:** "Improve performance" is not measurable. "Reduce p99 latency from 800ms to under 200ms" is measurable. Quality attribute scenarios (from arc42) are the right tool here.

### 3. Achievable and Realistic

**Question:** Is this the "good enough" choice, not the perfect one?

A sustainable decision is grounded in what the team can actually deliver. Over-engineering for hypothetical future needs is a common failure mode.

**Checklist:**
- [ ] Can the team implement this given current skills and capacity?
- [ ] Does this decision avoid over-engineering? (Is there a simpler alternative that was considered and rejected for a documented reason?)
- [ ] Is the implementation timeline realistic?
- [ ] Are the operational costs within budget?

**Pitfall:** A technically elegant decision that the team cannot execute is a failure of architecture, not of the team. The "good enough" test: does this decision get us 80% of the benefit with 20% of the complexity?

### 4. Rooted in Requirements

**Question:** Does this decision trace back to real business or technical requirements?

A sustainable decision is grounded in the actual problem — company context, team makeup, user needs — not an abstract "best practice."

**Checklist:**
- [ ] Is this decision directly tied to a specific requirement or constraint?
- [ ] Have team skills, training budget, and organizational context been considered?
- [ ] If the requirements change, would this decision need revisiting? (If yes, flag it.)
- [ ] Are external dependencies (vendors, platforms, regulations) documented?

**Pitfall:** "Everyone uses Kubernetes" is not a requirement. "We need horizontal scaling for predictable traffic patterns our current single-server setup can't handle" is a requirement. Decisions rooted in bandwagon effects rather than actual requirements age poorly.

### 5. Timeless

**Question:** Is this decision based on knowledge unlikely to be outdated soon?

A sustainable decision favors durable knowledge over fashionable technology. Platform-neutral patterns and architectural tactics outlast specific tools.

**Checklist:**
- [ ] Is the decision based on architectural patterns/tactics rather than specific tool versions?
- [ ] If the chosen vendor/product disappeared tomorrow, would the architecture survive?
- [ ] Is the rationale still valid if underlying technology choices change?
- [ ] Does the ADR distinguish between "what" (the pattern) and "which" (the specific tool)?

**Example:** Choosing event sourcing because "we need an audit trail" is a timeless architectural decision. Choosing event sourcing because "Kafka is trendy" is not. The ADR should articulate the timeless principle, not just the tool choice.

## Eight Guidelines for Sustainable Decisions

From the InfoQ article, these guidelines help put the criteria into practice:

| # | Guideline | Applies to |
|---|-----------|-----------|
| 1 | **Use a lean/minimalistic approach for initial documentation.** Don't write a Tyree & Akerman on day one. Start with Nygard or MADR. | ADR drafting |
| 2 | **Prioritize and capture all important decisions first.** Identify what matters before elaborating. | ADR identification |
| 3 | **Detail important decisions after initial approval.** Full-blown templates come after stakeholders agree the direction is right. | ADR review |
| 4 | **Use lean versions for trivial decisions.** Not every decision needs Options Analysis. For obvious choices, a paragraph in the index or a Nygard ADR is enough. | Template selection |
| 5 | **Reuse existing architectural knowledge.** Don't reinvent patterns documented in arc42, Martin Fowler, or your own past ADRs. Reference them. | ADR writing |
| 6 | **Establish traceability links between decisions, requirements, and code.** Every ADR should link back to the requirement that drove it and forward to the code that implements it. | ADR structure |
| 7 | **Provide automated consistency checking for traceability links.** See `references/fitness-functions.md` for how to make this mechanical. | CI/governance |
| 8 | **Enforce justifications forcefully.** The rationale is the most important part of any ADR. A decision without justification is not a decision — it's an opinion. | ADR quality |

## Using the Framework: ADR Review Checklist

Before accepting an ADR, evaluate it against these questions:

```
1. STRATEGIC — Does this consider long-term impact beyond the immediate problem?
   If no: add a "Future considerations" section to the ADR.

2. MEASURABLE — Are success/failure criteria defined, ideally with numeric targets?
   If no: add quality attribute scenarios before accepting.

3. ACHIEVABLE — Is this "good enough," not over-engineered for hypothetical futures?
   If no: document what simpler alternatives were considered and why the extra complexity is justified now.

4. ROOTED — Does this trace back to a specific requirement, constraint, or team context?
   If no: identify the actual requirement and link it. If none exists, re-evaluate whether the decision is needed.

5. TIMELESS — Is the rationale based on durable architectural knowledge, not today's trends?
   If no: reframe the ADR to articulate the architectural principle, not the specific tool name.
```

## Further Reading

- InfoQ — "Sustainable Architectural Design Decisions": https://www.infoq.com/articles/sustainable-architectural-design-decisions/
- ADR community repo — sustainability criteria: https://github.com/architecture-decision-record/architecture-decision-record (see `locales/en/documents/decision-sustainability-criteria/` and `guidelines-to-achieve-sustainable-decisions/`)
