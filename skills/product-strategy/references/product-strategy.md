# Product Strategy & Vision

## North Star Framework

The North Star is the single, leading metric that captures the value your product delivers to customers. It aligns the entire organization around outcome over output.

### Criteria for a Good North Star

| Criterion | Description | Example (Spotify) |
|-----------|-------------|-------------------|
| **Leading indicator** | Predicts long-term business outcomes | Time spent listening → predicts retention |
| **Customer-centric** | Reflects value delivered, not internal activity | Not "features shipped" |
| **Actionable** | Teams can directly influence it | Not "brand awareness" |
| **Measurable** | Can be instrumented and tracked | DAU/MAU, sessions, engagement depth |

### North Star Anti-Patterns

- **Revenue masquerading as a North Star** — Revenue is a lagging indicator. The North Star should be a leading indicator that *drives* revenue.
- **Composite metrics** — A score that combines 5 sub-metrics into one number isn't actionable. No team knows how to move it.
- **Vanity metrics** — Total registered users, not active users. Downloads, not engagement.
- **Annual planning cycle** — The North Star doesn't change quarterly. If you're reevaluating it every planning cycle, you don't have a North Star.

### Formulating a North Star

```text
[Product/Feature] helps [customer segment] achieve [core outcome] by [core capability].
We measure success by [North Star metric].
```

Example (Airbnb):
> Airbnb helps travelers belong anywhere by connecting them with local hosts.
> We measure success by **nights booked**.

## Product Principles

Product principles are decision-making heuristics that encode your product philosophy. They don't tell teams *what* to build — they tell them *how to decide* what to build.

### Anatomy of a Good Principle

| Component | Description | Example |
|-----------|-------------|---------|
| **Name** | Memorable label | "Default to Open" |
| **One-liner** | The rule itself | "Share data by default; only restrict when there's a clear privacy or security reason." |
| **Tradeoff** | What you're willing to sacrifice | "This may mean competitors see our usage patterns. That's acceptable because it builds trust faster." |
| **Boundaries** | When the principle doesn't apply | "Not applicable to PII or billing data." |

### Example Product Principles

- **Solve for the 80%** — Build the path most users take; power users get their edge cases through APIs and extensibility. *Tradeoff: power users may feel underserved.*
- **Progress, not perfection** — Ship the 80% solution this quarter rather than polishing to 95% for two quarters. *Tradeoff: early versions will have rough edges.*
- **Platform over point solution** — Build capabilities that multiple features can leverage, not single-use features. *Tradeoff: slower initial delivery.*
- **Default to simplicity** — When a decision adds complexity without a measurable improvement in the primary metric, reject it. *Tradeoff: some elegant-but-complex solutions won't ship.*

## Roadmap Prioritization

### RICE Scoring

The RICE framework scores feature proposals across four dimensions:

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

- **Reach**: How many users per unit time this affects
- **Impact**: How much it matters to those users (0.25× to 3× multiplier)
- **Confidence**: How sure you are about estimates (20%–100%)
- **Effort**: Total team-weeks required

See `rrice-framework.md` in the product-methodology skill for the full treatment.

### Kano Model

Categorizes features by their relationship to customer satisfaction:

| Category | Description | Example | Saturation risk |
|----------|-------------|---------|-----------------|
| **Threshold** (Must-be) | Expected; absence causes dissatisfaction | Login, payment processing | None — required to compete |
| **Performance** (One-dimensional) | More is better; directly correlates with satisfaction | Battery life, page load speed | Yes — diminishing returns |
| **Delight** (Attractive) | Unexpected; absence doesn't hurt, presence delights | Confetti animation on first purchase | Yes — becomes threshold over time |
| **Indifferent** | No impact on satisfaction | Unused settings options | N/A |
| **Reverse** | More is worse | Excessive notifications | N/A |

**Strategic implication:** Don't invest in delighters at the expense of threshold features. Threshold features are table stakes — you can't win on them, but you can lose without them. Invest in performance features for competitive differentiation, and sprinkle delighters as surprise-and-delight moments.

### Opportunity Solution Trees (OST)

A framework for connecting customer needs to build decisions without jumping to solutions:

```
Opportunity (customer need)
├── Solution option A
│   └── Assumption to test
├── Solution option B
│   └── Assumption to test
└── Solution option C
    └── Assumption to test
```

**Key rules:**
1. Start with an **opportunity** (something the customer needs to achieve), not a solution.
2. Branch into **possible solutions** — multiple options for each opportunity.
3. Each solution has **testable assumptions** — what must be true for it to work.
4. Test the riskiest assumption first. If it fails, move to the next solution.

**Pitfall:** Teams jump to a single solution because it's obvious. OST forces you to consider alternatives before committing.

## Product-Market Fit (PMF)

### Sean Ellis Test

Ask active users: "How would you feel if you could no longer use [product]?"

| Response | Interpretation |
|----------|---------------|
| **Very disappointed** | Core engaged users — 40%+ indicates PMF |
| **Somewhat disappointed** | Users who find value but aren't hooked |
| **Not disappointed** | Low value — no PMF |
| **N/A — no longer use** | Churned |

**Threshold:** If ≥40% answer "Very disappointed," you have product-market fit.

### Retention Curves

Plot % of users retained over time from their signup date:

- **Flattening curve** → PMF hit. Users who get the value stay.
- **Downward slope** → No PMF. Users try the product and leave.
- **Flattening then dropping** → Weak PMF for a specific segment. Find the cohort that sticks and focus on it.

**Segmentation tip:** Don't look at aggregate retention. Segment by acquisition channel, user persona, feature adoption, and behavior. The right cohort tells you where PMF exists; the wrong cohort hides it.

## Market Sizing: TAM / SAM / SOM

| Term | Definition | Question it answers |
|------|------------|---------------------|
| **TAM** (Total Addressable Market) | Total revenue opportunity if 100% market share | "How big is the pie?" |
| **SAM** (Serviceable Addressable Market) | Segment of TAM your product/service can reach | "How much of the pie can we actually serve?" |
| **SOM** (Serviceable Obtainable Market) | Share of SAM you can realistically capture | "How much will we actually eat?" |

### Top-Down Approach

Start with industry analyst data and apply filters:

```
TAM = Global market revenue for category X
SAM = TAM × % accessible via our distribution channels
SOM = SAM × % we can capture given our team/capital/competitive position
```

**Pitfall:** Top-down tends to overestimate. Analysts define markets broadly; your actual reach is narrower.

### Bottom-Up Approach

Start with your unit economics and scale up:

```
SOM = (Sales capacity × conversion rate × average deal size) × time horizon
SAM = SOM × (theoretical max sales capacity / current capacity)
TAM = Bottom-up SAM × (your price / average category price)
```

**Bottom-up is more credible** because it's grounded in operational reality.

## Platform Strategy

### API-First Design

Build the API before the UI. This forces contract clarity, enables multiple clients (web, mobile, partner API), and creates a foundation for ecosystem growth.

**Key decisions:**
- REST vs GraphQL vs gRPC — each has different tradeoffs for discoverability, performance, and client complexity
- Versioning strategy — URL-based (`/v1/`), header-based, or contract-based (GraphQL)
- Authentication — API keys (simple), OAuth2 (scoped), JWTs (stateless)

### Marketplace Strategy

Two-sided network effects create defensible moats:

| Phase | Supply side | Demand side | Mechanics |
|-------|-------------|-------------|-----------|
| **Cold start** | Recruit supply manually | Seed demand through marketing | Both sides need value before the other exists — hardest phase |
| **Growth** | Supply grows with demand | Demand grows with supply | Each new supply unit attracts demand, and vice versa |
| **Moat** | High switching costs | Deep inventory | Competitors can't replicate the liquidity |

### Ecosystem Strategy

- **Platform extensibility** — APIs, plugins, webhooks, embeddable widgets
- **Developer experience** — Documentation, SDKs, sandbox environments, SLAs
- **Governance** — What third parties can/cannot build, revenue share, certification
- **Control points** — Where you retain control vs open up

## Product Lifecycle Management

| Stage | Characteristics | Strategy | Metrics |
|-------|----------------|----------|---------|
| **Introduction** | Low revenue, high investment | Build awareness, find PMF | Activation rate, early retention |
| **Growth** | Rapid revenue growth | Scale acquisition, expand features | Net revenue retention, market share |
| **Maturity** | Slowing growth, stable revenue | Extract profits, segment positioning | Profit margin, customer lifetime value |
| **Decline** | Revenue declining | Harvest or pivot | Cash flow, cost of maintenance |

**Key insight:** The worst product strategy mistake is treating a mature product like a growth product (over-investing) or a growth product like a mature product (under-investing for short-term profit).
