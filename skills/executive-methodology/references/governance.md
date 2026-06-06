# Governance Frameworks

Governance defines who gets to decide what, how risk is managed, and how decisions escalate when they exceed someone's authority. Good governance is invisible — it creates clear boundaries that enable faster, higher-quality decisions.

## Risk Appetite

Risk appetite is the amount of risk an organization is willing to accept in pursuit of its objectives. It is not a single statement — it varies by domain.

### The Framework

| Domain | Risk Appetite Spectrum | |
|--------|----------------------|--|
| **Product Innovation** | Averse → **Moderate** → Aggressive | Most companies are moderate-to-aggressive here |
| **Financial Management** | **Averse** → Moderate → Aggressive | Most companies are conservative here |
| **Compliance & Legal** | **Averse** → Moderate → Aggressive | Zero tolerance for violations |
| **Engineering (uptime)** | **Averse** → Moderate → Aggressive | Depends on SLA commitments |
| **Market Expansion** | Averse → Moderate → **Aggressive** | Growth-stage companies are aggressive here |
| **Talent** | Averse → **Moderate** → Aggressive | Depends on hiring difficulty |

### Defining Risk Appetite Per Domain

For each domain, state:

1. **Boundary conditions.** What is absolutely unacceptable regardless of potential reward? (e.g., "We will never violate data privacy regulations.")
2. **Risk capacity.** How much can we afford to lose in this domain? (e.g., "We can absorb up to $500K of failed innovation experiments per quarter.")
3. **Risk tolerance.** How much variance from plan is acceptable? (e.g., "Revenue can vary ±10% from forecast without triggering escalation.")
4. **Review cadence.** How often is appetite reassessed? (e.g., "Quarterly review with the CEO.") 

### Risk Appetite Statement Template

```
Domain: [Product Innovation]
Appetite: Moderate
Boundary: We will not ship features without customer validation
Capacity: Up to $300K/quarter in experimental initiatives
Tolerance: 40% of experiments may fail to produce measurable value
Review: Quarterly during strategy review
```

---

## Delegation Levels

Decision rights should be pre-delegated so people know what they can decide without escalation. The delegation level varies by decision type, size, and organizational level.

### The Delegation Matrix

| Level | Name | Meaning |
|-------|------|---------|
| L1 | Decide, inform immediately | Full authority. Inform manager after the fact. |
| L2 | Decide, inform before acting | Authority to decide. Must communicate decision before executing. |
| L3 | Recommend, get approval | Prepare recommendation. Manager approves or sends back. |
| L4 | Escalate | Too big or too risky. Manager owns the decision. |

### Delegation by Decision Type (Example: Department Head)

| Decision Type | L1 | L2 | L3 | L4 |
|--------------|----|----|----|-----|
| Hiring (up to budget) | ✓ | | | |
| Hiring (above budget) | | | ✓ | |
| Vendor contracts < $50K | ✓ | | | |
| Vendor contracts $50-250K | | ✓ | | |
| Vendor contracts > $250K | | | | ✓ |
| Team restructuring | | | ✓ | |
| Employee termination | ✓ | | | |
| Org-wide policy change | | | | ✓ |
| Budget reallocation < 10% | ✓ | | | |
| Budget reallocation > 10% | | | ✓ | |
| Public communication | | | | ✓ |

### Delegation Anti-Patterns

- **All L4, all the time.** If every decision is escalated to the next level, you have a bottleneck problem, not a delegation problem. Either the level above is too risk-averse or the level below isn't trusted.
- **Delegation without guardrails.** Giving someone spend authority without limits on what they can spend on. "You can sign contracts up to $50K" must be paired with "on approved vendors in your department."
- **Different rules for different people.** If one director has L2 on hiring and another has L4, the discrepancy must be intentional and communicated.
- **Revoking delegation for convenience.** When a delegated decision goes wrong, the temptation is to pull decision rights back. This punishes everyone for one mistake. Address the individual, not the system.

---

## Escalation Paths

Escalation is not failure — it is a designed mechanism for routing decisions to the right level when they exceed the current level's authority, risk appetite, or capacity.

### When to Escalate

| Trigger | Example |
|---------|---------|
| **Beyond delegation** | Contract value exceeds L1 threshold |
| **Beyond risk appetite** | Opportunity requires accepting product risk above stated appetite |
| **Cross-functional** | Decision affects two departments that disagree |
| **Precedent-setting** | Would set a policy or compensation precedent |
| **Time-critical with unknown risk** | Need to act quickly but the risk profile is unclear |
| **Conflict of interest** | Decision-maker has personal stake in the outcome |

### The Escalation Format

When escalating, provide:

1. **The decision needed.** "Should we approve the $300K contract with Vendor X?"
2. **The recommendation.** "Yes, with the caveats in section 3."
3. **The analysis.** Context, options, trade-offs (2-3 paragraphs max)
4. **What you've already tried.** "We negotiated price down 15%, checked three alternatives, and confirmed budget availability."
5. **Time sensitivity.** "We need an answer by Thursday or we risk losing the discount offer."
6. **What happens if no decision is made.** "The current contract auto-renews at 20% higher cost."

### Escalation Anti-Patterns

- **Escalating decisions you should make.** If you have the authority and the information, decide. Escalating to avoid accountability undermines the delegation system.
- **Dumping without analysis.** "We have a problem, what should we do?" without providing options and a recommendation. The person you're escalating to has less context than you.
- **Escalating too late.** If you escalate a decision that should have been made last week, you've already failed. Escalate as soon as you identify the trigger.
- **Shadow escalations.** Going around your manager to their manager. This destroys trust in the chain. Only acceptable if your manager has failed to act after multiple attempts.

---

## Decision Rights Matrix (RACI for Governance)

A decision rights matrix assigns specific decisions to specific roles. It is more granular than delegation levels and should be maintained as a living document.

### Template

| Decision | Accountable | Consulted | Informed | Decision Process |
|----------|------------|-----------|----------|-----------------|
| Product roadmap priorities | CEO | CPO, CTO, CRO | Board | CEO decides after input from CPO and CTO |
| Engineering tooling standard | CTO | Engineering directors | VP Eng | CTO owns, directors provide input |
| Pricing changes | CEO | CFO, CRO | Board | CEO approves CFO recommendation |
| Hiring freeze/dept | CEO | All execs | HR | CEO decides, execs informed |
| Office location | COO | CEO, CFO | All staff | COO owns, CEO approves |
| Acquisition target > $10M | Board | CEO, CFO | Exec team | Board votes, CEO prepares |

### Maintaining the Matrix

- Review quarterly
- Update when organizational structure changes
- Attach to the executive charter or operating agreement
- Make it accessible to all managers, not just executives
