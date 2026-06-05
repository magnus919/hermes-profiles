# Flow Metrics in Kanban

Kanban replaces story point velocity with four core flow metrics. These metrics are derived from observed system behavior, not estimates, making them more honest and more actionable.

## The Four Core Metrics

### 1. WIP (Work in Progress)
The number of items that have entered the active workflow but have not yet reached Done.

**How to measure:** Count the items in all active columns (Ready + In Progress + In Review, depending on board design). The CFD shows this as the vertical distance between the entry band and the Done band.

**What it tells you:** Whether the team is overloaded. Rising WIP with flat throughput signals trouble — per Little's Law, cycle times are about to increase.

### 2. Cycle Time (or Lead Time)
The total time from when an item is committed (pulled into active work) to when it reaches Done.

**How to measure:** For each completed item, record the date it entered active work and the date it completed. Plot on a **cycle time scatterplot** — X = completion date, Y = cycle time in days. Draw percentile lines (50th, 85th, 95th).

**What it tells you:** Delivery predictability. The 85th percentile is the standard Service Level Expectation (SLE) threshold. If the 85th percentile is 14 days, then 85% of items complete within 14 days.

### 3. Throughput
The number of items completed per unit of time (typically per week).

**How to measure:** Count items reaching Done each week. Track as a time-series chart. A mature team's throughput will be relatively stable over time (fluctuating within a predictable range).

**What it tells you:** System capacity. Throughput is the denominator in Little's Law and the input to Monte Carlo simulations for forecasting.

### 4. Flow Efficiency
The ratio of active work time to total cycle time.

**Formula:** Active Time ÷ Total Cycle Time × 100

**How to measure:** Requires separating each workflow stage into active and queue states (e.g., "In Progress (active)" vs. "Ready for Review (queue)"). Active time = sum of time in active states; total cycle time = complete duration.

**What it tells you:** How much of your delivery time is actually productive work vs. waiting.
- **Typical starting range:** 1–15% (meaning 85–99% of time is waiting)
- **Mature, optimized teams:** ~40% (considered the practical upper bound)

## Service Level Expectations (SLEs)

An SLE is a published, data-derived probability statement: "Based on our historical performance, 85% of Standard work items complete within 14 days of being pulled into active work."

**How to derive an SLE:**
1. Collect cycle times for all completed items in the last 10–12 weeks
2. Filter by class of service
3. Plot on a scatterplot
4. Draw the 85th percentile line — this is your SLE

**Why 85th percentile:** High enough to be meaningful (most items fall within it) while excluding long-tail outliers that would inflate the number to uselessness.

**SLE vs. SLA vs. Sprint Commitment:**

| Mechanism | What it is | Enforced how |
|-----------|-----------|-------------|
| **SLA** | Contracted obligation | Penalties, escalation |
| **Sprint commitment** | Team promise | Social obligation; frequently missed |
| **SLE** | Data-derived forecast | Continuous monitoring; transparency |

SLEs replace sprint commitments. The key difference: sprint commitments are judged at sprint end with no visibility in between. SLEs are continuous — every item is monitored against the SLE daily, and approaching items are surfaced in standup before they breach.

## Cumulative Flow Diagrams (CFD)

The CFD is the single most information-dense chart available to a Kanban team. It simultaneously encodes WIP, cycle time, throughput, and flow health patterns.

**Reading a CFD:**
- **X-axis:** Calendar time
- **Y-axis:** Cumulative item counts per workflow stage
- **WIP:** Vertical distance between entry and Done bands
- **Cycle Time:** Horizontal distance between entry and exit
- **Throughput:** Slope of the Done band (steeper = faster delivery)

**Diagnostic patterns:**
- **Widening band:** WIP accumulating in that stage — bottleneck.
- **Flat line:** Zero items exited that stage — complete blockage.
- **Stair-step Done band:** Batch delivery, not continuous flow.
- **Narrowing band:** Stage is completing faster than new items arrive — possible upstream starvation.
- **S-curve:** Periods of zero WIP (feast-famine replenishment).

## Forecasting: Individual Items

Use the cycle time scatterplot. Instead of estimating how long an item will take, say:

> "This item just entered Ready. Our 85th percentile for Standard items is 14 days. There's an 85% chance it completes within 14 days."

No estimate required. The forecast is based on actual historical data.

## Forecasting: Initiatives and Backlogs

Use **Monte Carlo simulation** sampling from historical weekly throughput:

> "This backlog has 30 items. Our throughput is 6–8 items per week. Monte Carlo gives us: 50% confidence by week 5, 85% by week 7, 95% by week 9."

**Always give a range** — never a point estimate. Always state the confidence level. Always state the assumptions (no major incidents, stable staffing).

## Right-Sizing for Reliable Forecasting

Throughput-based forecasting requires consistent item sizes. If items vary from 1 day to 3 weeks, the cycle time scatterplot becomes a wide cloud and confidence intervals span months.

**Right-sizing vs. Same-sizing:** Right-sizing means decomposing work to the smallest customer-valuable unit that fits within the SLE threshold — not making all items the same size. The anchor: before pulling an item, ask "are we 85% confident this will complete within our SLE?" If not, can it be sliced?

**Wrong decomposition** (technical layers, no independent value at each step): "Build schema" / "Build API" / "Build frontend" — all three required before anything is evaluatable.

**Right decomposition** (customer value at each step): "Users can submit the form (basic flow)" / "Connect submission to backend" / "Add validation" — each is independently evaluatable.
