# Experimental Design Reference

## Design Taxonomy

```
What kind of study?
│
├─ EXPERIMENTAL (randomized assignment)
│  ├─ Completely Randomized Design (CRD)
│  │  └─ Subjects assigned randomly to treatments. Simplest design.
│  │  └─ Use when: homogeneous experimental units, no blocking factor
│  │
│  ├─ Randomized Complete Block Design (RCBD)
│  │  └─ Subjects grouped into blocks, randomized within each block
│  │  └─ Use when: known source of variability can be blocked (batch, day, location)
│  │
│  ├─ Split-Plot Design
│  │  └─ Hard-to-change factor applied at whole-plot level, easy-to-change at sub-plot
│  │  └─ Use when: some factors are expensive/difficult to change (temperature, batch)
│  │  └─ Warning: two error terms, complex analysis
│  │
│  ├─ Latin Square Design
│  │  └─ Block in two directions (row and column), each treatment appears once per row/col
│  │  └─ Use when: two nuisance factors need blocking
│  │  └─ Example: 4 operators × 4 days, testing 4 treatments
│  │
│  ├─ Factorial Design
│  │  ├─ Full factorial: all combinations of all factor levels
│  │  │  └─ Use when: interactions are of interest, factors ≤ 4
│  │  └─ Fractional factorial: subset of combinations
│  │     └─ Use when: many factors, screening design, interactions assumed negligible
│  │
│  ├─ Crossover Design
│  │  └─ Each subject receives multiple treatments in sequence
│  │  └─ Use when: washout period feasible, within-subject comparison more powerful
│  │  └─ Warning: carryover effects, period effects
│  │
│  ├─ Sequential / Adaptive Design
│  │  └─ Interim analyses, sample size re-estimation, adaptive randomization
│  │  └─ Use when: ethical concerns (clinical trials), expensive experiments
│  │  └─ Warning: complex statistics, must pre-specify stopping rules
│  │
│  └─ A/B Testing (online experiments)
│     └─ Special case of CRD with 2 treatments
│     └─ Considerations: sample ratio mismatch, novelty effects, network interference
│
├─ QUASI-EXPERIMENTAL (no randomization, but design estimates causal effect)
│  ├─ Difference-in-Differences (DiD)
│  │  └─ Compare treated vs untreated groups before and after treatment
│  │  └─ Assumption: parallel trends in absence of treatment
│  │
│  ├─ Regression Discontinuity (RD)
│  │  └─ Treatment assigned by cutoff on continuous variable
│  │  └─ Assumption: smooth relationship between running variable and outcome
│  │
│  ├─ Interrupted Time Series
│  │  └─ Compare outcome trajectory before vs after intervention
│  │  └─ Assumption: no other changes coinciding with intervention
│  │
│  └─ Propensity Score Methods
│     └─ Matching, stratification, IPTW
│     └─ Assumption: no unmeasured confounding
│
└─ OBSERVATIONAL (no randomization, descriptive or predictive)
    ├─ Cross-sectional: single time point
    ├─ Cohort: follow forward in time
    ├─ Case-control: select on outcome, look back
    └─ Ecological: aggregate-level data
```

---

## Power Analysis

### What It Answers
- Given α and β, how many subjects do I need to detect a given effect?
- Given α, N, and design, what effect size can I detect?
- Given N and expected effect, what power do I have?

### Key Parameters
- **α** (Type I error rate): usually 0.05 (two-sided) or 0.025 (one-sided)
- **β** (Type II error rate): usually 0.20 (power = 0.80)
- **Effect size**: standardized measure of the expected effect (Cohen's d, f, w, OR, etc.)
- **Sample size (N)**: total number of units
- **Design features**: number of groups, number of measurements, number of covariates, ICC (clustered designs)

### Power by Design Type

| Design | Test Statistic | Software | Key Inputs |
|--------|---------------|----------|------------|
| **Two-group comparison** (continuous, unpaired) | Two-sample t-test | `tt_ind_solve_power()` power | d, α, power → n_per_group |
| **Two-group comparison** (continuous, paired) | Paired t-test | `tt_solve_power()` power | d, α, power → n_pairs |
| **Two proportions** | z-test, chi-square | `zt_ind_solve_power()` or `power.prop.test()` | p₁, p₂, α → n_per_group |
| **One-way ANOVA** (k groups) | F-test | `power.anova()` or `pwr.anova.test()` | f, α, k → n_per_group |
| **Multiple regression** (p predictors) | F-test for R² | `FTestRegPower()` or `pwr.f2.test()` | f², p, α → N |
| **Logistic regression** | Wald test | `power.logistic()` or `vary()` approaches | OR, p_base, α → N |
| **Survival (log-rank)** | Log-rank test | `power.survival.test()` or `power.zt.survival()` | hazard ratio, median, α → events |
| **Cluster RCT** (m clusters, n/cluster) | Mixed model | `power.sim.normal()` or `clusterPower` | ICC, cluster size, m → power |
| **ANOVA interaction** | F-test | Manual or simulation | f, α, design → N |

### Sample Size Heuristics (Use Power Analysis Instead When Possible)

| Scenario | Rough Rule of Thumb |
|----------|---------------------|
| Detect large effect (d = 0.8) | ~26 per group (t-test, α=0.05, 80% power) |
| Detect medium effect (d = 0.5) | ~64 per group |
| Detect small effect (d = 0.2) | ~394 per group |
| A/B test (10% relative increase from 10% base) | ~15,000 per arm |
| A/B test (10% relative increase from 50% base) | ~3,100 per arm |
| Cluster RCT (ICC = 0.05, 20 per cluster) | Multiply individual-sample N by ~2.7 |
| Interaction in factorial design | 4× the sample for main effect |

### Power Analysis Protocol

```
1. Determine primary outcome measure
2. State minimum clinically/practically important effect
3. Choose α (usually 0.05) and desired power (usually 0.80)
4. Select appropriate test and design
5. Compute required N
6. Check feasibility: do you have this N?
7. If no: reduce effect size, accept lower power, or change design (e.g., paired instead of independent)
8. If yes: account for attrition (inflate N by expected dropout rate)
9. Pre-register the analysis plan including power assumptions
```

---

## A/B Testing Framework

### Standard Protocol

1. **Define the metric.** Primary metric must be one, pre-specified, measurable, and tied to a business/investigator decision.
2. **Determine minimum detectable effect (MDE).** What's the smallest effect worth acting on?
3. **Compute sample size.** Account for multiple metrics with Bonferroni correction on α.
4. **Randomize properly.** At the unit of analysis level. Check for sample ratio mismatch (SRM).
5. **Pre-register.** Analysis plan including exclusion criteria, stopping rule, and primary analysis method.
6. **Run for pre-computed duration.** Don't peek (or use sequential testing).
7. **Analyze.** Intention-to-treat primary analysis, per-protocol sensitivity. Report effect size with CI.
8. **Check assumptions.** Balance checks, novelty effects, network interference (SUE/stable unit treatment value assumption violation).

### Common A/B Testing Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Peeking at results | Inflation of Type I error rate | Sequential testing (always valid confidence intervals) |
| Stopping early when significant | Same as above | Pre-specify duration, or use sequential design |
| Multiple metrics without correction | Inflated false positive rate | Pre-specify primary, use Bonferroni/Holm on secondaries |
| Sample ratio mismatch (SRM) | Indicates randomization failure | Check χ² test on group assignment ratio |
| Novelty effect | Early effect decays as users adapt | Run long enough (2+ full business cycles) |
| Network interference | Treatment spills to control (social networks, marketplace) | Cluster randomization, design experiments at higher level |
| Segment hunting | Finding significance in subgroups | Pre-specify subgroups or correct for multiple comparisons |

### Minimum Detectable Effect by Sample Size (Continuous, 80% power, α=0.05)

| N per arm | MDE (Cohen's d) | MDE (proportion, base=50%) | MDE (proportion, base=10%) |
|-----------|-----------------|---------------------------|---------------------------|
| 100 | 0.40 | ±14% pp | ±12% pp |
| 500 | 0.18 | ±6.3% pp | ±5.4% pp |
| 1,000 | 0.13 | ±4.4% pp | ±3.8% pp |
| 5,000 | 0.06 | ±2.0% pp | ±1.7% pp |
| 10,000 | 0.04 | ±1.4% pp | ±1.2% pp |
| 50,000 | 0.02 | ±0.6% pp | ±0.5% pp |

---

## Blocking & Covariate Adjustment

### When to Block
- You have a pre-treatment variable known to affect the outcome
- You have a limited number of experimental units and want to reduce error variance
- You can group units into homogeneous blocks

### When to Use Covariate Adjustment (ANCOVA)
- Continuous pre-treatment variable correlated with outcome
- Increases statistical power beyond blocking alone
- Valid even in randomized experiments (does not introduce bias if pre-specified)

### When NOT to Adjust
- Post-treatment variables (they're outcomes, not covariates — introduces selection bias)
- Variables affected by treatment (collider bias)
- Multiple covariates without pre-specification (researcher degrees of freedom)

---

## Factorial Design Quick Reference

| Factors | Full Factorial Runs | ½ Fraction Runs | Resolution |
|---------|-------------------|----------------|------------|
| 2 | 4 | — | Full |
| 3 | 8 | 4 | III (½) |
| 4 | 16 | 8 | IV (½) |
| 5 | 32 | 16 | V (½) |
| 6 | 64 | 32 | VI (½) |
| 7 | 128 | 64 | VII (½) |

**Resolution guide:**
- **Resolution III:** Main effects may be confounded with two-way interactions. Screening only.
- **Resolution IV:** Main effects clear of two-way interactions; two-way interactions may be confounded with each other.
- **Resolution V:** Main effects and two-way interactions are clear. Three-way interactions may be confounded.
