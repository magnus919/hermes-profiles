# Regression Modeling Reference

## Model Selection Hierarchy

```
What's your outcome type?
│
├─ CONTINUOUS (unbounded, approximately normal)
│  └─ Linear regression → if assumptions violated, try:
│     ├─ Transform Y (log, Box-Cox, Yeo-Johnson)
│     ├─ Robust regression (M-estimation, Huber, quantile)
│     ├─ Generalized least squares (correlated errors)
│     └─ Nonparametric regression (GAM, kernel, Gaussian process)
│
├─ CONTINUOUS (bounded [0,1] or proportions)
│  └─ Beta regression (logit link) or fractional logit
│
├─ CONTINUOUS (positive, right-skewed)
│  └─ Gamma GLM (log link) or log-normal model
│
├─ BINARY (0/1)
│  ├─ Logistic regression (logit link — default)
│  ├─ Probit regression (normal CDF link — latent normal interpretation)
│  ├─ Complementary log-log (cloglog — asymmetric link, rare events)
│  └─ Robust Poisson (binary with common outcome, >10%)
│
├─ COUNT (non-negative integer)
│  ├─ Poisson regression (mean = variance)
│  │  └─ If overdispersed: Negative binomial regression
│  ├─ Zero-inflated model (excess structural zeros)
│  └─ Hurdle model (zero vs positive, then truncated count)
│
├─ ORDINAL (ordered categories)
│  └─ Proportional odds model (default)
│     └─ If proportional odds violated: partial proportional odds, adjacent category, or continuation ratio
│
├─ MULTINOMIAL (unordered categories)
│  └─ Multinomial logistic regression
│
├─ TIME-TO-EVENT
│  └─ Cox proportional hazards → if PH violated: stratified Cox, time-varying covariates, AFT
│
├─ TIME SERIES
│  └─ ARIMA / GARCH / state space / dynamic regression
│
├─ CLUSTERED / HIERARCHICAL
│  ├─ Linear/GLM + random effects (mixed models)
│  └─ GEE (population-averaged effects, robust to correlation misspecification)
│
└─ LONGITUDINAL
    ├─ Mixed effects models (subject-specific random effects)
    ├─ GEE (population-averaged)
    └─ Transition models (Markov-type, previous outcome as predictor)
```

---

## Linear Regression

### Assumptions & Diagnostics (in order of importance)

| Assumption | Violation Consequence | Diagnostic | Mitigation |
|-----------|----------------------|------------|------------|
| **Linearity** | Biased estimates, wrong functional form | Residuals vs fitted plot (check for patterns) | Add polynomials, splines, interaction terms, or GAM |
| **Independence of errors** | Inflated Type I error, wrong SEs | Durbin-Watson statistic (for serial correlation), plot residuals by order | GLS, cluster-robust SEs, mixed model |
| **Homoscedasticity** | Wrong SEs, inefficient estimates | Scale-location plot, Breusch-Pagan test | Heteroscedasticity-consistent SEs (HC1-HC3), weighted least squares |
| **Normality of residuals** | Invalid inference in small samples (large n → robust via CLT) | Q-Q plot, Shapiro-Wilk (n<50), Kolmogorov-Smirnov | Bootstrap inference, robust regression |
| **No influential points** | Estimates driven by few observations | Cook's distance, DFBETAS, DFFITS, leverage | Robust regression, drop/trim with documentation |
| **Multicollinearity** | Inflated SEs, unstable estimates | VIF > 5-10, condition index > 30 | Regularization (ridge/LASSO), remove/combine correlated predictors, PCA |

### Interpretation Guide

| Coefficient Type | Interpretation | Example |
|-----------------|---------------|---------|
| **Continuous (linear-linear)** | "A 1-unit increase in X is associated with a β-unit change in Y, holding other variables constant" | β = 2.3: "Each additional year of education is associated with a $2,300 increase in income" |
| **Binary (0/1)** | "The predicted Y is β units higher for the exposed group vs reference" | β = 5.1: "Women earn $5,100 more than men, controlling for other factors" |
| **Interaction (continuous × continuous)** | "The effect of X₁ on Y changes by β₃ for each 1-unit increase in X₂" | Simple slopes: plot at ±1 SD of moderator |
| **Interaction (binary × continuous)** | "The slope of X differs by β₃ between groups" | Plot separate regression lines for each group |
| **Log-transformed Y** | "A 1-unit change in X is associated with a 100·β % change in Y" | β = 0.03: "3% increase in Y per unit X" (approximate) |
| **Log-transformed X** | "A 1% increase in X is associated with β/100 unit change in Y" | β = 0.5: "1% more X → 0.005 unit more Y" |
| **Log-Log model** | "A 1% increase in X is associated with a β% change in Y" (elasticity) | β = 0.8: "1% more X → 0.8% more Y" |

### Common Pitfalls

| Pitfall | Why | Fix |
|---------|-----|-----|
| **Stepwise selection** | Inflated R², invalid inference, doesn't replicate | Use LASSO, domain knowledge, or AIC-based comparison of candidate models |
| **Interpreting coefficients when interactions are present** | Main effects are conditional (at zero of the moderator) | Center variables, plot marginal effects |
| **Ignoring nonlinearity** | Linear assumption hides U-shaped or threshold effects | Splines, GAMs, piecewise regression |
| **HARKing** (Hypothesizing After Results Known) | Inflated Type I error | Pre-register, split-sample (explore in half, confirm in half) |
| **p-value rounding** | "p = 0.051" is not trending | Report exact p-values and interpret continuously |
| **Not reporting uncertainty** | Overconfidence in point estimates | Always report CI/CrI with coefficients |

---

## Generalized Linear Models (GLMs)

### Canonical GLM Family Links

| Family | Default Link | Variance Function | Uses |
|--------|-------------|-------------------|------|
| Gaussian | Identity | σ² (constant) | Continuous outcomes |
| Binomial | Logit | μ(1−μ) | Binary, proportion |
| Poisson | Log | μ | Count data |
| Gamma | Inverse | μ² | Positive continuous, right-skewed |
| Inverse Gaussian | μ⁻² | μ³ | Positive continuous, very skewed |
| Negative Binomial | Log | μ + μ²/θ | Overdispersed counts |

### GLM Diagnostics (Beyond Linear)

- **Deviance residuals vs fitted** — check for pattern
- **DHARMa residuals** — simulated residuals for any GLM (recommended)
- **Overdispersion test** — for Poisson: residual deviance / df > 1.5 indicates overdispersion
- **Zero inflation** — compare observed vs predicted zeros for count models
- **Influence** — delta-betas and hat values (available via `statsmodels.graphics`)

---

## Mixed Effects / Hierarchical Models

### When to Use
- Repeated measures on same subjects (longitudinal)
- Data clustered in groups (students in schools, patients in hospitals)
- Crossed random effects (items and subjects in psycholinguistics)

### Standard Model Equation

```
Level 1: Yᵢⱼ = β₀ⱼ + β₁ⱼXᵢⱼ + εᵢⱼ
Level 2: β₀ⱼ = γ₀₀ + γ₀₁Wⱼ + u₀ⱼ
         β₁ⱼ = γ₁₀ + γ₁₁Wⱼ + u₁ⱼ
```

### Random Effect Structures

| Structure | Interpretation | N of Additional Parameters |
|-----------|---------------|---------------------------|
| Random intercept | Groups differ in baseline | 1 variance per grouping |
| Random slope + intercept | Groups differ in both baseline and covariate effect | 3 parameters: 2 variances, 1 covariance |
| Unstructured covariance | Full covariance matrix for repeated measures | k(k+1)/2 for k time points |

### Key Diagnostics
- **ICC** (intraclass correlation): proportion of variance due to between-group differences. ICC > 0.05 suggests multilevel modeling is beneficial.
- **Random effects Q-Q plot**: check normality of random effects
- **Centering**: group-mean centering for Level 1 predictors separates within- from between-group effects
- **Singular fit**: random effect variance estimated at zero → simplify random structure (Bates et al. 2015: keep maximal but drop zero-variance terms)

---

## Nonparametric & Semi-Parametric Regression

| Method | Use Case | Output |
|--------|----------|--------|
| **Smoothing splines** | Smooth nonlinear relationship, penalized | Fit with CV-chosen λ |
| **GAM (Generalized Additive Model)** | Multiple smoothed predictors, any GLM family | Partial dependence plots |
| **LOESS / LOWESS** | Local polynomial smoothing, one predictor | Smooth curve, no equation |
| **Kernel regression** | Nadaraya-Watson estimator | Smoothed conditional mean |
| **Gaussian Process** | Bayesian nonparametric regression | Full posterior over functions |
| **Regression Trees** | Decision tree for regression | Tree structure, interpretable |
| **Random Forest** | Ensemble of trees | Variable importance, partial dependence |
| **Gradient Boosting** | Sequential trees (XGBoost, LightGBM, CatBoost) | Usually best predictive accuracy |

### When to Choose Nonparametric Over Parametric
- The functional form is unknown and not theoretically specified
- The sample is large enough to estimate flexible relationships (>200 observations per smooth term)
- Prediction accuracy is more important than interpretability
- You've checked that parametric assumptions are violated and transformations don't fix it
