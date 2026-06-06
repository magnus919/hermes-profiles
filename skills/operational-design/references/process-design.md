# Process Design

Frameworks for understanding, documenting, and improving business processes. Process design is the foundation of operational excellence — you cannot improve what you haven't mapped.

## Value Stream Mapping (VSM)

A lean-management technique for analyzing the flow of materials and information required to deliver a product or service to a customer.

### Standard VSM Elements

| Symbol | Name | Meaning |
|--------|------|---------|
| □ | Process box | A process step (department, system, person) |
| ▼ | Inventory | Work-in-progress between steps |
| → | Push arrow | Material moves without pull signal |
| ☰ | Information flow | Communication (manual or electronic) |
| ⚡ | Kaizen burst | Improvement opportunity identified |
| ⏰ | Timeline | Value-added vs non-value-added time |

### Building a Current-State VSM

1. **Define the product/service.** What's the specific product, order, or request you're mapping?
2. **Walk the process.** Physically follow the work from start to finish. Don't map from memory.
3. **Map process steps.** Each major step is a process box. Include wait states and handoffs.
4. **Collect data for each step:**
   - Cycle time (time to complete the step)
   - Changeover time (time to switch between types)
   - Uptime / reliability
   - First-pass yield (% of work done right first time)
   - Number of operators
5. **Map information flow.** How does each step know what to do? Email? System? Verbal?
6. **Add the timeline.** Calculate value-added time vs total lead time.

### Value-Added vs Non-Value-Added

| Category | Definition | Examples |
|----------|-----------|----------|
| **Value-Added (VA)** | Changes the product/service in a way the customer cares about and pays for | Manufacturing, code development, customer consultation |
| **Business Non-Value-Added (BNVA)** | Required by regulation or business policy but not valued by customer | Compliance checks, reporting, approvals |
| **Non-Value-Added (NVA)** | Pure waste. Customer would not pay for this. | Rework, waiting, handoffs, unnecessary steps |

### The Efficiency Metric

```
Process Cycle Efficiency = Total Value-Added Time / Total Lead Time
```

| Efficiency | Classification |
|------------|---------------|
| > 25% | Excellent. Lean process. |
| 10-25% | Good. Room for improvement. |
| 5-10% | Typical for most organizations. Significant waste. |
| < 5% | High waste environment. Major opportunity. |

---

## BPMN (Business Process Model and Notation)

A standardized notation for process modeling. Use BPMN when you need formal, unambiguous process documentation.

### Core Elements

| Element | Notation | Meaning |
|---------|----------|---------|
| Event | Circle | Something that happens (start, end, timer, message) |
| Activity | Rounded rectangle | Work performed (task, subprocess) |
| Gateway | Diamond | Decision point (XOR, AND, OR) |
| Sequence Flow | Solid arrow | Order of activities |
| Message Flow | Dashed arrow | Communication between participants |
| Pool | Large rectangle | A participant in the process |
| Lane | Nested section within a pool | Role or department within a participant |

### Gateway Types

| Gateway | Logic | Visual | Use When |
|---------|-------|--------|----------|
| **XOR (Exclusive)** | Exactly one path | Standard diamond | Yes/No decisions, routing |
| **AND (Parallel)** | All paths execute | Diamond with + | Tasks can happen simultaneously |
| **OR (Inclusive)** | One or more paths | Diamond with O | Multiple conditions may be true |

---

## Bottleneck Analysis

In any process, the slowest step determines the throughput of the entire system. Bottleneck analysis identifies that step.

### Theory of Constraints (Goldratt)

1. **Identify** the constraint (the bottleneck). The step with the smallest capacity or longest cycle time.
2. **Exploit** the constraint. Maximize the bottleneck's throughput. Don't let it wait.
3. **Subordinate** everything else. Non-bottleneck steps should operate at the bottleneck's pace, not at their own maximum.
4. **Elevate** the constraint. If exploitation isn't enough, invest in increasing the bottleneck's capacity.
5. **Repeat.** Once the bottleneck is resolved, a new bottleneck appears. Start over.

### Finding the Bottleneck

| Method | How | Best For |
|--------|-----|----------|
| **Walk the process** | Stand where the work is. Where is the pile of work-in-progress largest? | Quick assessment, small processes |
| **Capacity analysis** | Calculate maximum throughput of each step. Lowest = bottleneck. | Manufacturing, transactional |
| **Cycle time analysis** | Measure actual time per step. Longest = bottleneck. | Knowledge work, services |
| **Queues** | Where is the longest queue? The step before the queue is the bottleneck. | All processes |

### Bottleneck Anti-Patterns

- **Optimizing non-bottlenecks.** Improving a step that isn't the bottleneck increases capacity overall by 0%. It just creates more work-in-progress queued at the bottleneck.
- **Keeping the bottleneck idle.** Lunch breaks, meetings, training. If the bottleneck stops, the whole system loses throughput. Protect the bottleneck's time.
- **Ignoring variability.** A step may not look like the bottleneck on average, but if its variability is high, it causes intermittent bottlenecks.

---

## Workflow Optimization Patterns

### The Seven Wastes (TIMWOOD)

| Waste | Description | Example in Knowledge Work |
|-------|-------------|--------------------------|
| **T**ransportation | Unnecessary movement of work | Multiple handoffs between teams |
| **I**nventory | Excess work-in-progress | Too many open tickets |
| **M**otion | Unnecessary movement of people | Context switching, finding information |
| **W**aiting | Idle time between steps | Approval queues, review backlogs |
| **O**ver-processing | Doing more than needed | Excessive documentation, over-engineering |
| **O**ver-production | Doing work before it's needed | Building features without demand |
| **D**efects | Errors requiring rework | Bugs, miscommunication, incorrect data |

### Process Improvement Heuristics

| Heuristic | When to Apply | Expected Impact |
|-----------|--------------|-----------------|
| Eliminate handoffs | Process has 5+ handoffs | High — each handoff adds delay and error |
| Parallelize independent steps | Sequential steps that don't depend on each other | Medium-High — reduces lead time significantly |
| Move decisions earlier | Late-stage approvals cause rework | High — fail fast, not late |
| Automate verification | Manual checking is slow and inconsistent | Medium — improves consistency more than speed |
| Standardize exceptions | The same exception gets handled differently every time | High — reduces cognitive load and error |
| Batch size reduction | Large batches increase lead time and variability | Medium — smoother flow, faster feedback |
| Remove sign-off layers | 3+ approvals for routine decisions | High — approvals are delays, not quality |

### Measuring Improvement

| Metric | Pre-optimization | Post-optimization | Target |
|--------|-----------------|-------------------|--------|
| Lead time (end-to-end) | | | |
| Value-added time | | | |
| First-pass yield | | | |
| Handoff count | | | |
| Approval steps | | | |
| Rework rate | | | |
| Cost per transaction | | | |
