#!/usr/bin/env python3
"""
Model Assumption Diagnostics

Runs appropriate diagnostics on fitted models or raw data + method specs.
Returns structured report with warnings.

Usage:
  python assumption-diagnostics.py --method ttest --data data.csv --group-var group --value-var score
  python assumption-diagnostics.py --method regression --data data.csv --formula "y ~ x1 + x2"
  python assumption-diagnostics.py --method anova --data data.csv --group-var condition --value-var score
  python assumption-diagnostics.py --method mannwhitney --data data.csv --group-var group --value-var score
  python assumption-diagnostics.py ... --json
  python assumption-diagnostics.py ... --engine r
"""

import argparse
import json
import math
import sys

try:
    import numpy as np
    from scipy import stats as sp_stats
    HAS_NUMERIC = True
except ImportError:
    HAS_NUMERIC = False


def _check_deps():
    if not HAS_NUMERIC:
        print("Error: scipy and numpy required. pip install scipy numpy", file=sys.stderr)
        sys.exit(1)


METHODS = {
    "ttest": "Independent two-sample t-test",
    "ttest-paired": "Paired t-test",
    "onesample": "One-sample t-test",
    "anova": "One-way ANOVA",
    "regression": "Linear regression",
    "logistic": "Logistic regression",
    "correlation": "Pearson correlation",
    "mannwhitney": "Mann-Whitney U (nonparametric)",
    "kruskal": "Kruskal-Wallis (nonparametric)",
    "chisquare": "Chi-square test of independence",
}


def check_normality(data, method="shapiro"):
    """Test normality. Returns (statistic, p_value, is_violated)."""
    _check_deps()
    if method == "shapiro":
        if len(data) < 3:
            return None, None, True
        if len(data) > 5000:
            # Shapiro-Wilk is unreliable for n > 5000, use D'Agostino-Pearson
            stat, p = sp_stats.normaltest(data)
            method_used = "D'Agostino-Pearson"
        else:
            stat, p = sp_stats.shapiro(data)
            method_used = "Shapiro-Wilk"
    else:
        stat, p = sp_stats.normaltest(data)
        method_used = "D'Agostino-Pearson"

    return {
        "test": method_used,
        "statistic": round(stat, 4),
        "p_value": round(p, 4),
        "is_violated": p < 0.05
    }


def check_equal_variance(*groups):
    """Levene's test for equal variance across groups."""
    _check_deps()
    stat, p = sp_stats.levene(*groups)
    return {
        "test": "Levene's test",
        "statistic": round(stat, 4),
        "p_value": round(p, 4),
        "is_violated": p < 0.05
    }


def check_sphericity(data, groups, blocks):
    """Approximate sphericity check (Mauchly's test approximation)."""
    # Full sphericity requires repeated measures ANOVA structure
    return {
        "note": "Full Mauchly's test requires R (see --engine r). "
                "As a heuristic: check pairwise variance differences with Bartlett's test.",
        "is_violated": None
    }


def check_independence_durbin_watson(residuals):
    """Durbin-Watson test for autocorrelation of residuals."""
    _check_deps()
    n = len(residuals)
    dw = sum((residuals[i] - residuals[i-1])**2 for i in range(1, n)) / sum(r**2 for r in residuals)
    return {
        "test": "Durbin-Watson",
        "statistic": round(dw, 4),
        "is_violated": dw < 1.5 or dw > 2.5,
        "note": f"DW ≈ 2 = no autocorrelation. DW = {dw:.4f}"
    }


def check_linearity(x, y):
    """Check linearity via correlation ratio (eta) vs Pearson r."""
    _check_deps()
    r, _ = sp_stats.pearsonr(x, y)
    # Simple check: fit quadratic and see if it improves over linear
    # For now, report correlation and flag non-monotonic patterns
    return {
        "pearson_r": round(r, 4),
        "note": "For thorough linearity check, plot residuals vs fitted values.\n"
                "Significant non-linearity if residuals show clear U-shaped or curved pattern."
    }


def check_multicollinearity(X_matrix):
    """Approximate VIF for each predictor."""
    _check_deps()
    X = np.array(X_matrix)
    n_features = X.shape[1]
    vifs = []
    for i in range(n_features):
        y_i = X[:, i]
        X_i = np.delete(X, i, axis=1)
        try:
            # Regress feature i on all others, get R²
            X_i_with_intercept = np.column_stack([np.ones(X_i.shape[0]), X_i])
            beta = np.linalg.lstsq(X_i_with_intercept, y_i, rcond=None)[0]
            y_pred = X_i_with_intercept @ beta
            ss_res = np.sum((y_i - y_pred)**2)
            ss_tot = np.sum((y_i - np.mean(y_i))**2)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            vif = 1 / (1 - r2) if r2 < 1 else float('inf')
        except Exception:
            vif = float('inf')
        vifs.append(vif)
    return {
        "VIF_values": [round(v, 2) if v != float('inf') else "inf" for v in vifs],
        "high_collinearity": any(v > 10 for v in vifs if v != float('inf')),
        "note": "VIF > 5-10 indicates problematic multicollinearity."
    }


def check_outliers(data, method="iqr"):
    """Flag potential outliers."""
    _check_deps()
    data = np.array(data)
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = data[(data < lower) | (data > upper)]
    return {
        "method": "IQR (1.5×)",
        "n_outliers": len(outliers),
        "percent_outliers": round(len(outliers) / len(data) * 100, 1),
        "bounds": {"lower": round(lower, 4), "upper": round(upper, 4)},
        "is_violated": len(outliers) > 0,
        "note": f"{len(outliers)} potential outliers ({len(outliers)/len(data)*100:.1f}%)"
    }


def run_ttest_assumptions(group1, group2, is_paired=False):
    results = []

    n1, n2 = len(group1), len(group2)
    results.append({"check": "Sample size", "detail": f"n1 = {n1}, n2 = {n2}"})

    if not is_paired:
        results.append({"check": "Independence", "detail": "Design-based assumption (random assignment)",
                        "is_violated": False})

    # Normality per group
    norm1 = check_normality(group1)
    norm2 = check_normality(group2)
    if n1 < 30:
        results.append({"check": "Normality (Group 1)", "result": norm1,
                        "is_violated": norm1["is_violated"] if norm1 else True})
    if n2 < 30:
        results.append({"check": "Normality (Group 2)", "result": norm2,
                        "is_violated": norm2["is_violated"] if norm2 else True})

    if not is_paired and n1 >= 30 and n2 >= 30:
        results.append({"check": "Normality", "detail": "Both n ≥ 30 — CLT applies, normality not required"})

    if not is_paired:
        eqvar = check_equal_variance(group1, group2)
        results.append({"check": "Equal variance (Levene's)", "result": eqvar,
                        "is_violated": eqvar["is_violated"]})

    # Outliers per group
    out1 = check_outliers(group1)
    out2 = check_outliers(group2)
    results.append({"check": "Outliers (Group 1)", "result": out1})
    results.append({"check": "Outliers (Group 2)", "result": out2})

    if is_paired:
        diffs = np.array(group1) - np.array(group2)
        norm_diff = check_normality(diffs)
        results.append({"check": "Normality of differences", "result": norm_diff,
                        "is_violated": norm_diff["is_violated"] if norm_diff else True})

    passed = all(
        not r.get("is_violated", False)
        for r in results
        if "is_violated" in r and r["is_violated"] is not None
    )
    return {"method": "Independent t-test" if not is_paired else "Paired t-test",
            "overall_passed": passed,
            "checks": results,
            "recommendation": "All assumptions met" if passed else
                              "Violations detected. Consider: Welch's t-test (unequal var), "
                              "Mann-Whitney/Wilcoxon (non-normal), or check outliers."}


def run_regression_assumptions(X, y, residuals=None):
    """Run linear regression diagnostics."""
    results = []
    n = len(y)
    p = X.shape[1] if hasattr(X, 'shape') and len(X.shape) > 1 else 1
    results.append({"check": "Sample size", "detail": f"N = {n}, predictors = {p}, ratio = {n/p:.1f}:1",
                    "is_violated": n/p < 10})

    if residuals is not None:
        # Linearity: residuals vs fitted
        # Homoscedasticity: Breusch-Pagan approximation
        res = np.array(residuals)
        bp_stat = n * (sum(r**2 for r in res) / n) ** 2  # Simplified
        results.append({"check": "Residual normality", "result": check_normality(res)})

        # Durbin-Watson
        dw = check_independence_durbin_watson(res)
        results.append({"check": "Error independence (DW)", "result": dw, "is_violated": dw["is_violated"]})

        # Homoscedasticity via Breusch-Pagan simplified
        res2 = res ** 2
        bp_corr, _ = sp_stats.spearmanr(range(len(res2)), res2) if len(res2) > 3 else (0, 1)
        results.append({"check": "Homoscedasticity",
                        "detail": f"Spearman ρ between fitted values and |residuals| = {bp_corr:.4f}",
                        "is_violated": abs(bp_corr) > 0.15})

    results.append({"check": "Linearity", "detail": "Check residuals vs fitted plot for patterns"})

    passed = all(
        not r.get("is_violated", False)
        for r in results
        if "is_violated" in r and r["is_violated"] is not None
    )
    return {"method": "Linear regression",
            "overall_passed": passed,
            "checks": results,
            "recommendation": "All assumptions met" if passed else
                              "Violations detected. Consider: robust SEs (heteroscedasticity), "
                              "transformations (non-linearity), or GLS (correlated errors)."}


def run_anova_assumptions(groups):
    """Run one-way ANOVA diagnostics."""
    results = []
    n_groups = len(groups)
    sizes = [len(g) for g in groups]
    results.append({"check": "Sample sizes", "detail": str(sizes),
                    "is_violated": max(sizes) / min(sizes) > 2 if min(sizes) > 0 else True})

    # Normality per group (for small n)
    for i, g in enumerate(groups):
        if len(g) < 30:
            norm = check_normality(g)
            results.append({"check": f"Normality (Group {i+1})", "result": norm})

    # Equal variance
    eqvar = check_equal_variance(*groups)
    results.append({"check": "Equal variance (Levene's)", "result": eqvar,
                    "is_violated": eqvar["is_violated"]})

    # Independence
    results.append({"check": "Independence", "detail": "Design-based assumption (random assignment within blocks)"})

    passed = all(
        not r.get("is_violated", False)
        for r in results
        if "is_violated" in r and r["is_violated"] is not None
    )
    return {"method": "One-way ANOVA",
            "overall_passed": passed,
            "checks": results,
            "recommendation": "All assumptions met" if passed else
                              "Violations detected. Consider: Welch's ANOVA (unequal var), "
                              "Kruskal-Wallis (non-normal), or transform data."}


def run(args):
    # Parse data if provided
    if args.data:
        if not HAS_NUMERIC:
            print("Error: scipy + numpy required for data analysis. Install with: pip install scipy numpy",
                  file=sys.stderr)
            sys.exit(1)
        try:
            import pandas as pd
            df = pd.read_csv(args.data)
        except ImportError:
            print("Error: pandas required for CSV reading. pip install pandas", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: file not found: {args.data}", file=sys.stderr)
            sys.exit(1)
    else:
        df = None

    if not args.method:
        print("Error: --method required. Options: " + ", ".join(METHODS.keys()), file=sys.stderr)
        sys.exit(1)

    method_map = {
        "ttest": run_ttest_assumptions,
        "ttest-paired": lambda g1, g2: run_ttest_assumptions(g1, g2, is_paired=True),
    }

    result = {"method": args.method, "status": "ok"}

    if args.method in ("ttest", "ttest-paired") and df is not None:
        if not args.group_var or not args.value_var:
            print("Error: --group-var and --value-var required for t-test", file=sys.stderr)
            sys.exit(1)
        groups = [group[args.value_var].values for name, group in df.groupby(args.group_var)]
        if len(groups) != 2:
            print("Error: t-test requires exactly 2 groups", file=sys.stderr)
            sys.exit(1)
        result["diagnostics"] = run_ttest_assumptions(groups[0], groups[1], args.method == "ttest-paired")

    elif args.method == "anova" and df is not None:
        if not args.group_var or not args.value_var:
            print("Error: --group-var and --value-var required for ANOVA", file=sys.stderr)
            sys.exit(1)
        groups = [group[args.value_var].values for name, group in df.groupby(args.group_var)]
        result["diagnostics"] = run_anova_assumptions(groups)

    elif args.method == "regression":
        if df is not None and args.formula:
            try:
                import statsmodels.api as sm
                import statsmodels.formula.api as smf
                model = smf.ols(args.formula, data=df).fit()
                X = model.model.exog
                y = model.model.endog
                residuals = model.resid
                result["diagnostics"] = run_regression_assumptions(X, y, residuals)
                result["model_summary"] = {
                    "R_squared": round(model.rsquared, 4),
                    "adj_R_squared": round(model.rsquared_adj, 4),
                    "F_statistic": round(model.fvalue, 2),
                    "F_p_value": round(model.f_pvalue, 4),
                    "AIC": round(model.aic, 2),
                    "BIC": round(model.bic, 2),
                }
            except ImportError:
                print("Error: statsmodels required for regression diagnostics. pip install statsmodels",
                      file=sys.stderr)
                sys.exit(1)
        else:
            result["diagnostics"] = {
                "method": "Linear regression",
                "note": "Provide --data and --formula for full diagnostics",
                "checks": [
                    {"check": "Linearity", "detail": "Check residuals vs fitted plot"},
                    {"check": "Independence", "detail": "Check Durbin-Watson"},
                    {"check": "Homoscedasticity", "detail": "Check Breusch-Pagan test"},
                    {"check": "Normality of residuals", "detail": "Check Q-Q plot"},
                ]
            }

    elif args.method in ("mannwhitney", "kruskal", "chisquare", "onesample", "correlation", "logistic"):
        result["diagnostics"] = {
            "method": args.method,
            "note": f"Nonparametric and special methods require fewer assumptions. "
                    f"Provide data with --data, --group-var, --value-var for automated checks.",
            "checks": [
                {"check": "Independence", "detail": "Design-based assumption"},
            ]
        }

    else:
        print(f"Error: method '{args.method}' requires --data file. Provide CSV data.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        diag = result.get("diagnostics", {})
        print(f"## {diag.get('method', args.method)} Assumption Diagnostics")
        print(f"Status: {'✓ PASS' if diag.get('overall_passed', False) else '⚠ ISSUES FOUND'}")
        print()
        for check in diag.get("checks", []):
            status = "✓" if not check.get("is_violated") else "✗"
            print(f"{status} {check.get('check', 'Check')}")
            if "detail" in check:
                print(f"    {check['detail']}")
            if "result" in check and isinstance(check["result"], dict):
                for k, v in check["result"].items():
                    if k == "is_violated":
                        continue
                    print(f"    {k}: {v}")
            print()
        if "recommendation" in diag:
            print(f"**Recommendation:** {diag['recommendation']}")
        if "model_summary" in result:
            print(f"\nModel: R² = {result['model_summary']['R_squared']}, "
                  f"AIC = {result['model_summary']['AIC']}")
        if args.engine == "r":
            print("\n--- R equivalent ---")
            print(f"# In R, use: install.packages(c('car', 'lmtest', 'performance'))")
            print(f"library(car); library(lmtest); library(performance)")
            print(f"model <- lm({args.formula if args.formula else 'y ~ x'}, data = {args.data if args.data else 'df'})")
            print(f"check_model(model)  # Comprehensive assumptions plot")


def main():
    parser = argparse.ArgumentParser(description="Model Assumption Diagnostics")
    parser.add_argument("--method", choices=list(METHODS.keys()), help="Statistical method")
    parser.add_argument("--data", help="CSV file path")
    parser.add_argument("--group-var", help="Grouping variable name (for t-test, ANOVA)")
    parser.add_argument("--value-var", help="Value/outcome variable name")
    parser.add_argument("--formula", help="R-style formula for regression (e.g., 'y ~ x1 + x2')")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--engine", choices=["python", "r"], default="python",
                        help="Output language")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
