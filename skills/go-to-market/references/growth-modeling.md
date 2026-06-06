# Brand Architecture

## Brand Systems Frameworks

### The Brand Hierarchy

| Level | Description | Example (Apple) |
|-------|-------------|-----------------|
| **Corporate brand** | The parent company | Apple Inc. |
| **Product brand** | Individual product lines | iPhone, Mac, iPad |
| **Sub-brand** | Variants within product lines | iPhone Pro, MacBook Air |
| **Endorsed brand** | Standalone brands backed by corporate | Beats by Dr. Dre (Apple) |
| **Descriptor** | Clarifies what the brand does | Google "Cloud," Amazon "Web Services" |

### Brand Relationship Spectrum

A continuum from fully integrated to fully independent:

```
Branded House ─ Sub-brands ─ Endorsed Brands ─ House of Brands
   (Google)        (Apple)       (Marriott)       (P&G)
```

**Decision framework:** The more distinct the customer, channel, and price point, the further right you go. The more integration, cross-sell, and efficiency you need, the further left.

## Brand Voice & Tone

### Voice Dimensions

| Dimension | Spectrum | Example |
|-----------|----------|---------|
| Formal ↔ Casual | Language complexity | Legal docs ↔ Slack messages |
| Serious ↔ Playful | Emotional tone | Medical device ↔ Gaming |
| Respectful ↔ Irreverent | Power distance | Bank ↔ Startup |
| Enthusiastic ↔ Matter-of-fact | Energy level | Social media ↔ Documentation |
| Concrete ↔ Abstract | Specificity | "Save 2 hours/week" ↔ "Empower your team" |

### Tone Shifts by Context

| Context | Tone shift | Example |
|---------|-----------|---------|
| **Error message** | Empathetic, solution-oriented | "Something went wrong — we've been notified. Retry?" |
| **Marketing** | Benefit-driven, active | "Ship faster with automated deployments." |
| **Legal/Compliance** | Precise, careful | "This statement does not constitute a guarantee of performance." |
| **Support** | Personal, ownership | "I'll personally ensure this gets resolved for you." |
| **Internal** | Direct, transparent | "Here's what we know and what we're doing about it." |

## Growth Modeling

### CAC / LTV Deep Dive

#### Calculating CAC

```
CAC = (Sales expenses + Marketing expenses + Sales tools + S&M overhead)
      └─────────────────────────────────────────────────────────────────┘
                                    ÷
      New customers acquired in period
```

**Blended vs Paid vs Organic:**
- **Blended CAC** — Total S&M spend ÷ all new customers (hides channel mix)
- **Paid CAC** — Paid channel spend ÷ paid-acquired customers (for efficiency analysis)
- **Organic CAC** — Organic channel spend ÷ organically acquired customers (usually near $0)

#### LTV Calculation Methods

**Simple LTV (for subscription):**
```
LTV = ARPU × Gross Margin × (1 / Monthly Churn)
```

**Cohort LTV (more accurate):**
Track actual revenue from each cohort over 6-12 months. Plot the curve and extrapolate:

```
LTV_t = Σ(revenue per user in month t) × survival rate to month t
```

**Net Revenue Retention (NRR) LTV:**
```
LTV with expansion = ARPU × Gross Margin / (1 - (Net Retention / 100))
```
Net retention >100% means LTV is infinite (in theory) — customers expand faster than churn.

### Cohort Analysis — Practical Guide

#### Setting Up Cohorts

| Cohort type | When to use | Example |
|-------------|-------------|---------|
| **Time-based** | You want to track improvements over time | Users who signed up in January vs February |
| **Behavior-based** | You want to compare path-dependent outcomes | Trial-started vs trial-converted |
| **Segment-based** | You want to compare persona outcomes | Enterprise vs SMB users |
| **Channel-based** | You want to compare acquisition quality | Organic vs paid vs referral |

#### The Cohort Retention Table

```
Cohort | Month 1 | Month 2 | Month 3 | Month 4 | Month 5 | Month 6
Jan    |  100%   |   42%   |   31%   |   28%   |   26%   |   25%
Feb    |  100%   |   48%   |   35%   |   30%   |   27%   |
Mar    |  100%   |   51%   |   38%   |   32%   |         |
Apr    |  100%   |   48%   |   34%   |         |         |
May    |  100%   |   45%   |         |         |         |
Jun    |  100%   |         |         |         |         |
```

**Reading the table:** The vertical axis shows cohort quality (improving or declining over time). The horizontal axis shows stickiness (how quickly users fall off, and where they plateau).

### Market Entry Strategy

#### Beachhead Selection Matrix

| Criterion | Weight | Segment A | Segment B | Segment C |
|-----------|--------|-----------|-----------|-----------|
| Urgent need (1-5) | 25% | 5 | 3 | 4 |
| Accessible (1-5) | 20% | 3 | 5 | 2 |
| Low competition (1-5) | 20% | 2 | 4 | 5 |
| Budget available (1-5) | 15% | 5 | 3 | 3 |
| Reference value (1-5) | 10% | 4 | 3 | 2 |
| Scale potential (1-5) | 10% | 5 | 3 | 1 |
| **Weighted score** | 100% | **4.10** | **3.60** | **3.15** |

#### Land-and-Expand Playbook

| Phase | Duration | Tactics | Success signal |
|-------|----------|---------|----------------|
| **Land** | 0-3 months | Solve a narrowly-scoped pain; white-glove onboarding; overinvest in success | First renewal, first public reference |
| **Prove** | 3-6 months | Track usage metrics; build case study; gather sponsor quotes | CSAT >90%, NPS >50 |
| **Expand** | 6-12 months | Introduce adjacent use cases; invite more teams; API access | Seat count 3x, feature adoption >3 modules |
| **Entrench** | 12-24 months | Custom integrations; exec relationships; steering committee | Multi-year renewal, product feedback loops |
