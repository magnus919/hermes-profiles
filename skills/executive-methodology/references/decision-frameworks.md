# Decision Frameworks

A library of decision-making frameworks for C-suite use. Each framework has a specific domain of applicability. The art is matching the framework to the decision type.

## RAPID (Recommended for decisions with one accountable person)

RAPID assigns each person a role in a decision. Every decision must have exactly one person with a "D" role (Decide). Note: RAPID is not an acronym for the roles in logical order — the order is Recommend, Agree, Perform, Input, Decide.

### The Roles

| Role | Responsibility | Count |
|------|---------------|-------|
| **R**ecommend | Proposes the decision. Gathers data, analyzes options, drafts recommendations. | Typically 1–2 people |
| **A**gree | Must sign off before the decision can proceed. Has veto power. Can send the recommendation back. | 1–3 people |
| **P**erform | Executes the decision once made. Needs to understand the decision but does not shape it. | As many as needed |
| **I**nput | Provides relevant information and perspective. Consulted but not part of the decision. | As many as needed |
| **D**ecide | The single person who makes the final call. This role is not shared. | Exactly 1 |

### Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Multiple Ds | Two execs both think they're the decider. Decision stalls. | Identify the single accountable executive. The other moves to A or I. |
| Everyone is Input | The D gets so much conflicting input they freeze. | Limit Input to those with genuinely relevant data. |
| A as a blocker | An Agree person uses veto to delay instead of improve. | Set a time-box for the Agree phase. After that, the D decides without their sign-off. |
| Skipping Recommend | The D decides without a structured recommendation. | The R role must produce a written recommendation before the D decides. |

### When to Use RAPID

- High-stakes decisions where clarity of ownership is critical
- Decisions that cross organizational boundaries
- Decisions that need input from multiple stakeholders but one accountable person

### When Not to Use RAPID

- Consensus-driven decisions where buy-in from the whole group is the goal (use DACI)
- Low-stakes operational decisions (just decide)
- Decisions where collective ownership matters more than speed

---

## DACI (Recommended for group decisions with a driver)

DACI is similar to RAPID but designed for decisions that benefit from collective discussion and shared ownership. The key difference: DACI has a Driver instead of a Decider, and the Driver's role is to facilitate to consensus rather than to unilaterally decide.

### The Roles

| Role | Responsibility |
|------|---------------|
| **D**river | Facilitates the decision process. Manages timelines, ensures all voices are heard, pushes toward closure. Unlike RAPID's D, the Driver does not unilaterally decide — they facilitate the group to consensus. |
| **A**pprover | The person(s) who must sign off. Has veto power. In DACI, there can be multiple Approvers. |
| **C**ontributor | Provides input, expertise, and perspective. Actively participates in the discussion. |
| **I**nformed | Needs to know the outcome but does not participate in the process. |

### RAPID vs DACI

| Dimension | RAPID | DACI |
|-----------|-------|------|
| Final authority | One Decider | Group consensus facilitated by Driver |
| Speed | Faster — one person decides | Slower — requires consensus |
| Best for | Decisions where speed matters and one person has the scope | Decisions where group buy-in is critical |
| Risk | May leave stakeholders feeling unheard | Risk of lowest-common-denominator decisions |

### DACI Pitfalls

- **Driver becomes Decider.** The Driver gets impatient and unilaterally decides. This breaks the DACI model and destroys trust.
- **Too many Approvers.** Every Approver has veto power. More than two or three Approvers guarantee deadlock.
- **Confusing Contributor with Approver.** Contributors provide input. Approvers can block. These are very different roles and must be assigned separately.

---

## Decision Matrix (Recommended for comparing options against criteria)

A systematic method for evaluating multiple options against weighted criteria. Reduces bias from recency, anchoring, and availability.

### The Method

1. **Define criteria.** What matters for this decision? List all relevant dimensions.
2. **Weight criteria.** Not all criteria are equal. Assign weights summing to 1.0 (or 100%).
3. **Score each option** against each criterion (1–5 or 1–10 scale).
4. **Multiply scores by weights** and sum for each option.
5. **Review and reality-check.** Does the winner feel right? If not, challenge your criteria or weights.

### Example: Buy vs Build Decision

| Criterion | Weight | Build | Buy |
|-----------|--------|-------|-----|
| Time to market | 0.30 | 2 (0.6) | 5 (1.5) |
| Total cost (3yr) | 0.25 | 3 (0.75) | 2 (0.5) |
| Customizability | 0.20 | 5 (1.0) | 2 (0.4) |
| Competitive advantage | 0.15 | 4 (0.6) | 2 (0.3) |
| Maintenance burden | 0.10 | 2 (0.2) | 4 (0.4) |
| **Total** | **1.00** | **3.15** | **3.10** |

**Analysis:** Build and buy are nearly tied. Time-to-market advantage for buy is offset by customizability and competitive advantage for build. Recommendation depends on strategic urgency.

### Pitfalls

- **Weight anchoring.** The first criterion discussed tends to get disproportionate weight. Define criteria independently before assigning weights.
- **False precision.** Scores of 4.3 vs 4.2 suggest precision that doesn't exist. Use whole numbers. Differences of less than 10% are noise.
- **Confirmation scoring.** Scoring to justify a pre-existing preference. If you can predict the winner before scoring, you're doing it wrong.
- **Criterion omission.** If a key dimension (e.g., team morale, regulatory risk) is missing, the matrix will produce a wrong answer even with perfect scores.

---

## Pre-Mortem (Recommended for stress-testing strategic plans)

A pre-mortem is a prospective hindsight exercise. The team imagines that a plan has failed spectacularly, then works backward to identify what went wrong. It surfaces risks that normal planning processes miss.

### The Method

1. **Frame the scenario.** "It's 12 months from now. We executed our plan perfectly, and yet the outcome was a disaster. Write down everything that went wrong."
2. **Silent generation (5 minutes).** Each person writes failures independently. This prevents anchoring and groupthink.
3. **Round-robin sharing.** Each person shares one failure. Continue until all failures are surfaced. No debate during sharing.
4. **Cluster and prioritize.** Group related failures. Vote on the top 5–7 most probable and most impactful failure modes.
5. **Design mitigations.** For each top failure mode, design a prevention or early-detection mechanism.
6. **Assign owners and triggers.** Each mitigation needs an owner and a trigger condition that would activate it.

### Pre-Mortem vs Post-Mortem

| Dimension | Pre-Mortem | Post-Mortem |
|-----------|------------|-------------|
| Timing | Before execution | After failure |
| Cost | Low (1-2 hour meeting) | High (actual failure) |
| Psychological safety | Created explicitly (blame-free future scenario) | Must be created (often difficult after real failure) |
| Actionability | Mitigations can be built into the plan | Lessons applied to future plans |

### Common Failure Categories (use as prompts)

- **Market**: Customer need didn't materialize, competitor moved faster, pricing was wrong
- **Technical**: Architecture didn't scale, integration failed, security vulnerability
- **Organizational**: Wrong team structure, key person left, communication breakdown
- **Execution**: Missed milestones, quality issues, scope creep
- **Financial**: Ran out of money, cost overrun, revenue miss
- **Regulatory**: Compliance issue, legal challenge, policy change
- **External**: Economic downturn, supply chain disruption, geopolitical event

### Pitfalls

- **Skipping silent generation.** If the first person to speak sets the tone, the exercise captures their bias, not the group's collective knowledge.
- **Too much optimism.** Teams often mitigate with "we'll be more careful" rather than concrete structural changes. Push for specific mechanisms.
- **Failure to follow through.** The value is in the mitigations, not the list. If mitigations aren't tracked and implemented, the exercise was theater.
