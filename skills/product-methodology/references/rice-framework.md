# RICE Scoring Framework

A method for prioritizing feature proposals by scoring them across four dimensions: Reach, Impact, Confidence, and Effort.

## The Formula

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

Score is unitless — used only for relative comparison. A score of 50 is not "good"; it's better than 30 and worse than 100.

## Dimensions

### Reach — How many people does this affect?

Measured in users or customers per unit time. Be specific about the time window.

| Signal | Typical value | Example |
|--------|--------------|---------|
| Affects all users | 10,000+/quarter | Login flow improvement |
| Affects a segment | 1,000–10,000/quarter | New export format for power users |
| Affects very few | 100–1,000/quarter | Admin UI improvement |
| Niche edge case | < 100/quarter | Specific error message improvement |

**Pitfall:** Don't inflate Reach by counting everyone as "affected." A feature must measurably change their experience to count them.

### Impact — How much does it matter to the people it reaches?

A qualitative score converted to a multiplier. Use a standard scale to keep comparisons consistent.

| Score | Label | Meaning |
|-------|-------|---------|
| 3 | Massive | Transformative for the target users |
| 2 | High | Significant improvement |
| 1 | Medium | Noticeable improvement |
| 0.5 | Low | Marginal improvement |
| 0.25 | Minimal | Barely noticeable |

**Pitfall:** Impact is about the people reached, not total business value. A 0.5 impact × 10,000 reach = 5,000; a 3 impact × 100 reach = 300. The high-reach/low-impact item scores higher. This is by design — it surfaces broad improvements over narrow deep ones.

### Confidence — How sure are you about your Reach and Impact estimates?

Expressed as a percentage. Low confidence should penalize the score heavily.

| Score | Label | Meaning |
|-------|-------|---------|
| 100% | High | Primary data (ran an experiment, have production metrics) |
| 80% | Medium | Strong secondary evidence (user interviews, survey data, industry benchmarks) |
| 50% | Low | Informed opinion (domain expertise, analogous feature history) |
| 20% | Guess | Gut feeling with no supporting data |

**Pitfall:** Don't use 100% unless you have actual data. Most RICE scores should live in 50-80% confidence. Items with <50% confidence should be treated as bets, not commitments, regardless of their score.

### Effort — How much time from the full team?

Estimated in person-weeks (or person-months for larger items). Include design, engineering, QA, and release overhead.

| Effort | Typical scope |
|--------|--------------|
| 1–2 weeks | Small change, well-understood |
| 3–5 weeks | Moderate feature, some unknowns |
| 6–10 weeks | Significant feature, multiple systems |
| 10+ weeks | Major initiative, cross-team effort |

**Pitfall:** Effort should include all overhead — design reviews, QA, documentation, deployment. The actual build time is only 50-70% of total effort.

## When to Use RICE vs Other Frameworks

| Use RICE When | Don't Use RICE When |
|--------------|---------------------|
| You have enough data to estimate four dimensions credibly | Estimates are pure guesses across the board |
| You're comparing unrelated feature proposals | All options are variations of the same thing |
| You need to defend priorities to stakeholders | The decision is a quick call between two obvious choices |
| You're planning a quarter+ roadmap | You're planning a single sprint |

## Common RICE Pitfalls

### Score inflation across the board
All scores drift up over time as teams get optimistic. **Reset periodically.** If everything scores above 100, your scale has shifted. Re-anchor against a known baseline ("last quarter's top feature was a 47 — does this really beat it by 3x?").

### Effort as a schedule, not a cost
Effort should be team-weeks, not calendar-weeks. A feature that takes 2 weeks of engineering work but 4 weeks of calendar time because of dependencies should be scored at 2 weeks. The dependency is a separate concern.

### Cherry-picking the easy dimension
If Reach is obviously high, don't pad Impact and Confidence to match. Each dimension should be estimated independently. If you find yourself adjusting Confidence to fit a desired score, you're anchoring.

### The denominator trap
Effort is the denominator. For large efforts (10+ weeks), small changes in Effort have huge effects. Round conservatively. If a feature is "roughly 8-12 weeks," use 12.

## Example

| Item | Reach | Impact | Confidence | Effort | Score |
|------|-------|--------|------------|--------|-------|
| Add CSV export | 2,000/q | 2 (High) | 80% | 2 wks | (2000×2×0.8)/2 = 1600 |
| Dark mode | 10,000/q | 1 (Med) | 50% | 6 wks | (10000×1×0.5)/6 = 833 |
| Rebuild search | 10,000/q | 3 (Massive) | 20% | 12 wks | (10000×3×0.2)/12 = 500 |

CSV export wins despite lower Reach because high Confidence + low Effort creates a better ratio. The search rebuild has the most potential but needs validation before it's worth the bet.
