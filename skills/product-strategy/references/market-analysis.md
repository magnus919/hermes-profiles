# Market Analysis

## TAM / SAM / SOM — Deep Dive

### TAM (Total Addressable Market)

The total revenue opportunity if your product achieved 100% market share in a defined market.

**Top-down method:**
```
TAM = Number of potential customers × Average revenue per customer
```

Sources: Industry analyst reports (Gartner, Forrester, IDC), government statistics (NAICS codes), trade associations, public company filings (10-Ks).

**Bottom-up method:**
```
TAM = Price × number of units the entire market buys
```

More credible than top-down because it's grounded in transactional reality.

**Pitfall:** TAM inflation. If you define your market as "every company that uses software," the TAM is meaningless. Narrow to the specific use case your product addresses.

### SAM (Serviceable Addressable Market)

The portion of TAM your product and distribution channels can realistically reach.

**Filters:**
- Geographic — "We only sell in the US and EU"
- Channel — "We sell via Shopify App Store, not enterprise sales"
- Product fit — "Our product requires a modern tech stack"
- Segment — "SMBs only (under 500 employees)"

```
SAM = TAM × (% of market reachable via our channels)
```

### SOM (Serviceable Obtainable Market)

The portion of SAM you can realistically capture given your team, capital, and competitive position — typically over a 12-36 month horizon.

**Bottom-up (most credible):**
```
SOM = Sales capacity × Average deal size × (1 - churn rate) × Time
```

- Sales capacity: Number of reps × deals per rep per month
- Marketing capacity: CAC × budget → number of new customers
- Time horizon: Usually 12-24 months for startup fundraising, 36 months for strategic planning

## Product-Market Fit Assessment

### The PMF Pyramid

```
        ┌─────────────┐
        │  Retention  │  ← Core indicator of PMF
        ├─────────────┤
        │  Activation │  ← Do users get value in the first session?
        ├─────────────┤
        │ Acquisition │  ← Can you reach users efficiently?
        ├─────────────┤
        │  Product    │  ← Does the product solve a real need?
        └─────────────┘
```

PMF is layered. You can't have retention without activation, or activation without acquisition, or acquisition without a product-market need.

### PMF Signals

| Signal | What to look for | Red flag |
|--------|------------------|----------|
| **Organic growth** | W-o-M referrals, inbound requests | Zero organic — all paid |
| **Retention** | Flattening retention curve at 30-60-90 days | Continuous downward slope |
| **Usage depth** | Power users who use >5x per week | Everyone uses sporadically |
| **Paying willingness** | High conversion from free to paid | Users love it but won't pay |
| **Churn reason** | "Couldn't get value" (bad PMF) vs "went out of business" (sales problem) | "Didn't see the need anymore" |
| **NPS at scale** | >40 with high response rate | Low response rate or <10 NPS |

### When PMF Is Strong vs Weak

| Strong PMF | Weak PMF |
|------------|----------|
| Users who hit the "aha moment" stay for months | Users try, plateau, and leave |
| 40%+ would be "very disappointed" if you disappeared | <20% would be disappointed |
| Net revenue retention >100% (existing customers spend more over time) | Net revenue retention <80% |
| Hard to scale because demand overwhelms capacity | Hard to scale because nobody cares |
| Sales-led growth works because users bring the product to their org | Sales-led growth fails because there's no bottom-up pull |

## Market Entry Strategy

### Beachhead Selection

Choose your first market segment using these criteria:

| Criterion | Weight | Question |
|-----------|--------|----------|
| **Need** | High | Does this segment urgently need what you build? |
| **Access** | High | Can you reach them cost-effectively? |
| **Competition** | Medium | Is the segment underserved by incumbents? |
| **Budget** | High | Do they have money to spend? |
| **Reference value** | Medium | Will winning here help you win adjacent segments? |
| **Scale** | Low | Is the segment large enough to matter? |

**The beachhead test:** Pick a segment where you can achieve market leadership with a focused offering. If you can't own this segment, pick a narrower one.

### Land-and-Expand

| Phase | Goal | Strategy |
|-------|------|----------|
| **Land** | Get one foot in the door | Solve a specific, painful problem for one team/department |
| **Prove** | Demonstrate measurable ROI | Track adoption, usage, and outcomes rigorously |
| **Expand** | Grow within the account | Add users, teams, use cases, integrations |
| **Entrench** | Become infrastructure | Embed in workflows, data, and processes |

### Platform Entry Strategy

When entering as a platform (not a point solution):

1. **Start with a killer app** — The platform needs one iconic use case that drives adoption
2. **Then open the API** — Once users are on the platform, let them extend it
3. **Then build an ecosystem** — Third-party developers extend reach
4. **Then move up the stack** — Add higher-value capabilities on top of the platform

## Product Lifecycle Management

### The PLC Stages

| Stage | Revenue | Profit | Cash flow | Team focus |
|-------|---------|--------|-----------|------------|
| **Introduction** | Low, growing slowly | Negative | Heavy burn | Product-market fit |
| **Growth** | Rapid growth | Breakeven → positive | Moderate burn → cash-flow-positive | Scale |
| **Maturity** | Slowing growth | Peak | Strong generator | Efficiency, segmentation |
| **Decline** | Declining | Declining | Decreasing | Harvest or pivot |

### Lifecycle Decisions

| Decision point | Introduction | Growth | Maturity | Decline |
|----------------|-------------|--------|----------|---------|
| **Investment** | Heavy (finding PMF) | Heavy (scaling) | Selective (segments) | Minimal (harvesting) |
| **Pricing** | Skim or penetrate | Maintain or optimize | Defend or bundle | Cut |
| **Distribution** | Direct, selective | Broaden channels | Optimize channels | Reduce |
| **Competition** | Few early entrants | More entrants | Many competitors | Consolidation |
| **Product** | Core features | Expand horizontally | Segment-specific variants | Reduce SKUs |

### The S-Curve

Products follow S-curves: slow adoption → rapid growth → plateau. The strategic challenge is to invest in the **next S-curve** while the current one still generates cash. This is the Innovator's Dilemma:

- By the time the current S-curve plateaus, the next one is already growing
- Incumbents underinvest in the next S-curve because the current one is profitable
- New entrants ride the next S-curve up and displace incumbents

**Strategic response:** Run parallel innovation tracks — one optimized for the current curve (extract value), one for the next curve (explore).
