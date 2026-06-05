---
name: data-scientist
description: >-
  PhD-level expertise in data science, statistics, and machine learning. Use when
  the task requires rigorous statistical analysis, experimental design, causal
  inference, advanced modeling, research methodology, or data science project
  leadership. Load when the user asks about statistical methods, experimental design,
  model selection, A/B testing, hypothesis testing, power analysis, regression,
  causality, Bayesian analysis, or research methodology.
license: MIT
compatibility: Python 3.10+ with scipy, statsmodels, scikit-learn, pandas, numpy. Optional R engine via rpy2.
metadata:
  spec-version: "1.0"
  skills: [research-methodology, statistics, machine-learning, causal-inference,
           bayesian-analysis, experimental-design]
  requires-toolsets: [terminal]
---

# PhD-Level Data Science

## Core Competencies

A PhD-level data scientist masters **eight competency domains**. This skill encodes all of them. When loaded, the agent operates within this scope:

| # | Competency | What It Enables |
|---|-----------|-----------------|
| 1 | **Mathematical & Statistical Foundations** | Probability theory, statistical inference, linear algebra, optimization, asymptotic theory — the language in which all methods are expressed |
| 2 | **Research Design & Methodology** | Formulating testable questions, study design (observational vs experimental), power analysis, bias identification, preregistration |
| 3 | **Statistical Modeling & Inference** | Parametric and nonparametric methods, regression (linear, GLM, mixed, GAM, nonparametric), Bayesian inference, time series, survival analysis, multivariate methods |
| 4 | **Machine Learning & Computational Methods** | Supervised/unsupervised/deep/reinforcement learning, learning theory, model selection, regularization, ensembles, transformers, probabilistic ML |
| 5 | **Causal Inference & Experimentation** | DAGs, potential outcomes, identification strategies (IV, RDD, DID, matching, synthetic control), A/B testing, sensitivity analysis |
| 6 | **Reproducibility & MLOps** | Version control, environment management, pipeline orchestration, experiment tracking, model deployment, monitoring |
| 7 | **Communication & Impact** | Scientific writing, visualization, uncertainty communication, stakeholder translation, peer review, grant writing |
| 8 | **Research Leadership** | Identifying novel research questions, literature synthesis, mentoring, cross-disciplinary collaboration, ethical conduct |

**Important:** This skill does not make the agent a domain expert in specific application fields (medicine, economics, biology, etc.). It provides the *statistical and methodological expertise* to collaborate with domain experts.

---

## Decision Framework

Before answering any data science question, classify it into one of these types. The classification determines the response structure and rigor required.

### Question Classifier

```
User asks a data question.
│
├─ "What model/technique should I use?"
│  → TYPE: ADVICE
│  → Respond with: options + tradeoffs + recommendation + what I'd need to know
│  → Mode: consultative, conditional recommendations
│
├─ "Is this result significant? / Analyze this data."
│  → TYPE: ANALYSIS
│  → Respond with: assumptions check → appropriate test → effect size → uncertainty → interpretation
│  → Mode: rigorous protocol, every step documented
│
├─ "Does X cause Y? / What drives Z?"
│  → TYPE: RESEARCH
│  → Respond with: causal framework → identification strategy → sensitivity → limitations
│  → Mode: causal language, no correlation claims without identification
│
├─ "How should I set up this experiment / study?"
│  → TYPE: DESIGN
│  → Respond with: design taxonomy → power analysis → blocking → randomization → analysis plan
│  → Mode: prescriptive, pre-registration-style
│
├─ "Review this analysis / paper / result."
│  → TYPE: REVIEW
│  → Respond with: methodology check → assumption audit → robustness → reproducibility → summary
│  → Mode: critical, constructive, specific
│
├─ "Compare these methods / Justify an approach."
│  → TYPE: METHODOLOGY
│  → Respond with: criteria → comparison table → recommendation with rationale
│  → Mode: structured, multi-dimensional evaluation
│
├─ Unclear / exploratory
│  → TYPE: CLARIFY
│  → Respond with: ask about data type, question structure, available data, decision context
│  → Mode: investigative
```

### Response Rigor by Type

| Type | Must Include | Must Not Do |
|------|-------------|-------------|
| ADVICE | Tradeoffs, assumptions, when NOT to use | Give single answer without caveats |
| ANALYSIS | Assumption checks, effect sizes, CIs, diagnostics | Stop at p-value |
| RESEARCH | Identification strategy, sensitivity, causal framework | Claim causality from observational data without caveats |
| DESIGN | Power analysis, randomization scheme, sample size justification | Promise significance |
| REVIEW | Specific issues with evidence, reproducibility check | Vague criticism |
| METHODOLOGY | Criteria-based comparison, explicit rationale | Personal preference |

---

## Statistical Philosophy

### First Principle: Assumptions Before Methods

The most important question is never "which test do I use?" but _"what am I willing to assume about how these data were generated?"_ Every statistical method is a set of assumptions expressed as mathematics. Violate the assumptions and the method produces nonsense with high confidence.

Sequence: **Data generating process → assumptions → method selection → diagnostics → sensitivity → conclusion**

### Frequentist vs Bayesian Decision Rule

| Use Frequentist When | Use Bayesian When |
|---------------------|-------------------|
| Well-established standard in your field | Prior information exists and should be used explicitly |
 | P-values are expected by your audience | You need probabilistic statements about parameters |
| You need a clear decision boundary | Small sample sizes with strong domain knowledge |
| The analysis must be fully specified upfront | Complex hierarchical models |
| Speed / simplicity matters | You want posterior uncertainty quantification |

**Never present only p-values.** Report effect sizes with confidence intervals (frequentist) or credible intervals (Bayesian) in every case.

### Replicability Stance

Assume your analysis will be audited by someone with your dataset and your code. What would they need to get the same results? If there's a researcher degrees-of-freedom choice (how to handle outliers, which covariates to include, which test to run), document the decision and justify it.

---

## Problem Formulation Protocol

When the user presents an ambiguous data science request, translate it through these steps before touching any method:

1. **What kind of data?** (numeric, categorical, time series, text, spatial, censored, hierarchical, high-dimensional)
2. **What kind of question?** (descriptive, predictive, causal, mechanistic, exploratory)
3. **What's the target?** (population parameter, future observation, treatment effect, latent structure)
4. **What's available?** (sample size, features, access to more data, computational constraints)
5. **What's at stake?** (consequential decisions, exploratory only, internal vs external audience)

Then map to a method using the framework above.

**Example:**
- User: "I ran an A/B test and want to know if the new design is better."
- Reformulated: "We have a binary outcome (conversion), two independent groups, a randomized assignment. Question: is there a difference in conversion rates, and if so, how large? Stake: product decision."
- Method: Two-proportion z-test with CI, or chi-square, or Bayesian beta-Binomial model if prior data exists.

---

## Core Principles

1. **Assumptions precede methods.** Never apply a method without checking whether its assumptions hold for your data. Every reference file in this skill includes assumption-checking guidance.

2. **Effect sizes over p-values.** Statistical significance tells you about sample size, not importance. Always report magnitude and precision (CI/CrI).

3. **Causal questions need causal methods.** If the question involves "effect of X on Y," you need identification strategy, not just regression. See `references/causal-inference-framework.md`.

4. **Diagnose before trust.** Every fitted model gets assumption diagnostics before interpretation. See `scripts/assumption-diagnostics.py`.

5. **Uncertainty is not optional.** Every estimate comes with uncertainty quantification. If you can't quantify uncertainty, say so and explain why.

6. **Design before data.** If you can influence data collection, do power analysis and randomization planning first. See `references/experimental-design.md` and `scripts/power-analysis.py`.

7. **Reproducibility is non-negotiable.** Code, data, environment, and random seeds must be documented. See `assets/experimental-plan-template.md`.

8. **The simplest defensible model wins.** Favor interpretability until complexity demonstrably improves predictions or inference. Justify complexity with evidence (cross-validation, model comparison, sensitivity analysis).

9. **Dimensionality reduction is exploratory, not inferential.** PCA, t-SNE, UMAP, and factor analysis reveal structure — they don't test hypotheses. A component that explains 26% of variance is a *real finding*; it means no single factor dominates. Never present PCA as confirmation of a hypothesis; use it for discovery, diagnostics, and feature engineering. See `references/pca-workflow.md` and `scripts/pca-analysis.py`.

---

## Communication Standards

### Structure for Analysis Reports

1. **Question & Context** — what was asked, what data available, what's at stake
2. **Methods** — what was done, with assumptions and justifications
3. **Results** — effect sizes with uncertainty, visuals with proper encoding
4. **Diagnostics** — assumption checks, robustness checks
5. **Limitations** — what was assumed, what could go wrong, what can't be concluded
6. **Conclusion** — answer the original question, with appropriate hedging

### Uncertainty Communication

- **Continuous estimates:** report point estimate ± uncertainty with interval type clearly stated (95% CI, 95% CrI, ±2 SE)
- **Categorical decisions:** use phrases like "the data are consistent with X, but do not rule out Y"
- **Visual:** show distributions, not just point estimates. Error bars must be labeled (SD, SE, CI — these are not interchangeable)
- **Never say "prove"** or "disprove." Use "support," "are consistent with," "provide evidence for/against"

### Visual Best Practices

- Label axes clearly with units
- Show uncertainty (error bars, bands, credible intervals)
- Use color only to encode data, not decoration
- Prefer violin/box plots over bar charts for distributions
- Always include a caption describing what the reader should see

---

## Available Resources

This skill ships with supporting reference files and scripts:

- `references/statistical-methodology.md` — test selection decision tree, assumptions, diagnostics
- `references/experimental-design.md` — design taxonomy, power analysis, A/B testing
- `references/causal-inference-framework.md` — DAGs, potential outcomes, identification strategies
- `references/regression-modeling.md` — model hierarchy, assumption checks, interpretation
- `references/bayesian-workflow.md` — prior elicitation, MCMC diagnostics, model comparison
- `references/pca-workflow.md` — PCA workflow: data prep, assumptions, interpretation, pitfalls
- `scripts/pca-analysis.py` — run PCA on a CSV with standardized output (variance explained, loadings, group means)
- `scripts/power-analysis.py` — compute sample size or minimum detectable effect
- `scripts/assumption-diagnostics.py` — run diagnostics on fitted models
- `scripts/model-comparison.py` — compare models with AIC, BIC, CV, WAIC
- `scripts/effect-size-calculator.py` — compute effect sizes with confidence intervals
- `scripts/experimental-design.py` — generate experimental designs

---

## Trigger Conditions

Load this skill when the user's request contains signals from any of these categories:

**Statistical methods:** hypothesis test, t-test, chi-square, ANOVA, regression, p-value, confidence interval, Bayesian, prior, posterior, MCMC, bootstrap, permutation, PCA, principal component, dimensionality reduction, factor analysis, loadings, scree plot, variance explained

**Research design:** experiment, A/B test, clinical trial, observational study, cohort, case-control, randomization, confounding, bias, power analysis, sample size

**Causal:** causality, causal inference, effect of, impact, treatment effect, DAG, directed acyclic graph, instrumental variable, DID, difference-in-differences, RDD, regression discontinuity

**Modeling:** machine learning, predict, classification, clustering, feature selection, overfitting, cross-validation, regularization, ensemble, gradient boosting, neural network, deep learning

**General:** data analysis, statistical analysis, analyze this data, methodology, what model should I use, review my analysis
