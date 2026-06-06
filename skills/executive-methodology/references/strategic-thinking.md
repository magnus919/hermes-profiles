# Strategic Thinking Patterns

Mental models for reasoning about complex strategic problems. These patterns are not step-by-step processes — they are cognitive frameworks for reframing problems, challenging assumptions, and anticipating consequences.

## Inversion

Inversion asks: "Instead of asking how to achieve our goal, what would guarantee failure?" By identifying and avoiding failure modes, the path to success often becomes obvious.

### The Method

1. **State the goal.** "We want to increase market share by 20% this year."
2. **Invert the question.** "What would guarantee that we NOT only fail to grow market share, but actually lose share?"
3. **Generate the failure list.** Write down everything that would cause the opposite of the desired outcome.
4. **Check current reality.** Which of these failure modes are we currently exposed to? Which are actively happening?
5. **Mitigate.** Design interventions for the identified failure modes.

### Example

| Goal | Inversion | Failure Modes | Mitigations |
|------|-----------|---------------|-------------|
| Retain top talent | What would make our best people leave? | Bad manager, no growth, unfair comp, boring work | Manager training, career paths, comp benchmarking, stretch projects |
| Launch on time | What would guarantee a slip? | Unclear requirements, under-resourced, scope creep, dependencies | Spec sign-off, dedicated team, change control, dependency tracking |
| Raise Series A | What would make investors pass? | Weak metrics, small TAM, founder risk, no differentiation | Metric improvement, market sizing, hire experienced exec, IP/patents |

### Why It Works

- **Avoidance is easier than achievement.** It's often easier to identify and eliminate failure modes than to design the perfect path to success.
- **Surfaces hidden assumptions.** The inversion exercise forces you to articulate what you're currently not doing that you should be.
- **Pessimism is more creative.** People generate more complete lists when thinking about failure than when thinking about success.

---

## First Principles Thinking

First principles thinking breaks a problem down into its fundamental truths — things that are known to be true — and reasons up from there. It is the opposite of analogical reasoning (copying what others do).

### The Method

1. **Identify the current approach or assumption.** "We need to spend $2M/year on cloud infrastructure."
2. **Deconstruct to first principles.** What are the fundamental physical and economic truths?
   - Compute: we need X CPU-hours at Y cost per hour
   - Storage: we need Z GB at W cost per GB
   - Bandwidth: we need V TB at U cost per TB
3. **Rebuild from first principles.** What would the optimal solution look like if we designed from scratch?
4. **Compare to current approach.** The gap between first-principles cost and actual cost reveals optimization opportunity.

### Application Areas

| Area | Conventional Wisdom | First Principles | Opportunity |
|------|--------------------|------------------|-------------|
| Cloud costs | "We need AWS/Azure/GCP" | "We need compute, storage, and bandwidth at minimum cost" | Reserved instances, spot instances, hybrid, bare metal |
| Hiring | "We need a senior engineer" | "We need a specific outcome delivered" | Contractor, agency, fractional, training a mid-level |
| Pricing | "Price at market rate" | "Price at value delivered minus retention risk" | Value-based pricing above or below market |
| Product | "Build more features to compete" | "What job is the customer hiring us for?" | Focus on the core job, remove waste |

### Pitfalls

- **Stopping too early.** "Because that's how it's done in our industry" is not a first principle. Keep asking "why" until you reach something physically or economically undeniable.
- **First principles paralysis.** Breaking everything down to fundamentals is expensive. Use it for high-stakes problems where reframing could unlock large value. Don't use it for routine decisions.
- **Ignoring transaction costs.** The first-principles optimal solution may require huge organizational change. The cost of change is a real constraint.

---

## Second-Order Effects

Every action produces a first-order effect (the intended outcome) and second-order effects (the consequences of the first-order effect). C-suite decisions should be evaluated at least to the second order.

### The Framework

| Order | Definition | Example: Cutting R&D budget 20% |
|-------|-----------|--------------------------------|
| 1st | Direct, intended effect | Short-term cost savings, improved quarterly P&L |
| 2nd | Consequence of 1st order | Product velocity slows, features slip, team morale drops |
| 3rd | Consequence of 2nd order | Best engineers leave for faster-paced companies, product falls behind competitors |
| 4th+ | Consequence of 3rd order | Revenue growth stalls, company loses market position, deeper cuts needed |

### Heuristics for Second-Order Thinking

1. **Ask "and then what?"** After evaluating the first-order effect, ask: "And then what happens?" Repeat at least twice.
2. **Identify who adapts.** People and competitors change their behavior in response to your actions. A price cut provokes competitor response, which may neutralize the advantage.
3. **Look for delayed effects.** Second-order effects often take quarters or years to materialize. A layoff improves margins this quarter and reduces innovation capacity two years from now.
4. **Consider asymmetric effects.** Some actions have small first-order effects and massive second-order effects (e.g., publicly criticizing a customer). Some have large first-order effects and trivial second-order effects (e.g., changing office supplies vendor).

### Decision Table

| Decision Type | First Order | Second Order Risk | Mitigation |
|--------------|-------------|-------------------|------------|
| Layoffs | Cost reduction | Survivor syndrome, innovation loss, rehiring cost | Treat as last resort, communicate why, invest in survivors |
| Price increase | Revenue per customer | Churn increase, competitor gain | Test with segment, analyze price elasticity |
| Acquisition | Capability/customer acquisition | Integration cost, culture clash, talent loss | Integration plan before signing, retention packages |
| New market entry | Revenue growth | Distraction from core, brand dilution | Ring-fence investment, clear success criteria |

---

## Probabilistic Reasoning

Replace binary thinking (will it happen / won't it) with ranges and probabilities. The goal is not to predict precisely — it's to make decisions that are robust across a range of outcomes.

### The Method

1. **Replace point estimates with ranges.** Not "we'll close Q3 at $10M" but "we'll close Q3 between $9-11M with 80% confidence."
2. **Calibrate regularly.** Make 10 predictions with 80% confidence. If 8 of 10 come true, you're calibrated. If 10 of 10 come true, you're under-confident (your ranges are too wide). If 5 of 10 come true, you're over-confident.
3. **Use scenarios, not single forecasts.** Build base case, upside, and downside scenarios. Assign probabilities to each.
4. **Update beliefs explicitly.** When new information arrives, state your prior belief, the new evidence, and your updated belief. This is Bayesian thinking for executives.

### Common Calibration Errors

| Error | Pattern | Fix |
|-------|---------|-----|
| Over-confidence | "I'm 90% sure" about things that happen 60-70% of the time | Add 20% more uncertainty to every estimate |
| Under-confidence | "Maybe 50% chance" about things that happen 80% of the time | Track predictions. You'll see the pattern. |
| Anchoring | First number discussed anchors all subsequent estimates | Collect independent estimates before sharing any |
| Recency bias | Most recent outcome dominates probability estimate | Track base rates for similar events |

### Expected Value in Strategic Decisions

Expected Value (EV) = (Probability of Success × Value of Success) + (Probability of Failure × Cost of Failure)

Use EV to compare strategies that have different risk/reward profiles. A low-probability, high-reward strategy may have higher EV than a safe, low-reward strategy.

**Example: Market Entry Decision**

| Option | Success Prob | Success Value | Failure Cost | EV |
|--------|-------------|---------------|--------------|-----|
| Enter quickly | 30% | $50M | $5M | (0.3 × 50) - (0.7 × 5) = $11.5M |
| Enter carefully | 60% | $25M | $2M | (0.6 × 25) - (0.4 × 2) = $14.2M |
| Don't enter | 100% | $0 | $0 | $0 |

The careful entry has higher expected value despite lower upside, because of lower failure probability and cost.
