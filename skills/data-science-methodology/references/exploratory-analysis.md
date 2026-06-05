# Exploratory Data Analysis

## First Pass

- **Structure:** What are the data types? Missing values? Unique values per column?
- **Distributions:** Histogram for each numeric column. Value counts for each categorical column.
- **Correlations:** Pairwise correlation matrix. Flag strong correlations (>0.8) for multicollinearity.
- **Missingness:** Is data missing at random? Does missingness correlate with other variables?

## Visualization Before Modeling

Always plot the data before building a model. Summary statistics hide:
- Multimodal distributions (same mean, different shapes)
- Outliers and extreme values
- Non-linear relationships
- Interaction effects

## Common Patterns

| Pattern | What It Suggests |
|---------|-----------------|
| Skewed distribution | Log transform may be needed |
| Bimodal distribution | Possible mixture of two populations |
| Heavy tails | Outliers likely; robust methods needed |
| Step changes in time series | Regime change or intervention effect |
