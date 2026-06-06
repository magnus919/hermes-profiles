# Unit Economics

Unit economics is the foundation of financial analysis for any business that sells to customers. It answers the question: "Do we make money on each customer, and how long does it take to recover our investment?"

## Core Metrics

### CAC (Customer Acquisition Cost)

Total cost of acquiring a new customer.

```
CAC = Total Sales & Marketing Spend (period) / New Customers Acquired (period)
```

**What to include:**
- Sales team salaries, commissions, and bonuses
- Marketing team salaries
- Advertising spend (all channels)
- Sales tools (CRM, sales engagement, prospecting)
- Marketing content production
- Events and sponsorships
- Sales enablement
- Allocated overhead (office, management, shared services)

**What NOT to include:**
- Product/engineering costs (those are R&D, not acquisition)
- Customer success/support (those are retention, not acquisition)
- G&A (general and administrative overhead)

**Blended vs Paid CAC:**

| Metric | Formula | Use Case |
|--------|---------|----------|
| **Blended CAC** | Total S&M / Total new customers | Overall efficiency of all channels |
| **Paid CAC** | Paid marketing spend / Customers from paid channels | Efficiency of paid acquisition specifically |
| **Organic CAC** | Organic S&M cost / Customers from organic channels | Efficiency of organic/inbound channels |

### LTV (Lifetime Value)

Total revenue a customer generates over their entire relationship with the company.

**Simple LTV (Gross Margin based):**

```
LTV = ARPU × Gross Margin × Average Customer Lifetime (months)

Where: Average Customer Lifetime = 1 / Monthly Churn Rate
```

**Cohort LTV (more accurate):**

Track actual revenue from a cohort of customers over time, accumulating until the cohort stabilizes. This captures expansion revenue, contraction, and churn patterns that simple LTV misses.

| Metric | Simple LTV | Cohort LTV |
|--------|-----------|------------|
| Accuracy | Low — assumes constant ARPU | High — captures actual behavior |
| Time to compute | Instant — uses averages | 12-24 months of data needed |
| Expansion revenue | Not included | Included |
| Use when | Early stage, little data | Growth stage+, sufficient history |

### Payback Period

How long it takes to earn back the cost of acquiring a customer.

**Gross Margin Payback Period:**
```
Payback (months) = CAC / (ARPU × Gross Margin %)
```

**Simple Payback Period (no gross margin):**
```
Payback (months) = CAC / ARPU
```

| Payback Period | Health |
|---------------|--------|
| < 6 months | Excellent |
| 6-12 months | Good |
| 12-18 months | Acceptable (depends on churn) |
| 18+ months | Dangerous (unless very low churn) |

### Contribution Margin

Revenue from a customer minus the variable costs of serving them. Unlike gross margin, contribution margin includes all variable costs.

```
Contribution Margin = Revenue - COGS - Variable Operating Costs
```

| Included | Not Included |
|----------|-------------|
| Hosting/infrastructure per customer | R&D |
| Customer support cost | G&A |
| Payment processing fees | S&M (treated separately for CAC) |
| Onboarding services | Fixed overhead |
| Per-seat licensing costs | |

---

## Interpreting Unit Economics

### The LTV/CAC Ratio

```
LTV/CAC Ratio = LTV / CAC
```

| Ratio | Quality | Action |
|-------|---------|--------|
| > 5x | Excellent | Can invest in growth, may have headroom to raise prices |
| 3-5x | Good | Healthy business, maintain current trajectory |
| 1-3x | Marginal | Needs improvement — lower CAC, increase LTV, or both |
| < 1x | Critical | Losing money on every customer — must fix unit economics before scaling |

### CAC Payback vs LTV/CAC

These are complementary metrics:

| If CAC Payback is… | And LTV/CAC is… | Then… |
|--------------------|------------------|--------|
| Fast (< 6 mo) | High (> 5x) | Excellent unit economics. Invest in growth. |
| Fast (< 6 mo) | Low (< 3x) | Low churn (long lifetime) but low ARPU. Consider pricing changes. |
| Slow (> 18 mo) | High (> 5x) | Very high LTV justifies long payback. Maintain and optimize CAC. |
| Slow (> 18 mo) | Low (< 3x) | Unsustainable. Must reduce CAC, increase pricing, or fix retention. |

### Common Pitfalls

- **Counting all S&M spend.** Not all marketing spend is acquisition. Brand marketing has a longer-term effect. Consider splitting into acquisition and brand separately.
- **Ignoring time value of money.** A $100 customer who pays over 24 months is worth less than a $100 customer who pays upfront. Discount future cash flows for rigor.
- **Averaging across segments.** Enterprise CAC can be 10x SMB CAC. Enterprise LTV can be 50x SMB LTV. Always segment unit economics by customer type.
- **Survivorship bias in LTV.** If you only calculate LTV for current customers, you miss the customers who already churned. Use cohort analysis instead.
- **Not updating.** Unit economics change over time as customer mix, pricing, and acquisition channels evolve. Recalculate quarterly.

## Segment-Level Analysis

Always break down unit economics by segment:

| Segment | CAC | ARPU | Gross Margin | Churn (mo) | LTV | LTV/CAC |
|---------|-----|------|-------------|------------|-----|---------|
| Enterprise | $15K | $3K/mo | 80% | 1.5% | $160K | 10.7x |
| Mid-Market | $5K | $800/mo | 78% | 3% | $20.8K | 4.2x |
| SMB | $500 | $100/mo | 72% | 6% | $1.2K | 2.4x |

This reveals that SMB may appear unprofitable while enterprise is highly efficient. The strategy implications are clear: shift investment toward enterprise.

### Unit Economics Health Dashboard

| Metric | Red Flag | Yellow | Green |
|--------|----------|--------|-------|
| LTV/CAC | < 3x | 3-5x | > 5x |
| Payback | > 18 months | 12-18 months | < 12 months |
| Gross Margin | < 50% | 50-70% | > 70% |
| Monthly Churn | > 5% | 2-5% | < 2% |
| Contribution Margin | < 20% | 20-40% | > 40% |
