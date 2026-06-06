# Operational Metrics

Metrics are how you know whether the operation is performing as designed. The right metrics create alignment. The wrong metrics drive the wrong behavior.

## KPI Design Framework

### Good KPIs vs Bad KPIs

| Good KPI | Bad KPI |
|----------|---------|
| Specific and measurable | Vague ("improve quality") |
| Actionable — can be influenced | Purely informative ("stock price") |
| Owner assigned | No one responsible |
| Tied to a target or threshold | No context for good/bad |
| Leading or lagging with clear relationship | Random measures without connection |
| Few in number (5-7 per department) | Too many to focus on |

### The KPI Hierarchy

**Level 1: Company North Star (1-2 metrics)**
The single metric that best captures whether the company is succeeding. Everything else supports this.

**Level 2: Departmental KPIs (3-5 per department)**
What each department must achieve to support the North Star.

**Level 3: Team/Individual Metrics (3-5 per team)**
What teams and individuals can directly influence.

**Level 4: Process Metrics (as needed)**
Real-time operational measures that feed into Level 3.

### KPI Template

```
Name: [Metric name]
Formula: [How it's calculated]
Frequency: [Daily, weekly, monthly]
Owner: [Who is accountable]
Target: [Good, acceptable, critical thresholds]
Data source: [Where the data comes from]
Lag/Lead: [Leading or lagging indicator]
```

---

## Leading vs Lagging Indicators

| Type | Definition | Examples | When to Use |
|------|-----------|----------|-------------|
| **Lagging** | Measures outcomes after they happen | Revenue, profit, churn, NPS | Strategic review, board reporting |
| **Leading** | Predicts future outcomes | Pipeline creation, demo requests, activation rate | Operational management, early warning |

### Leading Indicators by Function

| Function | Lagging Indicator | Leading Indicator |
|----------|------------------|-------------------|
| **Sales** | Revenue closed | Pipeline created, demo-to-close ratio, win rate |
| **Marketing** | Leads generated | Website traffic, content engagement, conversion rate |
| **Product** | Feature adoption | Time to value, activation rate, session frequency |
| **Engineering** | System uptime | Deployment quality, alert volume, WIP limits |
| **Support** | Customer satisfaction | First response time, resolution time, ticket volume trend |
| **HR** | Attrition rate | Engagement survey score, promotion readiness, time-to-hire |

### The Lead-Lag Chain

Build a causal model connecting leading indicators to lagging outcomes:

```
More demos (lead) → Higher pipeline (lead) → More closed deals (lag) → Revenue growth (lag)
Faster time to value (lead) → Higher activation (lead) → Lower churn (lag) → Higher LTV (lag)
Faster deployment frequency (lead) → Shorter lead time (lead) → Lower change failure rate (lag) → Higher uptime (lag)
```

---

## Balanced Scorecard

A strategic planning and management system that goes beyond financial metrics to include customer, process, and learning perspectives.

### The Four Perspectives

| Perspective | Question | Typical Metrics |
|-------------|----------|-----------------|
| **Financial** | How do we look to shareholders? | Revenue growth, profitability, ROIC, cash flow |
| **Customer** | How do customers see us? | NPS, retention, satisfaction, time to value |
| **Internal Process** | What must we excel at? | Quality, cycle time, cost, throughput |
| **Learning & Growth** | Can we continue to improve? | Employee engagement, skill development, innovation pipeline |

### Building a Balanced Scorecard

1. **Define the strategy.** What is the organization's strategic objective for the next 12-24 months?
2. **Identify 3-5 objectives per perspective.** What must happen in each perspective to achieve the strategy?
3. **Define 1-2 measures per objective.** How will you know the objective is being achieved?
4. **Set targets.** What does good look like? What's the stretch target?
5. **Identify initiatives.** What projects or programs drive movement on these measures?

### Scorecard Example (SaaS Company)

| Perspective | Objective | Measure | Target | Initiative |
|-------------|-----------|---------|--------|------------|
| Financial | Grow recurring revenue | ARR growth rate | 40% YoY | Sales team expansion |
| Financial | Improve efficiency | Rule of 40 | ≥ 40% | Cost optimization program |
| Customer | Improve retention | Net Revenue Retention | ≥ 120% | Customer success automation |
| Customer | Shorten time to value | Days to first activation | < 7 days | Onboarding redesign |
| Internal | Improve delivery speed | Lead time for changes | < 1 day | CI/CD pipeline investment |
| Internal | Ensure quality | Change failure rate | < 5% | Automated testing increase |
| Learning | Develop leadership | Internal promotion rate | 40%+ | Leadership development program |
| Learning | Improve engagement | eNPS score | > 50 | Engagement action planning |

---

## Designing Operational Dashboards

### Dashboard Layers

| Layer | Audience | Refresh | Content |
|-------|----------|---------|---------|
| **Strategic** | Executives | Monthly | North Star, high-level KPIs, trend lines |
| **Tactical** | Department heads | Weekly | Departmental KPIs, variance vs plan, top issues |
| **Operational** | Team leads, ICs | Daily | Process metrics, queues, real-time status |

### Dashboard Design Principles

1. **One page, one purpose.** Don't try to serve everyone with one dashboard. Create separate views for different audiences.
2. **Show the target.** A metric without a target is just a number. Show the actual vs target and the direction.
3. **Trend over time.** A single number is meaningless without context. Show at least the last 12 periods.
4. **Highlight exceptions.** The dashboard should surface what needs attention, not just report what's normal.
5. **Limit to 7-10 metrics per view.** More than that and the dashboard becomes noise.
6. **Label everything.** Metric name, unit, frequency, owner. If someone can't understand the dashboard without asking, it's not done.

### Common Dashboard Anti-Patterns

- **Vanity metrics.** "Total registered users" sounds impressive but tells you nothing about health. Use active users, cohort retention, and conversion rates instead.
- **Data puking.** 50 charts on one page. More data is not more insight. Edit ruthlessly.
- **No drill-down.** The dashboard shows revenue is down. Can you click to see by product line? By region? By segment? Layer in drill-down capability.
- **Stale data.** A dashboard that's updated monthly for operational use is misleading. Match refresh frequency to decision frequency.
- **Automated but unowned.** Every metric needs a human owner. If a number goes red, someone should know who to call.
