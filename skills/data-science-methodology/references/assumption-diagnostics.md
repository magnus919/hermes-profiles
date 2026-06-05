# Assumption Diagnostics

## For Linear Models

- **Linearity:** Residuals vs fitted plot — should show no pattern
- **Independence:** Durbin-Watson test for autocorrelation
- **Homoscedasticity:** Scale-location plot, Breusch-Pagan test
- **Normality of residuals:** Q-Q plot, Shapiro-Wilk test
- **Influence:** Cook's distance for influential points

## For Any Model

- **Sensitivity analysis:** Do results change with reasonable parameter variations?
- **Cross-validation:** Does performance generalize to held-out data?
- **Feature importance:** Which features drive predictions? Do they make sense?
- **Error analysis:** Where does the model fail? Systematic patterns in errors?

## Red Flags

- Model performs much better on training than test data → overfitting
- Model performs much better than expected → data leakage
- Model learns spurious correlations → check for confounders
- Feature importance contradicts domain knowledge → investigate
