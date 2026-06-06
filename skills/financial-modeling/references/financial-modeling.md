# Financial Modeling

Financial models translate business assumptions into projected financial statements. Their primary value is forcing explicit, internally consistent assumptions — not predicting the future.

## Model Structure

A complete financial model has three linked statements and supporting schedules.

### Core Statements

| Statement | What It Shows | Key Line Items |
|-----------|---------------|----------------|
| **Income Statement (P&L)** | Profitability over time | Revenue, COGS, Gross Margin, OpEx, EBITDA, Net Income |
| **Balance Sheet** | Assets, liabilities, equity at a point in time | Cash, AR, AP, Debt, Equity |
| **Cash Flow Statement** | Sources and uses of cash | Operating CF, Investing CF, Financing CF, Net Change in Cash |

### Supporting Schedules

| Schedule | Feeds Into | Contents |
|----------|-----------|----------|
| Revenue build | P&L Revenue | Assumptions, pipeline, conversion, pricing model |
| Headcount plan | P&L OpEx | Roles, start dates, salary, benefits, taxes |
| CapEx schedule | P&L Depreciation, BS Fixed Assets | Equipment, software, facilities, useful life |
| Debt schedule | BS Debt, P&L Interest | Principal, interest rate, term, covenants |
| Equity schedule | BS Equity | Rounds, option pool, dilution |

---

## Revenue Projections

### Building a Revenue Model

**Top-down approach** (starting from market):
```
Revenue = TAM × % Serviceable × % Obtainable × Price
```

**Bottom-up approach** (starting from operations):
```
Revenue = (# Customers × ARPU) + (# Expansion deals × $)
```

**Best practice: Use bottom-up for the base case, top-down as a sanity check.**

### Revenue Modeling by Business Model

**SaaS (Subscription):**

| Input | Description |
|-------|-------------|
| Starting customers | Current customer base |
| New customers per month | Sales model + ramp assumption |
| Churn rate | % of customers canceling per period |
| ARPU (avg revenue per user) | Average monthly revenue per customer |
| Expansion/contraction | Upsells, downgrades within existing base |
| Seasonality | Quarterly patterns, renewal concentration |

**Formula:**
```
Month N Revenue = (Prev Customers × (1 - Churn) × ARPU) + (New Customers × ARPU) + Expansion Revenue
```

**Usage-based:**

| Input | Description |
|-------|-------------|
| Customer count | Active users/accounts |
| Per-customer usage | Units consumed (API calls, storage, seats) |
| Price per unit | $/unit |
| Seasonality | Usage patterns (holidays, business cycles) |

**Professional Services:**
```
Revenue = Billable Headcount × Utilization Rate × Billable Rate × Days
```

### Revenue Modeling Pitfalls

- **Linear growth assumption.** Few businesses grow linearly. Consider: sales ramp, market saturation, competitive response, product launch timing.
- **Ignoring customer concentration.** If 40% of projected revenue comes from 2 customers, model what happens if they don't close or they churn.
- **Optimistic expansion rate.** SaaS expansion is not automatic. Model a range: flat (no expansion), moderate (industry average), aggressive (best case).
- **Silent churn.** "We don't churn much" usually means "we haven't measured it." Build churn into the model even if it's a guess.

---

## Cost Structures

### Fixed vs Variable Costs

| Type | Definition | Examples | Modeling Approach |
|------|-----------|----------|-------------------|
| **Fixed** | Doesn't change with revenue | Rent, base salaries, subscriptions | Step function (changes at headcount/space thresholds) |
| **Variable** | Scales with revenue | Cloud hosting, payment processing, commissions | % of revenue or per-unit cost |
| **Semi-variable** | Fixed base + variable above threshold | Support team, sales headcount | Model headcount tiers with utilization triggers |

### Modeling OpEx Categories

**R&D (Engineering + Product):**
- Headcount-driven: salary, benefits, recruiting, tools
- Model by role: senior, mid, junior; by function: platform, feature, infra
- Capitalize vs expense: software development capitalization rules

**S&M (Sales & Marketing):**
- Headcount: SDRs, AEs, CSMs, marketing
- Variable: commissions (% of closed revenue), advertising (CAC targets)
- Program: events, content, PR

**G&A (General & Administrative):**
- Headcount: exec, finance, legal, HR, admin
- Fixed: insurance, professional fees, software, facilities
- Public company costs: audit, compliance, D&O insurance

### Cost Structure Heuristics

| Metric | Benchmark |
|--------|-----------|
| R&D as % of revenue | 20-40% (growth), 10-20% (mature) |
| S&M as % of revenue | 30-50% (growth), 15-30% (mature) |
| G&A as % of revenue | 8-15% |
| Gross margin (SaaS) | 70-85% |
| Gross margin (services) | 20-40% |

---

## Scenario Planning

### The Three-Scenario Model

| Scenario | Definition | Typical Assumptions |
|----------|-----------|-------------------|
| **Base Case** | Most likely outcome | Management's best estimate |
| **Upside** | Favorable conditions | Growth accelerates, churn drops, margins improve |
| **Downside** | Adverse conditions | Growth slows, churn rises, cost overruns |

### Scenario Framework

| Variable | Downside | Base | Upside |
|----------|----------|------|--------|
| New customers/month | -20% from plan | Per plan | +20% from plan |
| Churn rate | +3% | Per plan | -1% |
| ARPU growth | 0% | 5%/yr | 10%/yr |
| S&M cost | +15% | Per plan | -5% |
| Gross margin | -5% | Per plan | +3% |
| Time to close | +50% | Per plan | -25% |

### Sensitivity Analysis

Identify which variables have the largest impact on outcomes. Run a sensitivity table:

```
                New Customers (variance from plan)
           -30%    -15%    0%    +15%    +30%
Churn  +3%   $X     $Y     $Z     $A     $B
rate   +1%   $C     $D     $E     $F     $G
(Δ)     0%   $H     $I     $J     $K     $L
       -1%   $M     $N     $O     $P     $Q
```

The cells where the outcome changes most are the variables that need the most attention and the most accurate assumptions.

---

## Runway Analysis

For pre-revenue or growth-stage companies, runway is the single most important financial metric.

### The Formula

```
Runway (months) = Cash Balance / Net Monthly Burn

Net Monthly Burn = Monthly Revenue - Monthly Operating Costs
```

### Runway Sensitivity

| Scenario | Monthly Burn | Cash | Runway (months) |
|----------|-------------|------|-----------------|
| Current | $500K | $5M | 10 months |
| +20% spend | $600K | $5M | 8.3 months |
| -20% spend | $400K | $5M | 12.5 months |
| +$1M revenue (annual) | $417K | $5M | 12 months |

### Runway Cushion

| Runway Remaining | Action Required |
|-----------------|-----------------|
| 18+ months | Comfortable. Plan for next fundraise. |
| 12-18 months | Start fundraise process. Begin investor conversations. |
| 6-12 months | Fundraise in active progress. Consider cost reduction. |
| 3-6 months | Emergency: significant cuts or bridge financing. |
| < 3 months | Survival mode: all non-essential spend stopped. |

### Runway Pitfalls

- **Forgetting one-time costs.** Legal fees for fundraise, severance, facility moves. Add 10-20% buffer.
- **Assuming linear burn.** Burn often increases before it decreases (hiring for a new initiative that then gets cut).
- **Ignoring AR/AP timing.** Cash flow is not P&L. A profitable company can run out of cash if customers don't pay on time.
- **Over-optimistic revenue timing.** "Revenue in Q4" usually means "revenue in Q1 next year." Revenue always slips.
