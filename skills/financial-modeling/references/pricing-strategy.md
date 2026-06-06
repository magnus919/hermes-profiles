# Pricing Strategy

Pricing is one of the most leveraged decisions a company makes. A 1% price increase, if done without losing customers, drops 8-12% to the bottom line — more than any cost-cutting initiative.

## Pricing Models

### Value-Based Pricing

Price is set based on the perceived value to the customer, not the cost to produce.

**Method:**
1. Quantify the value your product delivers to a customer in dollar terms
2. Price as a fraction of that value (typically 10-30%)
3. Segment by willingness to pay when possible

**Example:** A tool that saves a customer $100K/year in labor cost is worth $10-30K/year, regardless of what it costs to build.

| Pro | Con |
|-----|-----|
| Highest potential revenue | Requires deep customer value understanding |
| Aligns with customer perceived value | Harder to communicate and justify |
| Most defensible against competition | Requires ongoing value re-assessment |

### Cost-Plus Pricing

Price is set by adding a markup to the cost of production.

**Method:**
1. Calculate fully loaded cost per unit
2. Add desired margin (e.g., 40% gross margin → 67% markup on cost)
3. Adjust for market realities

**Example:** Cost to serve is $10/month per user. Target 70% gross margin → price at $33/user/month.

| Pro | Con |
|-----|-----|
| Simple to calculate | Ignores customer willingness to pay |
| Guarantees margin floor | Leaves money on the table if value is higher |
| Easy to defend internally | Prices too high if costs are inefficient |

### Competitive Pricing

Price is set relative to competitors.

**Methods:**
- **Premium:** Price above market (justified by superior value)
- **Parity:** Match market price (competition is the default)
- **Discount:** Price below market (sacrifice margin for share)

| Pro | Con |
|-----|-----|
| Market-referenced, easy to explain | Race to the bottom |
| Low cognitive load for customers | Assumes competitors know their pricing best |
| Works in commodity markets | Ignores your unique value |

### Freemium

Free tier + paid upgrade. The free tier serves as acquisition and qualification.

**Design Principles:**
- Free tier is genuinely useful (not crippled)
- Paid features are obviously valuable to power users
- Free → paid conversion rate is 2-5% (typical for SaaS)
- Unit economics must work: free user COGS < LTV of converting paid users

**When Freemium Works:**
- Network effects (more users = more value)
- Low marginal cost of serving free users
- Viral distribution potential
- Clear upgrade triggers (limits on usage, features, or team size)

### Tiered Pricing

Multiple packages at different price points. The most common B2B SaaS pricing model.

**Design Principles:**
- 3 tiers is the sweet spot (some use 4, rarely more)
- Each tier serves a distinct customer segment
- The middle tier is typically the most popular (goldilocks effect)
- Features should ladder: each tier includes all lower-tier features plus new ones
- The price difference between tiers should be significant enough to drive the decision

**Typical Tier Structure:**

| Tier | Target | Price | Positioning |
|------|--------|-------|-------------|
| Basic | Small teams / individuals | $10-30/mo | Entry point, limited features |
| Professional | Growing businesses | $50-200/mo | Most popular, full features |
| Enterprise | Large organizations | Custom pricing | Everything + support, security, compliance |

---

## Packaging Strategy

### What to Package Together

| Bundling Strategy | When It Works | Risks |
|-------------------|--------------|-------|
| **Pure bundle** | Features used together, customers value completeness | Customers pay for what they don't use |
| **Pure unbundle** | Features serve different needs, customers are price-sensitive | Complexity, decision paralysis |
| **Mixed bundling** (bundle available, individual also available) | Broad customer base with different needs | Cannibalization if bundle is too cheap |

### The Decoy Effect

The presence of a less-attractive option makes the target option look better.

**Example:**
- Basic: $10 (1 project)
- Professional: $25 (5 projects) ← target
- Enterprise: $50 (5 projects + support) ← decoy

The decoy makes Professional look like the smart choice, driving volume to the target tier.

### Pricing Page Best Practices

- **Annual discounts.** 15-20% discount for annual billing is standard. It improves cash flow and reduces churn.
- **Usage limits clearly shown.** Customers should understand what they're buying without reading fine print.
- **Feature comparison table.** Show what's included at each tier.
- **Enterprise CTA.** "Contact sales" for enterprise tier signals custom pricing and higher-touch service.
- **Social proof.** "Join 10,000+ teams" or logos of notable customers.

---

## Pricing Changes

### Price Increase Playbook

1. **Add value first.** Ship features, improve support, or increase limits before raising prices.
2. **Communicate the reason.** "We're investing in X" is better than "we need more money."
3. **Grandfather existing customers.** Keep them on the old price for a period (6-12 months) or permanently.
4. **Give notice.** 30-60 days minimum for existing customers.
5. **Test with a segment.** Increase price for new customers first, measure conversion impact.

### Price Elasticity Testing

Test price sensitivity before committing to a change:

| Method | How | Risk |
|--------|-----|------|
| **Survey** | Ask "Would you buy at $X?" | Low accuracy — stated vs revealed preference |
| **Segment test** | Raise price for new customers in one segment only | Medium — captures real behavior |
| **Grandfathering test** | Offer existing customers voluntary upgrade to new price point | Low — low risk, good signal |
| **Conjoint analysis** | Systematic trade-off survey | Medium — good accuracy if well-designed |

### Churn vs Price Trade-off

Before raising prices, estimate the LTV impact:

```
Current LTV = $100/mo × 60% gross margin × 1/5% monthly churn = $1,200
New LTV (price +20%) = $120/mo × 60% GM × 1/8% churn (3% increase) = $900
```

In this example, the price increase destroys LTV because the churn increase outweighs the revenue gain. Model this trade-off before deciding.

---

## Common Pricing Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Underpricing** | High conversion, low churn, but can't fund growth | Raise prices systematically, test elasticity |
| **Overpricing** | Low conversion, high demo-to-close time | Reduce price or add lower tier |
| **Too many tiers** | Analysis paralysis, 80% choose middle anyway | Consolidate to 3 tiers |
| **No annual discount** | Poor cash flow, higher churn | Add 15-20% annual discount |
| **One-size-fits-all** | Enterprise customers paying SMB prices | Add usage limits and feature tiers |
| **Sticky pricing** | Haven't changed in 2+ years | Review and adjust annually |
| **Metric confusion** | Customers don't understand what they pay for | Simplify the pricing metric (per user, per action, flat) |
