# Analysis Report Template

## 1. Question & Context

**Research question:** [One sentence: what are we trying to learn?]

**Motivation:** [Why does this question matter? What decision depends on the answer?]

**Data source:** [Where did the data come from? Collection method, timeframe, sample frame]

**Pre-registration:** [Link to preregistration if applicable. If not, flag any exploratory analyses.]

---

## 2. Data

**Sample size:** N = [n] ([n1] in group 1, [n2] in group 2)

**Inclusion/exclusion criteria:** [Who/what was included and excluded, and why]

**Missing data:** [Amount, pattern (MCAR/MAR/MNAR), handling method]

**Variables:**

| Variable | Type | Role | Description |
|----------|------|------|-------------|
| [name] | [continuous/binary/ordinal/etc.] | [outcome/predictor/covariate] | [description] |
| ... | | | |

---

## 3. Methods

**Analytic approach:** [e.g., two-sample t-test, linear regression with covariates, Bayesian hierarchical model]

**Justification:** [Why this method? What assumptions are we willing to make?]

**Pre-specified analyses:** [What was planned before seeing the data]

**Exploratory analyses:** [What was added after seeing the data]

**Software:** [Python 3.x with scipy/statsmodels/scikit-learn, R 4.x with package vX]

---

## 4. Assumption Checks

| Assumption | Method | Result | Status |
|------------|--------|--------|--------|
| Normality (Group 1) | Shapiro-Wilk | W = [value], p = [value] | ✓ / ✗ / N/A |
| Equal variance | Levene's test | F = [value], p = [value] | ✓ / ✗ / N/A |
| ... | | | |

**Summary:** [All assumptions met / violations detected and addressed]

---

## 5. Results

**Primary analysis:**

| Estimate | SE | 95% CI | Test Statistic | p-value | Effect Size [95% CI] |
|----------|-----|--------|----------------|---------|---------------------|
| [value] | [value] | [lower, upper] | [t/χ²/F/Z = value] | [value] | [d/η²/V/OR = value [CI]] |

**Secondary analyses:**

[Brief summary of secondary results]

**Visualization:**

[Figure: appropriate plot with clear axes, uncertainty shown, caption below]

*Figure 1: [Caption describing what the reader should see]*

---

## 6. Diagnostics & Robustness

**Sensitivity analyses:**

| Analysis | Result | Conclusion |
|----------|--------|------------|
| Main analysis | [original estimate] | — |
| Excluding outliers | [estimate] | Consistent / different |
| Alternative specification | [estimate] | Robust / sensitive |
| Different analysis method | [estimate] | Robust / sensitive |

**Residual diagnostics:** [Pattern in residuals? Influential points?]

---

## 7. Limitations

1. **[Assumption that may be violated]:** [How this could affect results]
2. **[Confounding not addressed]:** [Direction and magnitude of potential bias]
3. **[Generalizability concern]:** [Population or setting limits]
4. **[Measurement issue]:** [Reliability, validity of measures]

---

## 8. Conclusion

[One paragraph answering the original question, with appropriate uncertainty. Include:

- What we found (with effect size and precision)
- What we didn't find (null results with equivalence if applicable)
- What remains uncertain
- Practical implications

Example: "We found moderate evidence that the intervention increases response rate by 12 percentage points (95% CI [4, 20], p = 0.003, d = 0.45). This effect was robust to excluding outliers and controlling for baseline covariates. However, the result may not generalize to non-English-speaking populations, and the mechanism remains unclear."]

---

## Appendix

**Full model output:** [Link or table]

**Code:** [Link to repository]

**Data:** [Access information or note about availability]
