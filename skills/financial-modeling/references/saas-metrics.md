# SaaS Metrics

Standard operating metrics for SaaS businesses. These metrics are the language of board meetings, investor updates, and quarterly business reviews.

## Growth Metrics

### ARR (Annual Recurring Revenue)

The annualized value of recurring subscriptions. The primary revenue metric for SaaS.

```
ARR = Monthly Recurring Revenue × 12
     — OR —
ARR = Sum of all annual subscription values

Note: Excludes one-time fees, professional services, and usage-based revenue
above committed minimums.
```

**Components of ARR:**

| Component | Definition | How It's Tracked |
|-----------|-----------|-----------------|
| **New ARR** | ARR from new customers | Invoiced value of new contracts |
| **Expansion ARR** | Upsells, cross-sells, price increases to existing customers | Delta between old contract and new contract |
| **Contraction ARR** | Downgrades, seat reductions | Negative delta |
| **Churned ARR** | Lost from cancellations | Full ARR value of canceled contracts |
| **Net New ARR** | New + Expansion - Contraction - Churn | ARR growth for the period |

### MRR (Monthly Recurring Revenue)

Same as ARR but measured monthly. Useful for tracking short-term trends.

```
MRR = Number of paying customers × ARPU

Logo MRR vs Dollar MRR:
- Logo MRR: simple count × average price (less accurate)
- Dollar MRR: actual revenue from each account (preferred)
```

### ARR Growth Rate

```
YoY ARR Growth Rate = (Current ARR - Prior Year ARR) / Prior Year ARR
```

| Growth Rate | Classification |
|-------------|---------------|
| > 100% | Hypergrowth |
| 50-100% | Very high growth |
| 30-50% | High growth |
| 15-30% | Moderate growth |
| < 15% | Slow growth / Mature |

---

## Retention Metrics

### Logo Churn (Customer Churn)

The percentage of customers who cancel in a given period.

```
Monthly Logo Churn = Customers Churned (month) / Total Customers (start of month)

Annual Logo Churn = (1 - Monthly Retention^12) × 100
```

| Monthly Logo Churn | Annual Equivalent | Quality |
|--------------------|------------------|---------|
| < 2% | < 21.7% | Good |
| 2-5% | 21.7-46% | Acceptable |
| 5-8% | 46-63% | Concerning |
| > 8% | > 63% | Critical |

### Net Dollar Retention (NDR)

The most important SaaS retention metric. Measures whether existing customers are spending more or less over time.

```
NDR = (Starting ARR + Expansion - Contraction - Churn) / Starting ARR
```

**Benchmarks:**

| NDR | Classification | Implication |
|-----|---------------|-------------|
| > 130% | World-class | Massive expansion revenue. Growth without new customers. |
| 120-130% | Excellent | Strong expansion. Churn more than offset by upsells. |
| 110-120% | Good | Modest expansion. Healthy but room to improve. |
| 100-110% | Acceptable | Flat to slight growth in existing base. |
| 90-100% | Concerning | Existing base is shrinking. Fix retention. |
| < 90% | Critical | Losing customers faster than expanding. |

**Why NDR Matters:**
- At 120% NDR, a $10M ARR company grows to $12M without adding a single new customer.
- At 90% NDR, that same company needs $3M in new ARR just to reach $12M.
- High NDR companies are more capital-efficient and command higher valuation multiples.

### Gross Dollar Retention (Gross Retention)

The percentage of ARR retained excluding expansion.

```
Gross Retention = (Starting ARR - Churned ARR - Contraction ARR) / Starting ARR
```

Typically 80-95%. Lower than NDR because it doesn't benefit from expansion.

---

## Efficiency Metrics

### Rule of 40

The 40% Rule states that a healthy SaaS company's revenue growth rate + profit margin should equal or exceed 40%.

```
Rule of 40 = Revenue Growth Rate (%) + EBITDA Margin (%)
Target: ≥ 40%
```

**Interpretation:**

| Score | Assessment |
|-------|------------|
| > 40% | Strong — balance of growth and profitability |
| 30-40% | Acceptable — monitor, look for improvement trajectory |
| 20-30% | Concerning — either too slow or too unprofitable |
| < 20% | Critical — must improve growth, margin, or both |

**Example:**
- Company A: 50% growth, 10% EBITDA margin → 60 ✓
- Company B: 30% growth, 20% EBITDA margin → 50 ✓
- Company C: 80% growth, -50% EBITDA margin → 30 ✗ (growing unprofitably)
- Company D: 5% growth, 25% EBITDA margin → 30 ✗ (mature but low growth)

**Caveat:** The Rule of 40 is a single-number heuristic. Use it for high-level monitoring, not strategic decisions. A company at 35% with improving trajectory is better than one at 45% with declining trajectory.

### Magic Number

Measures sales efficiency: how much incremental ARR is generated per dollar of S&M spend.

```
Magic Number = Net New ARR (current quarter) × 4 / S&M Spend (previous quarter)
```

**Benchmarks:**

| Magic Number | Efficiency |
|-------------|------------|
| > 1.0x | Outstanding |
| 0.75-1.0x | Excellent |
| 0.5-0.75x | Good |
| 0.25-0.5x | Needs improvement |
| < 0.25x | Poor |

**Why previous quarter S&M:** There's a lag between spending on sales and marketing and the resulting ARR. Using the previous quarter's spend accounts for this.

### CAC Ratio (CAC Payback in Months)

```
CAC Ratio = (Prior Quarter S&M × 4) / Net New ARR

CAC Payback (months) = (Prior Period S&M) / (Net New ARR / 12)
```

**Benchmarks:**

| Metric | Good | Excellent |
|--------|------|-----------|
| Blended CAC Ratio | < 2x | < 1x |
| Paid CAC Payback | < 18 months | < 12 months |

### Burn Multiple

How much capital is burned for each dollar of incremental ARR.

```
Burn Multiple = Net Cash Burn (period) / Net New ARR (period)
```

| Burn Multiple | Capital Efficiency |
|--------------|-------------------|
| < 1x | Capital-efficient (or very profitable) |
| 1-2x | Moderate — within reasonable range |
| 2-3x | High burn — needs justification for growth |
| > 3x | Very high burn — likely unsustainable |

---

## Usage & Engagement Metrics

### Monthly Active Users (MAU)

Percentage of customer accounts that actively use the product.

```
MAU Rate = Unique active users (last 30 days) / Total billable users
```

### Time to Value (TTV)

How long from sign-up to first meaningful use. The single best predictor of retention.

| TTV | Retention Impact |
|-----|-----------------|
| < 1 hour | Very high retention (> 90%) |
| 1-24 hours | Good retention |
| 1-7 days | Average retention |
| 7-30 days | Below average retention |
| > 30 days | High churn risk |

### Health Score Components

A composite customer health score for proactive retention:

| Component | Weight | Measure |
|-----------|--------|---------|
| Product usage | 30% | MAU, feature adoption, session frequency |
| Support interactions | 20% | Ticket volume, severity, sentiment |
| NPS / Satisfaction | 20% | Survey score (promoter/detractor) |
| Account growth | 15% | Seat expansion, add-on purchases |
| Communication | 15% | Executive engagement, email responsiveness |

### SaaS Metrics Anti-Patterns

- **ARR obsession.** ARR is a vanity metric without churn, NDR, and efficiency context. A company with $50M ARR and 80% NDR is dying.
- **Churn averaging.** "Our churn is 3%" masks segments where it's 1% (enterprise) and 10% (SMB). Always segment churn by customer type.
- **Magic Number games.** Shifting S&M spend to R&D to improve the Magic Number is gaming the metric, not improving efficiency.
- **Comparing to irrelevant benchmarks.** A $5M ARR company shouldn't benchmark against Salesforce. Use stage-appropriate comparisons.
- **Monthly metrics for annual contracts.** If customers sign annual contracts, measure annual metrics. Monthly churn on annual contracts is misleading.
