# Data Scientist Agent Skill

An [Agent Skills](https://agentskills.io)-compatible skill that enables any AI agent to operate at PhD-level expertise in data science, statistics, and machine learning.

## What This Skill Provides

When loaded, this skill transforms how an agent reasons about data science problems:

- **Classifies questions** into advice, analysis, research, design, review, or methodology — and applies the appropriate level of rigor
- **Checks assumptions before methods** — the core PhD-level principle that separates good analysis from bad
- **Reaches for the right reference** — statistical tests, experimental designs, causal inference, regression models, Bayesian workflow
- **Runs power analysis, assumption diagnostics, model comparison, and effect size calculations** with real scripts
- **Generates analysis reports and experimental plans** in pre-registration format

## Skill Structure

```
data-scientist/
├── SKILL.md                              # Decision framework & trigger conditions
├── references/
│   ├── statistical-methodology.md        # Test selection, assumptions, effect sizes
│   ├── experimental-design.md            # Design taxonomy, power, A/B testing
│   ├── causal-inference-framework.md     # DAGs, potential outcomes, identification
│   ├── regression-modeling.md            # Model hierarchy, diagnostics, GLMs
│   └── bayesian-workflow.md              # Prior, MCMC, model comparison
├── scripts/
│   ├── power-analysis.py                 # Sample size / detectable effect calculator
│   ├── assumption-diagnostics.py         # Model assumption checking
│   ├── model-comparison.py               # AIC/BIC/CV model comparison
│   ├── effect-size-calculator.py         # Effect sizes with confidence intervals
│   └── experimental-design.py            # Randomization schedule generator
└── assets/
    ├── report-template.md                # Analysis report standard format
    └── experimental-plan-template.md     # Pre-registration-style planning
```

## Triggers

Load this skill when the task involves:

- **Statistical methods:** hypothesis testing, regression, Bayesian analysis, p-values, confidence intervals
- **Research design:** experiments, A/B testing, power analysis, sample size, randomization
- **Causal questions:** effect estimation, causality, treatment effects, identification strategies
- **Modeling:** machine learning, prediction, model selection, cross-validation
- **General:** "analyze this data," "what model should I use," "review this analysis"

## Usage Examples

```bash
# Power analysis for a t-test
python scripts/power-analysis.py --design ttest-ind --effect-size 0.5 --alpha 0.05 --power 0.80

# Power analysis with R output
python scripts/power-analysis.py --design anova --k 3 --effect-size 0.25 --engine r

# Effect size from means and SDs
python scripts/effect-size-calculator.py --design cohens-d --mean1 10 --mean2 8 --sd1 2.5 --sd2 2.8 --n1 30 --n2 30

# Model comparison
python scripts/model-comparison.py --models "OLS AIC=1200 BIC=1220 k=5" "GLM AIC=1190 BIC=1215 k=6"

# Generate experimental design
python scripts/experimental-design.py --design crd --treatments Control Treatment --n-per-group 20 --seed 42
```

All scripts accept `--json` for machine-readable output and `--engine r` for R equivalents.

## Requirements

Python 3.10+ with:
- `scipy >= 1.10` (power analysis, effect sizes, diagnostics)
- `numpy >= 1.24` (most scripts)
- `statsmodels >= 0.14` (assumption diagnostics from fitted models, model comparison)
- `pandas >= 2.0` (data loading, model comparison)

Optional: `rpy2` for R integration via `--engine r`.

## Domain Boundaries

This skill provides **statistical and methodological expertise**, not domain knowledge. It is designed to collaborate with domain experts who know their application field (medicine, economics, biology, engineering, etc.) but need rigorous data science methodology applied to their problems.

## Language Support

All scripts default to Python computation. The `--engine r` flag outputs equivalent R code, making this skill useful in R-dominant environments.

## License

MIT
