# Kanban Glossary

## A–C

**Aging Chart** — A view plotting every in-flight item by age (days in workflow) versus current stage. Items color-coded against the SLE threshold: green (within range), yellow (approaching), red (exceeded). Replaces sprint commitment as the primary accountability mechanism.

**Blocker** — An impediment preventing a work item from progressing. Tracked in a blocker log with duration and root cause category. A blocker category accounting for >20% of blocked time is a systemic risk, not a one-off.

**Cadence** — A recurring coordination meeting with fixed frequency, duration, participants, and purpose. Kanban defines seven cadences from daily (Standup) to quarterly (Strategy Review).

**Capacity Allocation** — The percentage of a shared team's throughput earmarked for each portfolio over a planning horizon. The foundational governance mechanism for multi-portfolio Kanban. Set by leadership quarterly, tracked in Service Delivery Reviews.

**CD3 (Cost of Delay Divided by Duration)** — A prioritization heuristic that ranks work by economic return speed. CD3 = Cost of Delay ÷ Duration. Higher CD3 values indicate work that should be pulled first when capacity is scarce.

**CFD (Cumulative Flow Diagram)** — A stacked area chart plotting cumulative work item counts per workflow stage over time. Simultaneously encodes WIP (vertical band width), cycle time (horizontal distance through bands), and throughput (slope of Done band).

**Class of Service (CoS)** — A policy framework differentiating how work items are treated based on urgency and cost of delay. Four canonical classes: Expedite, Fixed Date, Standard, Intangible. Each has distinct WIP treatment, pull sequence, and SLE.

**Cost of Delay** — The economic cost of deferring a work item by one unit of time. Three profiles: Linear (steady cost), Cliff (near-zero until deadline, then catastrophic), Exponential (immediate spike).

**Cycle Time** — The time from when an item enters active work (committed) to when it reaches Done. The primary delivery predictability metric. Measured per-class and expressed as percentiles (50th, 85th, 95th).

## D–F

**Definition of Done (DoD)** — The exit criteria for each workflow stage. Explicit conditions an item must meet before moving to the next column. Without explicit DoD, items move prematurely, creating rework and inflated cycle time.

**Definition of Ready (DoR)** — The entry criteria for the Ready queue. Items that don't meet the DoR are returned for clarification before entering active work. Typical: clear problem statement, acceptance criteria, independently deliverable, right-sized.

**Expedite** — The highest class of service. For work with immediate, maximum cost of delay. Bypasses WIP limits. WIP limit of 1 on the Expedite lane. Team swarms until resolved. Not "high priority" — crisis.

**Explicit Policies** — The fourth core Kanban practice. Written, visible, jointly-agreed rules governing how work moves through the system. Required properties: sparse, simple, well-defined, visible, always applied, readily changeable.

**Fixed Date** — A class of service for work with a specific future deadline and high cost of missing it. Requires Monte Carlo forecasting at intake. Never accept a Fixed Date commitment without running a forecast.

**Flow Debt** — The accumulated cost of systematically bypassing blocked or aging items in favor of fresh, easy work. Cherry-picking feels locally rational but produces systemic slowdown as avoided items age into crises.

**Flow Efficiency** — The ratio of active work time to total cycle time. Formula: Active Time ÷ Total Cycle Time × 100. Typical starting range: 1–15%. Mature optimum: ~40%. Requires separating active and queue states on the board.

## I–P

**Intangible** — The lowest class of service. Work with no visible near-term cost of delay: tech debt, internal tooling, platform reliability. Pulled last. Chronic deferral silently accumulates future Expedite conditions.

**Kanban** — A pull-based flow management system for knowledge work. Originating in Toyota's manufacturing system, adapted for knowledge work by David J. Anderson. Governed by four core principles and six core practices.

**Lead Time** — Often used interchangeably with cycle time. Some teams distinguish: lead time = time from request (backlog entry) to done; cycle time = time from commitment (pulled into active work) to done.

**Little's Law** — The mathematical relationship governing flow systems: WIP = Throughput × Cycle Time. Derived from queuing theory. Explains why reducing WIP is the most reliable path to faster delivery.

**Monte Carlo Simulation** — A forecasting technique that samples from historical throughput distributions to generate probability ranges for project completion dates. Replaces sprint commitment with evidence-based ranges.

**Multi-Portfolio Kanban** — An operating model for shared engineering teams serving multiple product portfolios simultaneously. Uses capacity allocations, a single board, and structured cadences to replace political negotiation with policy.

## P–Z

**Pull System** — Work moves forward when downstream capacity exists, not when upstream is ready. Engineers take new work only when a column drops below its WIP limit, not when assigned by a manager.

**Replenishment** — The cadence where work enters the Ready queue. Multi-PM intake forum. Applies capacity allocations, enforces Definition of Ready. All new work enters through Replenishment — no side-channel asks.

**Right-Sizing** — Decomposing work to the smallest customer-valuable unit that fits within the SLE threshold. Distinct from same-sizing (making all items identical size). Right-sizing enables reliable throughput-based forecasting.

**Service Delivery Review (SDR)** — The primary governance cadence for shared teams. Data-driven review of throughput vs. allocation, SLE adherence, blocker patterns. Where capacity allocation adjustments are debated and decided.

**Side-Channel Ask** — Work requested directly to an engineer outside the board and Replenishment process. The most common failure mode in multi-portfolio governance. The fix: all work through Replenishment, no exceptions.

**SLE (Service Level Expectation)** — A data-derived probability statement about delivery time: "85% of Standard items complete within 14 days." Replaces sprint commitments as the primary delivery communication mechanism.

**STATIK (Systems Thinking Approach to Implementing Kanban)** — A framework for designing Kanban systems per-team rather than applying a template. Analyzes sources of dissatisfaction, demand, capability, workflow, classes of service, and metrics.

**Throughput** — The number of items completed per unit time (typically per week). Kanban's replacement for velocity. Used as input to Monte Carlo simulations and SLE derivation.

**Upstream Kanban** — An extension of the pull model into pre-delivery phases. The backlog is a collection of options, not commitments. Commitment happens at the latest responsible moment — when an item enters Ready.

**WIP (Work in Progress)** — Items that have entered the active workflow but have not yet reached Done. The primary control variable in Kanban. Managed through WIP limits.

**WIP Limit** — The maximum number of items allowed in a workflow stage simultaneously. The primary flow control mechanism. A breach is a diagnostic signal, not a prompt to raise the limit. Enforced by team agreement, not by tooling.

**WIP Limit Trap** — The mistake of raising WIP limits in response to stakeholder pressure or capacity demand. Per Little's Law, this increases cycle time — making every stakeholder wait longer.
