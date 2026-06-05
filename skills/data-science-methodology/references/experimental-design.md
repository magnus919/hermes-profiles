# Experimental Design

## Key Questions Before Running an Experiment

1. **What's the causal question?** "Does X cause Y?" — be precise about X and Y
2. **What's the counterfactual?** What would happen without the intervention?
3. **How will you randomize?** Unit of randomization, stratification, blocking
4. **What's the minimum detectable effect?** How large must the effect be to matter?
5. **What's the sample size?** Power analysis to determine required N

## Common Threats to Validity

| Threat | Description | Mitigation |
|--------|-------------|------------|
| Selection bias | Treatment and control groups differ systematically | Randomization, stratification |
| Confounding | A third variable affects both treatment and outcome | Control for confounders, DAGs |
| Hawthorne effect | Subjects change behavior because they're being observed | Blind or unobtrusive measurement |
| Attrition bias | Subjects drop out differentially | Track and analyze dropouts |
| Multiple comparisons | Testing many hypotheses inflates false positive rate | Correction (Bonferroni, FDR) |
