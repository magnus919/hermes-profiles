# Multi-Portfolio Kanban Operating Model

When a single engineering team serves multiple product portfolios simultaneously, classic Scrum breaks down — its 1:1:1 assumption (one Product Owner, one team, one backlog) cannot handle the reality of multiple stakeholders with competing priorities. Multi-Portfolio Kanban addresses this structural failure.

## Core Insight: Engineering as a Service

Treat the shared engineering group not as a team juggling multiple masters, but as a **service** with multiple clients. Services have explicit capacity, published service-level expectations, governed intake processes, and regular performance reviews. The clients compete transparently for service capacity under visible, agreed rules.

## Capacity Allocations

Leadership sets a baseline capacity split — a percentage of throughput earmarked for each portfolio over a planning horizon (typically a quarter):

| Portfolio | Allocation | Notes |
|-----------|-----------|-------|
| Portfolio A | 60% | Primary product line |
| Portfolio B | 30% | Internal platform |
| Unallocated buffer | 10% | Incidents, tech debt, unplanned |

These allocations are:
- Applied at Replenishment when deciding what enters the Ready queue
- Tracked against actual throughput in Service Delivery Reviews
- Adjusted through formal channels when priorities shift — not through ad hoc escalation

Capacity allocations eliminate the need for stack ranking portfolios. No PM needs to "win" against another PM. Each portfolio has a guaranteed share.

## Board Design

One single board for all portfolios — not one per portfolio. The board is the team's operating reality and must show everything in one place.

**Swimlanes** (JQL-based in Jira, or equivalent):
- **Expedite** lane at top (WIP limit 1) — pinned above all portfolios
- **Portfolio A** lane
- **Portfolio B** lane
- **Everything Else** lane — tech debt, internal work, team improvement

**Columns** representing actual workflow stages:
- Backlog (not counted in WIP)
- Ready (committed, meets Definition of Ready)
- In Progress (active development — WIP limited)
- In Review (code review, QA — WIP limited)
- Done

**Card colors** by portfolio for at-a-glance allocation visibility during standup.

## Cadences for Multi-Portfolio

**Replenishment (1–2×/week, 30–60 min):** Replaces sprint planning. All PMs attend with the EM/TL. The team selects what enters Ready based on WIP capacity and allocation percentages. All new work enters through Replenishment — no side-channel asks to engineers.

**Service Delivery Review (bi-weekly or monthly, 60–90 min):** The primary governance loop. EM/TL presents metrics by portfolio: throughput vs. allocation, lead time percentiles, blocker frequency, SLE hit rate. PMs formally assert whether their portfolio is under- or over-served. Capacity allocations are adjusted here with data, not politics.

**Team Retrospective (every 2–4 weeks, 60 min):** Inward-focused. Engineers surface context-switching burden, expedite frequency, handoff friction, and replenishment quality. PMs do not attend — their concerns belong in the SDR.

## Side-Channel Asks: The Most Common Failure Mode

The most common failure in multi-portfolio governance is the direct ask — a PM messages an engineer directly, or a senior leader asks someone to "just squeeze this in." These asks are invisible to the board, consume real capacity, and violate allocations.

**The fix:** All work enters through Replenishment. The EM/TL tells engineers: "If anyone asks you to work on something not on the board, the answer is 'please bring it to Replenishment.'" PMs are told: "I will route any direct asks back to you for submission through Replenishment."

## Role Shifts

**EM/TL** moves from "sprint runner" to "service owner for flow" — accountable for the Kanban system design, enforcing WIP and policies, blocking side doors, and providing range-based forecasts.

**PM** moves from owning a dedicated squad to competing transparently for shared capacity. Their preparation discipline matters more: small, well-defined, high-value candidates are selected first. The primary governance lever is the Service Delivery Review, not the sprint negotiation.

**CTO/CPO** sets baseline allocation splits, reviews systemic bottlenecks in Risk Reviews, and resolves allocation disputes that can't be resolved at the team level.
