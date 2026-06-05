# Scrum-to-Kanban Transition Guide

Moving from Scrum to Kanban is one of the most common engineering transitions, and one of the most frequently mishandled. The failure modes are consistent: misdiagnosing why Scrum isn't working, making the switch without building understanding first, or treating it as a tool swap rather than a system change.

## Step 0: Diagnose First

Before switching, determine whether Scrum is failing due to structural limitations or poor implementation.

**Scrum is structurally the wrong fit when:**
- The team serves multiple stakeholders with competing priorities — the 1 PO:1 team:1 backlog model breaks
- Work is too variable in urgency and size for sprint commitments to be reliable
- The team is a shared service for multiple product portfolios
- Continuous delivery is expected rather than sprint-batch delivery

**Scrum is being implemented poorly when:**
- Engineers don't attend ceremonies or write acceptance criteria
- The product owner won't make hard prioritization calls
- Retrospectives produce no action items
- Velocity is treated as a performance metric rather than a planning input

A clean switch to Kanban will not fix poor implementation discipline. It will produce poorly implemented Kanban instead. Fix the culture first; then consider whether the method needs to change.

## What to Keep, Change, and Drop

### Keep
- **Daily standup** — retained with modified format (right-to-left board walk instead of personal status)
- **Retrospectives** — retained; focus shifts toward flow metrics and WIP health rather than sprint velocity
- **Frequent deliveries** — if the team shipped at sprint end, keep shipping; Kanban enables continuous delivery
- **Explicit planning** — planning doesn't disappear, it becomes more frequent and continuous via Replenishment

### Replace

| Scrum Practice | Kanban Equivalent |
|---------------|-------------------|
| Sprint planning (1 PO, 2-week scope) | Replenishment (multi-PM, 1–2×/week, capacity-allocation-based) |
| Sprint commitment | WIP limits + SLE |
| Sprint Review | Service Delivery Review (bi-weekly/monthly, portfolio-segmented) |
| Sprint burndown | CFD + throughput chart |
| Velocity (story points/sprint) | Throughput (items/week) + cycle time |

### Drop
- Sprint time boxes — no more end-of-sprint scrambles or carried-over work
- Story points and planning poker — replaced by right-sizing at Replenishment + cycle time forecasting
- Sprint scope commitment — replaced by WIP-based flow and SLEs
- Velocity targets — replaced by cycle time improvement and throughput stability

## The Scrumban Bridge

For teams where the organizational disruption of a direct switch is too high, Scrumban is the practical bridge. It retains sprint cadences while progressively adding WIP limits and flow metrics.

**Sequencing:**

1. **Month 1–2:** Add WIP limits to active work columns (In Progress, In Review). Don't change ceremonies yet. Let engineers experience the pull discipline.
2. **Month 2–3:** Add flow metrics — CFD, cycle time scatterplot. Present alongside velocity in sprint reviews. Let the team see what the data reveals.
3. **Month 3–4:** Introduce classes of service for Expedite items. Introduce a Definition of Ready.
4. **Month 4–6:** Replace sprint planning with Replenishment for the most variable work streams. Retain retrospective cadence.
5. **Month 6+:** If the team has built confidence in throughput-based forecasting, drop sprint commitments and time boxes.

The transition is reversible at any step. If Scrumban proves sufficient and full Kanban isn't needed, there is no obligation to continue.

## Changing the Stakeholder Relationship

The most psychologically challenging part is stakeholder communication. Stakeholders accustomed to "we promised Feature X in Sprint 7" will be unsettled by "Feature X has an 85% probability of delivery within 14 days."

**The reframe:** "We are replacing a commitment that frequently didn't hold with a forecast that is calibrated against our actual historical performance. The forecast is honest about uncertainty in a way the sprint commitment was not."

**The conversation:** "Under our Kanban model, I can't give you a hard date — but I can give you a probability. Based on our team's historical throughput and the current queue position, this feature has an 85% chance of completing by April 10. That's based on observed performance, not an estimate. If you need a harder commitment — 95% confidence — that moves to April 18. Which level of certainty do you need to plan around?"

## Common Transition Failure Modes

**1. Everyone-loves-Kanban honeymoon.** The first 2–3 weeks feel liberating (no sprints!). Then the board gets messy, WIP creeps up, and stakeholders realize "no sprint commitment" feels like "no commitment at all." The fix: have WIP limits and SLEs in place before removing sprint commitments.

**2. Sprint planning nostalgia.** PMs keep asking for sprint-level commitments. Engineers keep volunteering dates. The fix: anchor on the SLE and range-based forecasts. Give the same answer every time: "Based on throughput, 2–3 weeks at 85% confidence."

**3. Kanban-in-name-only.** Team switches the Jira project from Scrum to Kanban template but keeps working the same way — assign work in planning, commit to scope, no WIP enforcement. The fix: WIP limits that are actually enforced. A limit that is never hit is not a limit.

**4. Tool-switch without behavior change.** Switching Jira board templates is not a Kanban adoption. The method is about WIP limits, pull discipline, explicit policies, and cadences — not column names in a tool.
