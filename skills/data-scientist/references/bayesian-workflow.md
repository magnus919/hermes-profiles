# Bayesian Workflow Reference

## The Bayesian Workflow (Gelman et al. 2020)

Bayesian analysis is not "put a prior on everything and sample." It's an iterative process:

```
1. Model building
   │
   ├─ 2. Prior predictive check (do priors produce plausible data?)
   │  └─ If not, revise priors
   │
   ├─ 3. Inference (MCMC, VI, or exact)
   │
   ├─ 4. Posterior predictive check (does model reproduce observed data?)
   │  └─ If not, revise model
   │
   ├─ 5. Model comparison (WAIC, LOO, cross-validation)
   │
   └─ 6. Sensitivity analysis (try different priors, different likelihoods)
```

---

## 1. Prior Elicitation

### Types of Priors

| Prior Type | Description | When to Use |
|-----------|-------------|-------------|
| **Flat / Improper** | No information, ∝ 1 | Default reference, rarely recommended |
| **Weakly Informative** | Wide but finite: Normal(0, 10), Cauchy(0, 5) | Default for most parameters; shrink extreme values |
| **Regularizing** | Shrink toward zero: Normal(0, 1), Laplace(0, 1) | Many predictors, prevents overfitting |
| **Informative** | Narrowly centered on known value | Strong prior knowledge (previous studies, physical constraints) |
| **Hierarchical** | Prior on prior parameters (hyperpriors) | Multiple groups sharing information |

### Prior Recommendation Cheat Sheet

| Parameter Type | Default Prior | Why |
|---------------|--------------|-----|
| **Regression coefficient** (continuous predictor) | Normal(0, 1) or Normal(0, 2.5) | 95% of coefficients within ±2-5 units on logit/probit scale |
| **Intercept** | Normal(0, 10) | Wide enough for most scales |
| **Standard deviation** (positive) | Half-Cauchy(0, 2.5), Exponential(1), or Inverse-Gamma(3, 3) | Half-Cauchy preferred; avoids near-zero mass of inverse-gamma |
| **Correlation** (between -1 and 1) | LKJ(2) | Slightly regularizes toward zero correlation |
| **Variance parameter** (hierarchical) | Exponential(1) or Half-Cauchy(0, 2) | Robust to scale differences |
| **Proportion / probability** | Beta(1, 1) or Beta(2, 2) | Uniform vs slightly central |
| **Log-odds** (logistic) | Normal(0, 1.5) or Student-t(3, 0, 2.5) | Gelman et al. 2008: default for logistic regression |

### Prior Predictive Check Protocol

1. Sample from the prior distribution
2. Generate synthetic data from the prior-predictive distribution
3. Plot the distribution of synthetic data
4. Ask: "Could data generated this way actually occur in my problem?"
5. If the synthetic data implies impossible values (negative variances, 150-year-old humans, etc.): tighten the prior
6. If the synthetic data is too constrained (never allows realistic values): widen the prior

---

## 2. Computation

### MCMC Methods

| Method | Software | When to Use |
|--------|----------|-------------|
| **Hamiltonian Monte Carlo (HMC)** | Stan (via PyStan, CmdStanPy), PyMC (NUTS), NumPyro (NUTS) | Default for continuous parameters. Efficient exploration of posterior. |
| **Variational Inference (VI)** | PyMC (ADVI), NumPyro (SVI), Stan (VB) | Large datasets, fast approximate inference. Check fit against HMC on subset. |
| **Gibbs Sampling** | JAGS, BUGS | Legacy. Only when HMC is impractical. |
| **SMC / ABC** | PyMC (SMC), custom | Discrete parameters, likelihood-free inference |
| **Laplace Approximation** | INLA, statsmodels | Fast, accurate for latent Gaussian models (GLMM, spatial) |

### MCMC Diagnostics

| Diagnostic | What It Checks | Threshold | How to Fix |
|-----------|---------------|-----------|------------|
| **R-hat (Ř)** | Convergence across chains | < 1.01 (modern threshold, Vehtari et al. 2021) | Run longer, reparameterize, increase warmup |
| **Effective Sample Size (ESS)** | Number of independent samples | bulk-ESS > 400, tail-ESS > 400 | Run longer, thinner |
| **Trace plot** | Mixing, stationarity | No trends, good overlap between chains | Re-run with more iterations |
| **Autocorrelation** | Sampling efficiency | Lag-1 autocorrelation < 0.5 | Re-parameterize (centered vs non-centered) |
| **Divergent transitions** | HMC-specific: geometry problems | 0 divergences | Increase adapt_delta (0.80 → 0.95-0.99), reparameterize |
| **BFMI (Bayesian Fraction of Missing Information)** | Energy transition efficiency | BFMI > 0.2-0.3 | Re-parameterize non-centered |

### Reparameterization: Centered vs Non-Centered

| Type | Formula | When |
|------|---------|------|
| **Centered** | μ_normal = α + βX, σ ~ Half-Cauchy | Weak data, strong priors |
| **Non-centered** | μ_raw ~ Normal(0, 1), μ = α + βX + σ·μ_raw | Strong data, weak priors, hierarchical models |

Non-centered breaks the dependence between group-level mean and variance parameters, improving HMC geometry. Try non-centered when you see divergent transitions.

---

## 3. Model Comparison

### Information Criteria

| Criterion | What It Measures | When to Use | Formula |
|-----------|-----------------|-------------|---------|
| **WAIC** (Watanabe-Akaike) | Expected log pointwise predictive density + correction | Bayesian models, MCMC | WAIC = lppd − p_waic |
| **LOO-CV** (Leave-One-Out) | Same as WAIC but with Pareto-smoothed importance sampling | Bayesian models, MCMC (via `loo()` in ArviZ, loo package) | Computed via PSIS-LOO |
| **AIC** | −2 logL + 2k | Frequentist models, no prior | — |
| **BIC** | −2 logL + k log n | Frequentist models, nested comparison | — |
| **DIC** | Deviance + effective parameters | Bayesian models, MCMC (less stable than WAIC) | — |

### Model Comparison Decision Tree

```
Compare candidate models:
│
├─ Same likelihood, same data, nested?
│  ├─ Use information criteria (WAIC/LOO) for predictive comparison
│  └─ Use cross-validation for predictive accuracy
│
├─ Different likelihoods (e.g., Poisson vs Negative Binomial)?
│  └─ Use WAIC/LOO on same data, or cross-validation of predictive score
│
├─ Need to quantify evidence for H₀ vs H₁?
│  └─ Use Bayes Factor (BF₁₀) — but sensitive to prior choice. Report sensitivity.
│
└─ Which model is more useful given decision context?
    └─ Consider predictive performance (CV), interpretability, computational cost
```

### Bayes Factor Guidelines

| BF₁₀ | Evidence for H₁ |
|------|----------------|
| 1-3 | Weak / Anecdotal |
| 3-10 | Moderate |
| 10-30 | Strong |
| 30-100 | Very Strong |
| >100 | Extreme |

**Warning:** Bayes factors are very sensitive to prior choice. A diffuse prior can arbitrarily deflate the BF in favor of H₁. Always report sensitivity to prior width.

### Cross-Validation in Bayesian Models

- **Approximate LOO-CV** via PSIS (Pareto-smoothed importance sampling) — built into ArviZ
- **k-fold CV** — run inference on k-1 folds, evaluate on held-out fold. More robust but more expensive
- **Diagnostic:** Pareto k parameter. k < 0.5: reliable. 0.5 < k < 0.7: ok but watch. k > 0.7: unreliable (use k-fold instead)

---

## 4. Posterior Predictive Checking

### Core Idea
If the model is adequate, data generated from the posterior predictive distribution should resemble the observed data.

### Checks

| Check | What It Tests | Visualization |
|-------|--------------|--------------|
| **Mean / variance** | First and second moments | Overlay observed statistic on posterior of statistic from replicated datasets |
| **Extreme values** | Tail behavior | Probability of max(y_rep) ≥ max(y) |
| **Distribution shape** | Whole-distribution fit | Density overlay of y_rep and y |
| **Discrepancy measures** | Specific features you care about | Bayesian p-value (χ², skewness, proportion of zeros) |
| **Residual vs fitted** | Model structure violations | Plot standardized residuals from posterior mean vs fitted values |

### Bayesian p-values

A Bayesian p-value near 0.5 indicates good fit. Values near 0 or 1 indicate systematic discrepancy between model and data. Because it's the posterior probability that the test statistic is more extreme in the replicated data than in the observed, it doesn't have the same issues as frequentist p-values.

---

## 5. Hierarchical / Multilevel Bayesian Models

### Shrinkage

Hierarchical models borrow strength across groups. Group-level estimates are "shrunk" toward the population mean, with the amount of shrinkage determined by the group-level variance:

```
Groups with small N → more shrinkage (less reliable estimates pulled toward mean)
Groups with large N → less shrinkage (more data to estimate their own parameter)
```

### The 8 Schools Example (classic)

The canonical hierarchical Bayesian example: 8 schools each ran an experiment. Estimates vary widely due to small samples. Hierarchical model produces more realistic, shrunken estimates with proper uncertainty.

### When to Go Hierarchical:
- Multi-level data structure (students in classes in schools)
- You want to estimate group-level parameters while sharing information
- Small sample sizes in some groups (partial pooling)
- You need to model variation across groups explicitly

---

## 6. Software Quick Reference

| Task | PyMC | NumPyro | Stan |
|------|------|---------|------|
| Basic regression | `pm.Model()` with `pm.Normal()` | `numpyro.sample()` with `dist.Normal()` | `model { ... }` block |
| MCMC sampling | `pm.sample(1000)` | `mcmc.run(rng_key, ...)` | `./sample` via cmdstan |
| HMC NUTS | Default | `NUTS` | Default |
| Variational inference | `pm.fit(method='advi')` | `SVI` with `AutoDiagonalNormal` | `stan optimize` (VB deprecated) |
| Prior predictive | `pm.sample_prior_predictive()` | `Predictive()` with prior_samples | `generated quantities` block |
| Posterior predictive | `pm.sample_posterior_predictive()` | `Predictive()` with posterior_samples | `generated quantities` block |
| LOO/WAIC | `az.loo()`, `az.waic()` | `az.loo()`, `az.waic()` | `loo::loo()` in R |
| Visualization | ArviZ (`az.plot_trace`, etc.) | ArviZ | `bayesplot`, `shinystan` |

### Installation Notes

- **PyMC:** `pip install pymc arviz`
- **NumPyro:** `pip install numpyro arviz jax jaxlib`
- **Stan (Python):** `pip install pystan` (v3) or `cmdstanpy` (must install CmdStan separately: `install_cmdstan()`)
- **Stan (R):** `install.packages("rstan")`, `brms` for formula-based interface
- **R with Python:** use `rpy2` bridge or `reticulate` in R
