# Classes of Service in Kanban

Classes of Service (CoS) are the Kanban mechanism for differentiating how work items flow based on their urgency and cost of delay. They are not simply priority levels — each class carries distinct policies for WIP treatment, pull sequence, cycle time expectations, and governance.

## The Four Canonical Classes

### Expedite (Crisis)
**Purpose:** Work with immediate, maximum cost of delay — production incidents causing user harm, active security breaches, regulatory violations with legal consequences.

**Policy:** Pre-empts all other work. Bypasses WIP limits. Team swarms until resolved.

**WIP Limit:** 1 on the Expedite lane — prevents simultaneous crises from fracturing the team.

**Cost of Delay Profile:** Immediate and maximum — delay has high cost right now (exponential).

**SLE Target:** 95% within 24 hours (or faster, depending on severity).

**Common Mistake:** Treating "high priority" as expedite. High-priority work belongs in Fixed Date or Standard with an aggressive queue position. Expedite means crisis — if your expedite lane is never empty, the definition is too loose.

### Fixed Date (Deadline-Driven)
**Purpose:** Work with a specific future deadline and high cost of missing it — regulatory filing dates, contractual milestones, external launch commitments.

**Policy:** Pulled in advance based on throughput forecasting. Must pass Monte Carlo simulation at intake to confirm the deadline is achievable before the team commits.

**Cost of Delay Profile:** Low until deadline, then sharply high (cliff-shaped). Asymmetric risk justifies careful planning.

**Key Practice:** Never accept a Fixed Date commitment without running a forecast against historical throughput data.

### Standard (Default)
**Purpose:** The default class for the majority of feature work and improvements — moderate cost of delay, no specific deadline.

**Policy:** Pulled FIFO within this class. No pre-emption of other Standard items. Subject to normal WIP limits.

**Cost of Delay Profile:** Linear — the cost accumulates steadily but is not acutely high at any specific moment.

**Important:** When Standard items have homogeneous cost of delay (all roughly equivalent business value), relying solely on Standard class is preferred over adding sub-prioritization complexity. More classes add precision but increase complexity.

### Intangible (Investment)
**Purpose:** Work where the cost of delay is not visible in the near term — technical debt reduction, internal tooling, platform reliability, developer experience, training.

**Policy:** Pulled last. Yielded first when higher-class items arrive. May sit in the queue for extended periods.

**Cost of Delay Profile:** Appears near-zero — but chronic deferral silently accumulates the conditions that produce future Expedite emergencies.

**Key Practice:** Track aging Intangible items in the Risk Review. An authentication service that hasn't been updated in 18 months is a future Expedite item in waiting.

## Custom Classes

Teams frequently add a fifth class:

**Bugs** (software teams): Positioned between Fixed Date and Standard. Bugs have higher urgency than Standard features but rarely warrant the full Expedite response. Own SLE: "85% of Bug-class items resolve within 5 days."

**Urgent** (high unplanned request volume): For teams that struggle to decompose work. Positioned between Standard and Fixed Date. Allows prioritization of small unplanned requests (e.g., content updates) without triggering Expedite policies.

## Classes and Forecasting

Per-class cycle time measurement produces far more reliable SLEs and Monte Carlo simulations than system-wide averages. An Expedite item completing in 4 hours and a Standard item taking 14 days must not share a cycle time distribution.

Segregate data by class:
- Standard: 85% within 14 days (derived from Standard item history)
- Expedite: 95% within 24 hours (derived from Expedite item history)
- Fixed Date: committed only at ≥85% Monte Carlo confidence

## Board Implementation

Classes are typically implemented as swimlanes (horizontal bands on the board), one per class. The class is set at intake (Replenishment) or when an incident is raised. It can be escalated (Standard → Expedite when conditions change) but should never be inflated by default.

Typical priority order within the Ready queue:
1. Expedite items first (immediate, bypasses queue)
2. Fixed Date items (by deadline proximity)
3. Bug class items
4. Standard items (FIFO within portfolio allocation)
5. Intangible items (when no higher-class work is Ready)

## Cost of Delay Profiles

The three cost of delay profiles map directly to classes of service:

- **Linear (Standard):** Steady weekly cost of deferral — routine features
- **Cliff (Fixed Date):** Near-zero cost until a deadline, then catastrophic — regulatory, contractual
- **Exponential (Expedite):** Immediate spike — production incidents, active user harm

**CD3** (Cost of Delay Divided by Duration) ranks work by speed of economic return, surfacing which work generates the fastest return on investment rather than merely the highest total value.
