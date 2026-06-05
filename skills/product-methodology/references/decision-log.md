# Decision Log

Lightweight records for product decisions. Not every decision needs one — but the ones that will be questioned or forgotten do.

## When to Write One

Write a decision log entry when:
- The decision had tradeoffs that could be second-guessed later
- The decision involved multiple stakeholders with different opinions
- The decision sets a precedent for future work
- The decision commits significant resources (3+ weeks of team time)
- You want to revisit the decision in 3-6 months with data

## The Template

```
# Decision: [Title]

**Date:**
**Status:** Proposed / Accepted / Deprecated / Superseded

## Context

What led to this decision? Include the problem, the constraints, and any relevant data. Write enough that someone reading this in 6 months understands why this was even a question.

## Options Considered

### Option A: [Name]
Pros:
- [pro]
- [pro]

Cons:
- [con]
- [con]

### Option B: [Name]
Pros: ...
Cons: ...

### Option C: [Name] (if applicable)
Pros: ...
Cons: ...

## Decision

Chosen: Option [A/B/C]

Rationale: Why this one over the others? What was the decisive factor?

## Expected Outcome

What do we expect to happen as a result of this decision? Be specific enough that you can check later.

- We expect [metric] to move from [baseline] to [target] by [date]
- We expect [behavior/outcome]

## Follow-up

- **Review date:** [When to check if the decision was right]
- **Signal to watch:** [What data would tell us we made the right call]
- **Signal to reconsider:** [What data would tell us we made the wrong call]

## Sign-off

- [Stakeholder/role] — [date]
```

## Examples

### Good

```
# Decision: Prioritize CSV export over dark mode for Q3

Date: 2026-04-15
Status: Accepted

## Context

We have capacity for one medium feature in Q3. Customer support tickets show
15 requests/month for data export vs 3/month for dark mode. Sales calls
consistently mention "we need to get our data out" as a blocker for
enterprise deals. Dark mode is requested by existing users who like the
product; CSV export is requested by prospects who can't buy without it.

## Options Considered

### A: CSV export
Pro: Unblocks 3 enterprise deals in pipeline ($240K ARR)
Pro: Low engineering effort (2 weeks — well-understood pattern)
Con: Less visible to existing users

### B: Dark mode
Pro: High visibility, generates positive social media mentions
Pro: Frequently requested by power users
Con: Higher effort (4-5 weeks — needs design system work)
Con: Doesn't unblock any revenue

## Decision

Option A. The revenue signal is unambiguous. CSV export is a buying
criteria; dark mode is a preference. If CSV export ships in Q3, the
pipeline deals close this year.

## Expected Outcome

- Enterprise pipeline deals close by Q4 2026 ($240K)
- CSV export usage reaches 20% of power users within 2 months
- Support tickets for "how do I export data" drop to near zero

## Follow-up

Review date: 2026-10-01
Signal to watch: CSV export usage rate
Signal to reconsider: If enterprise deals don't mention CSV export as a
blocker in calls, we misprioritized the feature request volume vs revenue
signal
```

### Bad

```
Decision: Build CSV export

The team wants it. RICE score was high.

- A. Developer
```

This entry is useless because:
- No context (what problem? what options?)
- No tradeoffs (what was the cost of NOT building it?)
- No expected outcome (how do we know if it worked?)
- No review date (it disappears into the archive)

A decision log without substance is just a to-do list.
