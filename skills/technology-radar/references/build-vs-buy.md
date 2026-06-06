# Build vs Buy Decision Framework

A systematic approach to evaluating whether to build a capability internally or buy/license it from a vendor. The decision is never just about cost — it's about strategic control, opportunity cost, and long-term flexibility.

## Decision Tree

Use this as the first filter before doing any detailed analysis:

```
Is this capability core to our competitive advantage?
├── YES → Is it available to buy with acceptable terms?
│   ├── YES → Buy, but plan to insource over time
│   └── NO → Build (strategic investment)
└── NO → Is it a commodity?
    ├── YES → Buy (cheaper, faster, maintained)
    └── NO → Is the vendor market mature?
        ├── YES → Buy (market has validated solutions)
        └── NO → Build or partner (market is too immature)
```

## TCO Analysis

Total Cost of Ownership over a 3-year period. The first-year cost is often misleading — the true cost comparison requires a multi-year view.

### Build Costs (3-Year TCO)

| Cost Category | Year 1 | Year 2 | Year 3 | Total |
|---------------|--------|--------|--------|-------|
| Engineering (design + build) | $XXX | $XX | $XX | $XXX |
| Infrastructure (hosting, CDN, DB) | $XX | $XX | $XX | $XXX |
| Ongoing maintenance (20% of build/yr) | $0 | $XX | $XX | $XXX |
| Support & on-call rotation | $XX | $XX | $XX | $XXX |
| Documentation & training | $X | $X | $X | $XXX |
| Opportunity cost (what else could this team build?) | $XXX | $XXX | $XXX | $XXX |

### Buy Costs (3-Year TCO)

| Cost Category | Year 1 | Year 2 | Year 3 | Total |
|---------------|--------|--------|--------|-------|
| License/subscription fees | $XX | $XX | $XX | $XXX |
| Implementation & migration | $XX | $0 | $0 | $XX |
| Custom integration | $XX | $X | $X | $XXX |
| Training | $X | $X | $X | $XXX |
| Vendor management overhead | $X | $X | $X | $XXX |
| Renewal escalation (3-10% annual) | $0 | $X | $XX | $XXX |
| Exit cost (if vendor changes terms) | $0 | $0 | $0 | $XXX (contingent) |

### Hidden Costs (Often Missed)

**Build hidden costs:**
- Testing and QA infrastructure
- Security hardening and compliance certification
- Internal user support and troubleshooting
- Documentation maintenance
- Technical debt from rushed delivery
- Knowledge loss if a key engineer leaves

**Buy hidden costs:**
- Data egress/ingress fees
- Integration maintenance across vendor API changes
- Vendor lock-in (data portability, migration cost)
- Feature gaps that require workarounds
- SLA enforcement and vendor management
- Multiple vendor coordination in the same workflow

---

## Decision Matrix

After TCO analysis, score both options against weighted criteria.

### Standard Criteria

| Criterion | Typical Weight | Build Score (1-5) | Buy Score (1-5) |
|-----------|---------------|-------------------|-----------------|
| Strategic alignment | 25% | | |
| Total cost (3-year) | 20% | | |
| Time to value | 15% | | |
| Customizability | 15% | | |
| Maintenance burden | 10% | | |
| Vendor risk/lock-in | 10% | | |
| Team satisfaction | 5% | | |

### Scoring Template

```
Criterion: Strategic alignment
- 5: Directly creates competitive advantage, core to our moat
- 3: Supports the business but not differentiating
- 1: Commodity capability

Criterion: Time to value
- 5: Working in <1 month
- 3: Working in 1-3 months
- 1: Working in >6 months

Criterion: Maintenance burden
- 5: Near-zero maintenance (vendor handles everything)
- 3: Regular maintenance, dedicated team not required
- 1: Requires dedicated team for ongoing maintenance
```

---

## When Build is Right

1. **Core differentiator.** The capability is central to your competitive advantage. Owning it gives you control over your product's future.
2. **No adequate vendor.** The market doesn't offer what you need, or vendors are too immature/unstable.
3. **Existing capability.** You already built something similar. The marginal cost of extending it is lower than buying.
4. **Data advantage.** Your proprietary data makes the build significantly better than any off-the-shelf solution.
5. **Cost structure.** At scale, the build becomes dramatically cheaper than buying (common in infrastructure).

## When Buy is Right

1. **Commodity capability.** Payroll, email, analytics, maps, auth. Don't build what everyone already has.
2. **Speed to market.** The vendor can have you running in days. Building would take months.
3. **Non-core.** The capability is necessary but not differentiating. Buy preserves engineering capacity for what matters.
4. **Mature vendor market.** Multiple vendors compete on the feature you need. Price and quality are market-validated.
5. **Difficult to build well.** Encryption, compliance, payment processing, fraud detection. These domains have deep complexity and regulatory requirements.

## Build vs Buy Anti-Patterns

- **The "it's simple" fallacy.** "How hard can it be to build a chat system?" Very hard, if you need reliability, search, file sharing, compliance, and mobile sync.
- **The "we'll save money" trap.** First-year cost favors build. Three-year TCO with maintenance, support, and opportunity cost often favors buy.
- **Build because we're engineers.** Engineers want to build things. That doesn't mean they should build everything. The company's strategic priorities, not engineering preferences, should drive the decision.
- **Buy because we're in a hurry.** Urgency isn't a decision framework. A rushed buy that doesn't fit the architecture costs more than a delayed build.
- **The "not invented here" syndrome.** Organizational pride in building internally. Recognize it and evaluate honestly.
- **The "invented here" syndrome.** The opposite — assuming external vendors are always better. Apply the same scrutiny either way.
