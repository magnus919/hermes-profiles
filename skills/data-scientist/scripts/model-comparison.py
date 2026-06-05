#!/usr/bin/env python3
"""
Model Comparison Tool

Compares multiple models using information criteria and cross-validation.
Accepts model fit statistics directly or fits models from data.

Usage:
  python model-comparison.py --models "OLS AIC=1200 BIC=1220 k=5 LL=-590" "GLM AIC=1190 BIC=1215 k=6 LL=-588"
  python model-comparison.py --from-data data.csv --formulas "y~x1" "y~x1+x2" "y~x1*x2"
  python model-comparison.py ... --json
  python model-comparison.py ... --engine r
"""

import argparse
import json
import math
import sys
import re


def compute_aic(ll, k):
    """AIC = -2*LL + 2*k"""
    return -2 * ll + 2 * k


def compute_bic(ll, k, n):
    """BIC = -2*LL + k*ln(n)"""
    return -2 * ll + k * math.log(n)


def compute_aicc(aic, k, n):
    """Corrected AIC for small samples."""
    return aic + (2 * k * (k + 1)) / (n - k - 1) if n > k + 1 else float('inf')


def compute_weights(values):
    """Compute Akaike weights or similar model probabilities from IC values."""
    if not values:
        return []
    min_val = min(values)
    rel_likelihoods = [math.exp(-0.5 * (v - min_val)) for v in values]
    total = sum(rel_likelihoods)
    return [rl / total for rl in rel_likelihoods]


def model_entry_from_string(s):
    """Parse 'Name AIC=1200 BIC=1220 k=5 LL=-590 [n=100]'"""
    parts = s.split()
    if not parts:
        return None
    entry = {"name": parts[0]}
    for p in parts[1:]:
        if "=" in p:
            key, val = p.split("=", 1)
            key = key.lower()
            if key in ("aic", "bic", "aicc", "ll"):
                entry[key] = float(val)
            elif key in ("k", "n"):
                entry[key] = int(float(val))
    return entry if len(entry) > 1 else None


def compute_from_formulas(data_file, formulas, family="gaussian"):
    """Fit models from R-style formulas and compute ICs."""
    try:
        import pandas as pd
        import statsmodels.api as sm
        import statsmodels.formula.api as smf
    except ImportError:
        print("Error: pandas and statsmodels required for --from-data. pip install pandas statsmodels",
              file=sys.stderr)
        sys.exit(1)

    try:
        df = pd.read_csv(data_file)
    except Exception as e:
        print(f"Error reading {data_file}: {e}", file=sys.stderr)
        sys.exit(1)

    n = len(df)
    models = []
    for formula in formulas:
        try:
            if family == "gaussian":
                model = smf.ols(formula, data=df).fit()
            elif family == "binomial":
                model = smf.logit(formula, data=df).fit(disp=0)
            else:
                model = smf.ols(formula, data=df).fit()

            k = model.df_model + 1  # +1 for intercept
            ll = model.llf
            aic = model.aic
            bic = model.bic
            models.append({
                "name": formula,
                "aic": round(aic, 2),
                "bic": round(bic, 2),
                "k": int(k),
                "ll": round(ll, 2),
                "n": n,
                "r_squared": round(getattr(model, "rsquared", 0), 4),
            })
        except Exception as e:
            print(f"Warning: model '{formula}' failed: {e}", file=sys.stderr)
            continue

    return models


def compute_loo_cv(models_data, data_file):
    """Approximate LOO-CV using information criteria (not full CV)."""
    # WAIC and LOO require full posterior samples
    # For frequentist models, AIC/based weights serve as approximations
    return {
        "note": "Full LOO-CV requires Bayesian models with MCMC posterior samples. "
                "For frequentist models, AICc weights or k-fold CV are recommended instead.",
        "alternative": "Use k-fold cross-validation or Bayesian model (PyMC/Stan/NumPyro) with loo package."
    }


def run(args):
    models = []

    if args.models:
        for s in args.models:
            entry = model_entry_from_string(s)
            if entry:
                models.append(entry)

    if args.from_data:
        if not args.formulas:
            print("Error: --formulas required with --from-data", file=sys.stderr)
            sys.exit(1)
        fitted = compute_from_formulas(args.from_data, args.formulas, args.family)
        models.extend(fitted)

    if not models:
        print("Error: no valid models provided. Use --models or --from-data with --formulas",
              file=sys.stderr)
        print("\nExample:")
        print('  python model-comparison.py --models "OLS AIC=1200 BIC=1220 k=5 LL=-590" \\')
        print('    "GLM AIC=1190 BIC=1215 k=6 LL=-588"')
        print('  python model-comparison.py --from-data data.csv --formulas "y~x1" "y~x1+x2" \\')
        print('    --formulas "y~I(x1^2)"')
        sys.exit(1)

    # Ensure all models have required fields
    found_n = args.n or max(m.get("n", 0) for m in models) if models else 0
    for m in models:
        if not m.get("n") and found_n:
            m["n"] = found_n

    # Compute derived metrics
    for m in models:
        if "aic" not in m and "ll" in m and "k" in m:
            m["aic"] = round(compute_aic(m["ll"], m["k"]), 2)
        if "bic" not in m and "ll" in m and "k" in m and m.get("n"):
            m["bic"] = round(compute_bic(m["ll"], m["k"], m["n"]), 2)
        if "aic" in m and m.get("k") and m.get("n"):
            m["aicc"] = round(compute_aicc(m["aic"], m["k"], m["n"]), 2)
            if m["aicc"] == float('inf'):
                m["aicc"] = None

    # Sort by AIC (lower is better)
    models.sort(key=lambda m: m.get("aic", float('inf')))

    # Compute Akaike weights and delta
    aic_vals = [m.get("aic", float('inf')) for m in models]
    if all(v != float('inf') for v in aic_vals):
        weights = compute_weights(aic_vals)
        for i, m in enumerate(models):
            m["delta_aic"] = round(aic_vals[i] - aic_vals[0], 2)
            m["akaike_weight"] = round(weights[i], 4)

    bic_vals = [m.get("bic", float('inf')) for m in models]
    if all(v != float('inf') for v in bic_vals):
        bic_weights = compute_weights(bic_vals)
        for i, m in enumerate(models):
            m["delta_bic"] = round(bic_vals[i] - bic_vals[0], 2)
            m["bic_weight"] = round(bic_weights[i], 4)

    result = {
        "n_models": len(models),
        "criterion": "AIC / BIC / AICc",
        "best_model": models[0]["name"] if models else None,
        "models": models,
    }

    # Ranking table
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print("Model Comparison")
        print("=" * 80)
        print(f"Best model: {result['best_model']}")
        print()
        header = f"{'Model':<25} {'AIC':>8} {'ΔAIC':>8} {'w(AIC)':>8} {'BIC':>8} {'ΔBIC':>8} {'k':>4} {'R²':>6}"
        if any(m.get("aicc") for m in models if m.get("aicc") is not None):
            header += f" {'AICc':>8}"
        print(header)
        print("-" * len(header))
        for m in models:
            row = f"{m['name']:<25} "
            row += f"{m.get('aic', '-'):>8.2f} " if isinstance(m.get('aic'), (int, float)) else f"{'NA':>8} "
            row += f"{m.get('delta_aic', '-'):>8.2f} " if isinstance(m.get('delta_aic'), (int, float)) else f"{'NA':>8} "
            row += f"{m.get('akaike_weight', '-'):>8.4f} " if isinstance(m.get('akaike_weight'), (int, float)) else f"{'NA':>8} "
            row += f"{m.get('bic', '-'):>8.2f} " if isinstance(m.get('bic'), (int, float)) else f"{'NA':>8} "
            row += f"{m.get('delta_bic', '-'):>8.2f} " if isinstance(m.get('delta_bic'), (int, float)) else f"{'NA':>8} "
            row += f"{m.get('k', '-'):>4} "
            row += f"{m.get('r_squared', '-'):>6.4f} " if isinstance(m.get('r_squared'), (int, float)) else f"{'NA':>6} "
            if any(mm.get("aicc") for mm in models if mm.get("aicc") is not None):
                aicc_val = m.get('aicc', '-')
                if aicc_val is not None and isinstance(aicc_val, (int, float)):
                    row += f"{aicc_val:>8.2f}"
                else:
                    row += f"{'NA':>8}"
            print(row)

        print()
        print("Interpretation:")
        print("  ΔAIC < 2: substantial support for model being best")
        print("  ΔAIC 4-7: considerably less support")
        print("  ΔAIC > 10: essentially no support")
        print("  w(AIC): probability that model is best (given set)")
        print()
        if args.from_data:
            loo_note = compute_loo_cv(models, args.from_data)
            print(f"Note: {loo_note['note']}")

        if args.engine == "r":
            print("\n--- R equivalent ---")
            print("# Compare models in R")
            print("library(AICcmodavg)")
            print("# Assuming model objects: m1, m2, m3")
            print("models <- list(m1=m1, m2=m2, m3=m3)")
            print("aictab(models)")
            print("print(bictab(models))")


def main():
    parser = argparse.ArgumentParser(description="Model Comparison Tool")
    parser.add_argument("--models", nargs="+", help='Model specs: "Name AIC=1200 BIC=1220 k=5 LL=-590"')
    parser.add_argument("--from-data", help="CSV file to fit models from")
    parser.add_argument("--formulas", nargs="+", help="R-style formulas for model fitting")
    parser.add_argument("--family", default="gaussian", choices=["gaussian", "binomial"],
                        help="Distribution family for model fitting")
    parser.add_argument("--n", type=int, help="Sample size (if not in model specs)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--engine", choices=["python", "r"], default="python",
                        help="Output language")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
