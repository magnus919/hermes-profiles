# WIP Limit Calibration and Little's Law

WIP limits are Kanban's primary mechanism for controlling cycle time, preventing overload, and making systemic problems visible.

## Little's Law: The Mathematical Backbone

**WIP = Throughput × Cycle Time**

Or rearranged for practitioners: **Cycle Time = WIP ÷ Throughput**

This single equation makes explicit the relationship between how much work is in flight, how fast work exits the system, and how long each item waits to be delivered.

**The behavioral implication:** If throughput is roughly stable (which it is in any mature team near capacity), the only way to reduce cycle time is to reduce WIP. Adding more work in flight — expanding WIP limits under stakeholder pressure — produces longer wait times, not faster delivery.

## Setting Initial WIP Limits

The most reliable starting point is a team conversation, not a formula. Ask the team: **"What number of items in progress feels comfortable? Where you're busy and engaged but not overwhelmed?"**

That answer is the initial WIP limit. Treat it as a hypothesis — set it, observe for 2–4 weeks, read the CFD, and adjust.

**Structural principles:**
- WIP limits apply to **activities** (workflow stages), not to roles or people
- Columns should represent **activities**, not specialties
- A common starting heuristic for active work columns: `team_size × 1.5`
- Initial limits for In Review typically match or are slightly lower than In Progress

## WIP Limit Breaches as Diagnostic Signals

A WIP limit breach is not a prompt to raise the limit — it is an alarm mechanism. When the limit is hit, the correct question is "why are we at the limit?"

Common causes of breaches:
- **Items too large** — big items sit in a stage too long, blocking the limit for smaller items behind them. Fix: smaller slices.
- **Bottleneck downstream** — items pile up waiting for the next stage because that stage can't absorb them. Fix: increase throughput at the bottleneck, not the WIP limit upstream.
- **Expedite overuse** — frequent emergency items push over the limit. Fix: tighten expedite criteria or increase the unplanned buffer.
- **External dependencies** — blocked items count against WIP but aren't consuming active capacity. Fix: track blocked items explicitly and consider excluding them from active WIP counts.

## The Little's Law Trap

Adding more WIP in response to stakeholder pressure is the most common WIP calibration mistake. It feels like responsiveness, but Little's Law guarantees it produces slower cycle times.

**Example:** If throughput is stable at 10 items/week and WIP rises from 20 to 30, average cycle time increases from 2 weeks to 3 weeks. Every stakeholder now waits 50% longer.

**The counterintuitive move:** When cycle times are too long, reduce WIP. Finish current work first. The items most urgently needed will reach Done faster because they have a shorter queue to wait behind.

## When to Legitimately Adjust WIP Limits

**Legitimate reasons to increase:**
- Team has grown (new engineers added)
- A chronic blocker category has been resolved
- Retrospective data shows the team is consistently under the limit with low cycle times

**Legitimate reasons to decrease:**
- Cycle times are rising
- The CFD shows WIP widening in a stage
- Team composition has changed (members departed)
- The team identifies cherry-picking behavior during retros

## Little's Law for Bottleneck Identification

Applied per workflow stage, Little's Law becomes a diagnostic tool:
1. Calculate the average items in each stage (in-stage WIP)
2. Calculate the average items exiting per week (throughput out of that stage)
3. Divide: **in-stage Cycle Time = WIP ÷ Throughput**

The stage with the longest in-stage cycle time is the bottleneck. It is not necessarily the stage with the most items — it is the stage where WIP accumulates faster than items exit. This is visible in the CFD as a widening band.
