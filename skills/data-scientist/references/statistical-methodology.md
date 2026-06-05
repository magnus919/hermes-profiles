# Statistical Methodology Reference

## Test Selection Decision Tree

```
What type of outcome (dependent variable)?
│
├─ CONTINUOUS (interval/ratio)
│  ├─ 1 group → One-sample t-test (normal) or Wilcoxon signed-rank (non-normal)
│  ├─ 2 independent groups → Independent t-test (normal, equal var) or Welch's t-test (normal, unequal var) or Mann-Whitney U (non-normal)
│  ├─ 2 paired groups → Paired t-test (normal) or Wilcoxon signed-rank (non-normal)
│  ├─ 3+ independent groups → One-way ANOVA (normal, equal var, independent) or Kruskal-Wallis (non-normal)
│  ├─ 3+ paired groups → Repeated measures ANOVA (normal, sphericity) or Friedman test (non-normal)
│  ├─ Controlling for covariates → ANCOVA (normal, equal slopes, independent)
│  └─ Multiple predictors → Linear regression / GLM
│
├─ BINARY (yes/no, success/failure)
│  ├─ 1 group / compare to known proportion → Binomial test / One-proportion z-test
│  ├─ 2 independent groups → Chi-square test of independence or Fisher's exact (small cells) or Two-proportion z-test
│  ├─ 2 paired groups → McNemar's test
│  ├─ 3+ groups → Chi-square test
│  ├─ Multiple predictors → Logistic regression
│  └─ Rare outcome → Logistic regression with Firth correction or exact methods
│
├─ COUNT (0, 1, 2, 3...)
│  ├─ Unbounded → Poisson regression (mean = variance) or Negative binomial (variance > mean)
│  ├─ Excess zeros → Zero-inflated Poisson/NB or Hurdle model
│  └─ Over time → Poisson/NB with offset for exposure
│
├─ ORDINAL (Likert, ranked)
│  ├─ Compare 2 groups → Mann-Whitney U (independent) or Wilcoxon signed-rank (paired)
│  ├─ Compare 3+ groups → Kruskal-Wallis
│  └─ Multiple predictors → Ordinal logistic regression (proportional odds)
│
├─ TIME-TO-EVENT (survival)
│  ├─ Compare 2 groups → Log-rank test
│  ├─ Multiple predictors → Cox proportional hazards
│  └─ Proportional hazards violated → Accelerated failure time models
│
├─ CATEGORICAL (nominal, 3+ levels)
│  ├─ Outcome is categorical → Chi-square test of independence or Multinomial logistic regression
│  └─ Agreement between raters → Cohen's kappa (2 raters) or Fleiss' kappa (3+)
│
├─ TIME SERIES (repeated over time)
│  ├─ Single series forecasting → ARIMA, Exponential smoothing, Prophet
│  ├─ Multiple series comparison → Structural time series, Dynamic regression
│  ├─ Seasonal patterns → Seasonal decomposition (STL), SARIMA
│  └─ Anomaly detection → Change point detection, Twitter/AnomalyDetection
│
└─ MULTIVARIATE (multiple outcomes)
    ├─ Dimensionality reduction → PCA, t-SNE, UMAP, Factor analysis
    ├─ Group structure → Cluster analysis (k-means, hierarchical, DBSCAN)
    └─ Multiple DVs by group → MANOVA (normal, equal cov matrices)
```

---

## Assumptions Reference Table

| Method | Assumptions | How to Check | What If Violated |
|--------|-------------|-------------|-------------------|
| **One-sample t-test** | Independence, normality | Q-Q plot, Shapiro-Wilk test (n < 50), Anderson-Darling | Wilcoxon signed-rank test |
| **Independent t-test** | Independence, normality, equal variance | Levene's test, F-test of variances, Q-Q plot | Welch's t-test (unequal var), Mann-Whitney (non-normal) |
| **Paired t-test** | Normality of differences, independence of pairs | Q-Q plot of differences | Wilcoxon signed-rank test |
| **One-way ANOVA** | Independence, normality (within groups), equal variance (homoscedasticity) | Levene's test, Shapiro-Wilk per group, Q-Q plot, residual plot | Welch's ANOVA (unequal var), Kruskal-Wallis (non-normal) |
| **Repeated measures ANOVA** | Normality, sphericity (equal variances of differences), independence between subjects | Mauchly's test for sphericity, ε correction (Greenhouse-Geisser, Huynh-Feldt) | Friedman test, or use mixed effects model with unstructured covariance |
| **Linear regression** | Linearity, independence of errors, homoscedasticity, normality of residuals, no multicollinearity | Residuals vs fitted plot, Q-Q plot, Breusch-Pagan test, VIF (< 5-10), Durbin-Watson, Cook's distance for influential points | Robust SEs (heteroscedasticity), weighted least squares, transformations (non-linearity), GLS (correlated errors) |
| **Logistic regression** | Linearity in logit (continuous predictors independent of log-odds), independence | Box-Tidwell test (linearity), Hosmer-Lemeshow goodness-of-fit, AUC-ROC, residual plots | Splines or polynomials (non-linearity), Firth regression (rare events/separation) |
| **Chi-square test** | Expected frequency ≥ 5 in each cell, independence of observations | Check expected counts | Fisher's exact test (2x2), Monte Carlo simulation (larger tables) |
| **Cox proportional hazards** | Proportional hazards, independent censoring | Schoenfeld residuals test (global + per covariate), log-log plots | Time-dependent covariates, stratified Cox, AFT models |
| **ANCOVA** | Normality, equal variance, independence, linear relationship with covariate, equal slopes assumption | Homogeneity of slopes test (covariate × group interaction) | Add interaction term, use nonparametric ANCOVA (Quade) |
| **MANOVA** | Multivariate normality, equal covariance matrices, independence | Box's M-test, Q-Q plots per variable | Separate ANOVAs with Bonferroni, PERMANOVA |

---

## Effect Size Guide

| Test / Design | Effect Size Measure | Interpretation | CI Available |
|--------------|-------------------|----------------|-------------|
| **t-test** (independent) | Cohen's d = (M₁−M₂)/s_pooled | 0.2=small, 0.5=medium, 0.8=large | Yes (non-central t) |
| **t-test** (paired) | Cohen's d_z = t/√n | Same conventions | Yes |
| **ANOVA** (one-way) | η² = SS_between/SS_total | 0.01=small, 0.06=medium, 0.14=large | Yes |
| **ANOVA** | Partial η² | Same (for multifactor designs) | Yes |
| **ANOVA** (fixed effects) | Cohen's f = √(η²/(1−η²)) | 0.10=small, 0.25=medium, 0.40=large | Yes |
| **Chi-square** | Cramér's V = √(χ²/(n·min(r−1,c−1))) | 0.1=small, 0.3=medium, 0.5=large | Yes (bootstrap) |
| **2×2 tables** | Odds ratio | OR=1 no effect, OR>1 increased odds | Yes (Woolf) |
| **2×2 tables** | Risk ratio / Relative risk | RR=1 no effect | Yes (Katz) |
| **2×2 tables** | Risk difference | Absolute difference in proportions | Yes (Newcombe) |
| **Correlation** | r (Pearson) | 0.1=small, 0.3=medium, 0.5=large | Yes (Fisher z) |
| **Correlation** | r_s (Spearman) | Same conventions | Yes |
| **Regression** | R² | Variance explained | Yes |
| **Regression** | Cohen's f² = R²/(1−R²) | 0.02=small, 0.15=medium, 0.35=large | Yes |
| **Bayesian** | Bayes factor BF₁₀ | 1-3=weak, 3-10=moderate, 10-30=strong, 30-100=very strong, >100=extreme evidence for H₁ | Yes (HDI) |

### Reporting Examples

- *"The mean difference was 3.2 points (95% CI [1.8, 4.6]), t(58) = 3.41, p = 0.001, Cohen's d = 0.87."*
- *"The treatment group had 2.3× the odds of recovery (OR 2.3, 95% CI [1.4, 3.8], χ²(1) = 12.4, p < 0.001)."*
- *"The model explained 34% of variance in outcome (R² = 0.34, F(3, 96) = 16.5, p < 0.001, Cohen's f² = 0.52)."*

---

## Multiple Testing Corrections

| Correction | Use When | How It Works | Power |
|-----------|---------|-------------|-------|
| **Bonferroni** | Small number of planned comparisons | α/m | Low — conservative |
| **Holm-Bonferroni** | Same, slightly less conservative | Sequential rejective | Better than Bonferroni |
| **Benjamini-Hochberg (BH)** | Exploratory analysis, many tests | Controls FDR | Higher — recommended for omics/exploratory |
| **Benjamini-Yekutieli (BY)** | Dependent tests, same as BH | Controls FDR under dependency | Lower than BH |
| **Tukey HSD** | All pairwise comparisons after ANOVA | Studentized range distribution | Good, designed for this case |
| **Dunnett** | Multiple comparisons vs a single control | Comparison-specific critical values | Good for this case |
| **Scheffé** | Post-hoc contrasts not planned in advance | Most flexible, most conservative | Low |
| **FDR (q-value)** | Thousands of tests (genomics, fMRI) | Estimates proportion of false discoveries | High |

**Rule of thumb:** For 2-5 planned comparisons, use Bonferroni or Holm. For dozens of exploratory tests, use BH at FDR=0.05. For pairwise post-ANOVA, use Tukey HSD. Never cherry-pick which p-values to correct.

---

## Bayesian Alternatives for Common Frequentist Tests

| Frequentist | Bayesian Alternative | Key Benefit |
|------------|---------------------|-------------|
| One-sample t-test | Bayesian one-sample t-test (BEST) | Can quantify evidence for H₀ via BF |
| Two-sample t-test | Bayesian two-sample t-test (BEST) | Robust to outliers via heavy-tailed likelihood |
| ANOVA | Bayesian ANOVA (BANOVA) | Model comparison via BFs, no sphericity assumption |
| Linear regression | Bayesian linear regression | Prior regularization, full posterior for coefficients |
| Logistic regression | Bayesian logistic regression (with priors) | Handles separation, shrinks extreme estimates |
| Chi-square test | Beta-Binomial model, contingency table Bayes factor | More intuitive: what's the posterior difference in proportions? |
| Correlation | Bayesian correlation (beta* prior on ρ) | Posterior distribution of ρ |
| t-test with non-inferiority | Bayesian region of practical equivalence (ROPE) | Direct probability of clinically meaningful difference |
| Meta-analysis | Bayesian hierarchical meta-analysis | Handles heterogeneity, small studies better |

---

## Best Practices & Red Flags

### Green Flags (good analysis practices)
- Pre-registered analysis plan (when possible)
- Effect sizes with CIs reported alongside p-values
- Assumption checks documented (and violations addressed)
- Sensitivity analyses reported (different specifications, outlier exclusion)
- Code and data available for reproduction
- Multiple testing corrections applied where appropriate
- Missing data mechanism discussed (MCAR, MAR, MNAR)
- Power analysis conducted before data collection

### Red Flags (poor analysis practices)
- p-values without effect sizes
- Stepwise variable selection (forward/backward)
- P-hacking: trying tests until significance
- Ignoring violations of assumptions
- No missing data handling (or claiming "no missing data" unrealistically)
- Over-interpreting non-significant results as "no effect" without equivalence testing
- Reporting only significant results (cherry-picking)
- Using parametric tests on clearly non-normal data without justification
- "p = 0.06 is marginally significant" (it's not — p = 0.06 is non-significant)
