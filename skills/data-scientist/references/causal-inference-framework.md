# Causal Inference Framework

## Two Frameworks, Unified

Causal inference rests on two complementary traditions. A PhD-level data scientist is fluent in both.

| Tradition | Core Question | Key Concepts | Key Figures |
|-----------|--------------|--------------|-------------|
| **Structural / Graphical (SCM)** | What would happen under intervention? | DAGs, d-separation, do-calculus, structural equations | Pearl, Glymour, Jewell |
| **Potential Outcomes (Rubin Causal Model)** | What is the difference between observed and counterfactual? | Treatment effects, assignment mechanism, ignorability | Rubin, Hernán, Robins |

**Both frameworks should agree when applied correctly to the same problem.** Use them as complementary lenses.

---

## Part 1: DAGs & Graphical Approach

### DAG Construction Rules

A Directed Acyclic Graph (DAG) encodes causal assumptions. Every arrow represents a direct causal effect.

1. **Include all common causes** of any two variables in the graph (observed or unobserved)
2. **Arrows go from cause to effect** (temporal order)
3. **No cycles** (hence "acyclic")
4. **Mark unobserved variables** (dashed nodes, U variables) to track what's not measured
5. **Be parsimonious** — include only variables relevant to the causal question

### Causal DAG Vocabulary

| Concept | Definition | DAG Representation |
|---------|-----------|-------------------|
| **Confounder** | Variable that causes both treatment and outcome | C → T, C → Y (back door path T ← C → Y) |
| **Collider** | Variable caused by both treatment and outcome | T → C ← Y (conditioning on C opens path) |
| **Mediator** | Variable on causal pathway from T to Y | T → M → Y (don't adjust — blocks indirect effect) |
| **Instrumental Variable** | Variable that causes T but only affects Y through T | Z → T → Y (used when unobserved confounding) |
| **Selection Bias** | Conditioning on a collider or common effect | T → C ← U → Y (conditioning on C creates spurious association) |

### Back Door Criterion

A set of variables W satisfies the back door criterion for (T, Y) if:
1. No variable in W is a descendant of T
2. W blocks every back door path between T and Y (every path with an arrow into T)

If satisfied, the causal effect of T on Y is identifiable by adjusting for W:
```
P(Y | do(T = t)) = Σ_w P(Y | T = t, W = w) P(W = w)
```

### How to Identify Confounders in a DAG

```
Identify all paths between treatment T and outcome Y.
For each path:
│
├─ Directed path T → ... → Y: causal path (leave open)
│
├─ Back door path T ← ... → Y: potential confounding
│  ├─ Can I block it by adjusting for measured variables?
│  │  ├─ Yes → include them as covariates
│  │  └─ No → unmeasured confounding; consider IV, RDD, DID, or sensitivity
│  └─ Is there a collider on the path?
│     └─ If so, DON'T adjust for it (opens the path)
```

### Do-Calculus (Pearl)

Three rules for transforming expressions containing `do(T = t)` into ordinary conditional probabilities:

1. **Insert/delet observations**: P(Y | do(T), Z, W) = P(Y | do(T), W) if (Y ⟂ Z | T, W) in the graph where incoming arrows to T are removed
2. **Action/observation exchange**: P(Y | do(T), do(Z), W) = P(Y | do(T), Z, W) if (Y ⟂ Z | T, W) in the graph where incoming arrows to Z are removed
3. **Delet actions**: P(Y | do(T), do(Z), W) = P(Y | do(T), W) if (Y ⟂ Z | T, W) in the graph where incoming arrows to T and outgoing from Z are removed

---

## Part 2: Potential Outcomes Framework

### Core Notation

| Symbol | Meaning |
|--------|---------|
| Yᵢ(1) | Outcome for unit i if treated |
| Yᵢ(0) | Outcome for unit i if untreated (counterfactual) |
| Tᵢ | Treatment indicator (1 = treated, 0 = control) |
| Yᵢ = Tᵢ·Yᵢ(1) + (1−Tᵢ)·Yᵢ(0) | Observed outcome (fundamental problem: only one potential outcome observed) |
| ITE = Yᵢ(1) − Yᵢ(0) | Individual treatment effect (unobservable) |
| ATE = E[Y(1) − Y(0)] | Average Treatment Effect |
| ATT = E[Y(1) − Y(0) | T = 1] | Average Treatment Effect on the Treated |
| CATE = E[Y(1) − Y(0) | X = x] | Conditional Average Treatment Effect |

### Key Assumptions for Causal Identification

1. **Stable Unit Treatment Value Assumption (SUTVA):** No interference between units (one unit's treatment doesn't affect another's outcome) and only one version of treatment.
2. **Ignorability / Unconfoundedness:** Y(1), Y(0) ⟂ T | X (treatment assignment is independent of potential outcomes conditional on covariates). Also called "no unmeasured confounding."
3. **Positivity / Overlap:** 0 < P(T = 1 | X = x) < 1 for all x (every unit has non-zero probability of receiving either treatment).

**These assumptions are untestable from data alone.** They must be justified by design (randomization) or defended with subject matter knowledge and sensitivity analysis.

---

## Part 3: Identification Strategies

### Method Selection Decision Tree

```
You want to estimate the causal effect of T on Y.
│
├─ Was T randomly assigned?
│  ├─ YES → Analyze as randomized experiment
│  │  ├─ Simple: difference in means + t-test
│  │  ├─ Adjust for chance imbalance: ANCOVA
│  │  └─ Account for clustering: mixed model
│  └─ NO → Use observational causal method:
│
│     Is there a variable that determines T discontinuously?
│     ├─ YES → Regression Discontinuity Design
│     │
│     └─ NO → Is there a natural experiment / shock?
│        ├─ YES → Difference-in-Differences
│        │
│        └─ NO → Do you have a valid instrument?
│           ├─ YES → Instrumental Variables
│           │
│           └─ NO → Can you measure all confounders?
│              ├─ YES → G-formula / IPTW / Matching / Doubly Robust
│              └─ NO → Can you use sensitivity analysis?
│                 ├─ YES → E-value, Rosenbaum bounds
│                 └─ NO → Consider whether causal effect is identifiable at all
```

### 1. Randomized Experiments (Gold Standard)

**When:** Treatment assigned by investigator with randomization.
**Assumptions:** SUTVA, random assignment holds (no differential attrition, no non-compliance).
**Analysis:** ITT (intention-to-treat) primary; per-protocol and IV for non-compliance as sensitivity.
**Caveats:** External validity may be limited (treatment effect in experimental sample ≠ population).

### 2. Instrumental Variables (IV)

**When:** Z affects T, Z affects Y only through T, Z is independent of confounders of T and Y.

**Assumptions (for IV to be valid):**
1. **Relevance:** Z is correlated with T
2. **Exclusion restriction:** Z affects Y only through T (no direct path Z → Y)
3. **Independence:** Z is as good as randomly assigned (or conditional on X)
4. **Monotonicity:** Z affects T in one direction for all units (for LATE interpretation)

**Estimand:** Local Average Treatment Effect (LATE) — effect for compliers (units whose treatment status is changed by Z).

**Analysis:** Two-stage least squares (2SLS):
1. T̂ = α + βZ + γX (predict T from Z)
2. Y = α + τT̂ + γX (outcome on predicted T)

**First-stage diagnostics:** F-statistic > 10 (rule-of-thumb for strong instrument).

### 3. Regression Discontinuity Design (RDD)

**When:** Treatment assigned by a cutoff on a continuous variable (the "running variable").

**Assumptions:**
1. **Continuity:** The relationship between the running variable and potential outcomes is continuous at the cutoff
2. **No manipulation:** Units cannot precisely manipulate their running variable value around the cutoff

**Analysis:**
- Local linear regression around the cutoff
- Bandwidth selection (Imbens-Kalyanaraman, cross-validation)
- Polynomial specifications with robustness checks
- McCrary density test (check for manipulation of running variable)

**Estimand:** Local Average Treatment Effect at the cutoff (LATE).

**Key diagnostic:**
- Density plot of running variable (should be smooth at cutoff)
- Balance test on covariates at cutoff (should be smooth)
- Placebo tests at fake cutoffs (should show no effect)

### 4. Difference-in-Differences (DiD)

**When:** You have pre/post data for treated and untreated groups.

**Assumptions:**
1. **Parallel trends:** In the absence of treatment, the outcome would have evolved identically in treated and untreated groups
2. **No anticipation:** Treatment has no effect before it occurs
3. **No spillover:** Treatment doesn't affect control group outcomes

**Analysis:**
Y = β₀ + β₁·Treat + β₂·Post + β₃·(Treat × Post) + ε
where β₃ is the DiD estimate.

**Key diagnostics:**
- Plot pre-treatment trends (should be parallel)
- Placebo test: fake treatment date (should show no effect)
- Event study: plot treatment effect over time
- Sensitivity to parallel trends assumption? Use Rambachan-Roth (2023) approach

**Modern developments:**
- Two-way fixed effects (TWFE) can be biased with staggered adoption
- Use Callaway & Sant'Anna (2021), Sun & Abraham (2021), or Borusyak et al. (2024) estimators
- These handle heterogeneous treatment effects over time better

### 5. Matching & Weighting

**When:** You can measure all relevant confounders (unconfoundedness).

**Propensity Score:** e(X) = P(T = 1 | X)

| Method | Description |
|--------|-------------|
| **Propensity score matching (PSM)** | Match each treated unit to control unit(s) with nearest propensity score |
| **Nearest neighbor matching** | Match on Mahalanobis distance or other distance metric directly on covariates |
| **Coarsened Exact Matching (CEM)** | Coarsen continuous variables into strata, exact match within strata |
| **Inverse Probability of Treatment Weighting (IPTW)** | Weight by 1/e(X) for treated, 1/(1−e(X)) for control |
| **Doubly Robust** | Combine outcome regression with IPTW — consistent if either model is correct |
| **Targeted Maximum Likelihood (TMLE)** | Doubly robust with additional bias correction for efficiency |

**Post-matching diagnostics:**
- Standardized mean differences < 0.1 (balance achieved)
- Variance ratios between 0.5 and 2.0 (first moments balanced)
- Love plot (visualize balance improvement)

### 6. Synthetic Control

**When:** One or a few treated units, many potential control units.

**Idea:** Construct a weighted combination of control units that matches the treated unit's pre-treatment outcome trajectory. The post-treatment difference between treated and synthetic control is the treatment effect.

**Assumptions:**
- Pre-treatment fit is good
- No interference between treated and control units
- Control units are not affected by the treatment

**Analysis:** `Synth` (Abadie et al.) or augmented SC (Ben-Michael et al.).
**Diagnostic:** Placebo test — permute treatment across control units.

---

## Part 4: Sensitivity Analysis

**All observational causal analyses should include sensitivity analysis.** The core assumptions (ignorability, parallel trends, exclusion restriction) are untestable. Sensitivity analysis asks: **how far off must the assumption be for the conclusion to change?**

### Common Sensitivity Methods

| Method | When | What It Does |
|--------|------|-------------|
| **E-value** | General unmeasured confounding | Minimum strength of association between unmeasured confounder and both T and Y needed to explain away the observed effect |
| **Rosenbaum bounds** | Matched pairs | How large would hidden bias need to be to change significance? |
| **VanderWeele & Ding** | Binary confounders | Same as E-value but for binary exposures and outcomes |
| **Imbens' method** | General | How much of the treatment effect variance would need to be due to unconfoundedness? |
| **Cinelli & Hazlett** | OLS regression | Robustness of inference to confounding (partial R²) — how much residual variation must confounders explain? |
| **Placebo tests** | DiD, RDD | Use known fake treatment dates/cutoffs; if you find an effect, the real estimate is suspect |
| **Negative controls** | General | Use a control outcome that shouldn't be affected by treatment; if you find an effect, confounding is present |

### E-value Calculator (Mental)

```
E-value = RR_obs + sqrt(RR_obs × (RR_obs − 1))
        (for RR_obs > 1; symmetric for RR_obs < 1, use 1/RR_obs)

Interpretation: If an unmeasured confounder had an association of < E-value with both
treatment and outcome (after measured confounders), it could not explain away the observed
effect. Larger E-values = more robust findings.

Example: RR = 2.0 → E-value = 2.0 + √(2.0 × 1.0) = 2.0 + 1.41 = 3.41
Meaning: An unmeasured confounder would need >3.4× association with both T and Y to 
nullify the observed effect.
```

---

## Part 5: Causal Inference in A/B Testing & Product Analytics

| Scenario | Causal Method | Key Concern |
|----------|--------------|-------------|
| Randomized feature rollout | Difference in means | Network interference (social features) |
| Natural experiment (random error, scheduled downtime) | IV / DiD | Validity of natural experiment |
| Self-selected feature adoption | Matching / IPTW | Unmeasured confounding (motivated users) |
| Geographic rollout | DiD or Synthetic Control | Parallel trends assumption |
| Pre-post with no control | Interrupted time series | Secular trends, regression to mean |
| User chooses treatment | IV (instrument: random encouragement) | Weak instrument, LATE interpretation |

---

## Quick Reference: Causal Language

| Say This | Don't Say This |
|----------|---------------|
| "The estimate suggests a causal effect of X on Y under the assumption that..." | "X causes Y" |
| "We find that X is associated with a __ change in Y..." | "X impacts Y" |
| "In this randomized experiment, the treatment caused..." | Any causal claim from observational data without caveats |
| "The result is robust to unmeasured confounding of magnitude < E-value" | "We controlled for all confounders" |
| "The effect is identified under the assumption of parallel trends" | "We used DiD so it's causal" |
