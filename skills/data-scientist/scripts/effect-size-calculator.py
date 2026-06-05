#!/usr/bin/env python3
"""
Effect Size Calculator

Computes effect sizes with confidence intervals for common designs.

Usage:
  python effect-size-calculator.py --design cohens-d --mean1 10 --mean2 8 --sd1 2.5 --sd2 2.8 --n1 30 --n2 30
  python effect-size-calculator.py --design cohens-d --t-stat 3.41 --df 58
  python effect-size-calculator.py --design eta-squared --ss-between 120 --ss-total 350
  python effect-size-calculator.py --design cramers-v --chi-sq 12.4 --n 200 --min-dim 2
  python effect-size-calculator.py --design odds-ratio --a 45 --b 55 --c 30 --d 70
  python effect-size-calculator.py --design correlation --r 0.45 --n 100
  python effect-size-calculator.py --design cohens-f2 --r-squared 0.34
  python effect-size-calculator.py --design r-squared --r 0.58
  python effect-size-calculator.py ... --json
  python effect-size-calculator.py ... --engine r
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


DESIGNS = {
    "cohens-d": "Cohen's d (independent groups)",
    "cohens-d-paired": "Cohen's d_z (paired groups)",
    "hedges-g": "Hedges' g (corrected Cohen's d for small samples)",
    "eta-squared": "Eta-squared (ANOVA)",
    "partial-eta-squared": "Partial eta-squared (factorial ANOVA)",
    "cohens-f": "Cohen's f (ANOVA effect size)",
    "cohens-f2": "Cohen's f² (regression effect size)",
    "r-squared": "R-squared from correlation",
    "cramers-v": "Cramér's V (chi-square associations)",
    "odds-ratio": "Odds ratio (2×2 tables)",
    "risk-ratio": "Risk ratio / Relative risk (2×2 tables)",
    "risk-difference": "Risk difference (2×2 tables)",
    "pearson-r": "Pearson correlation",
    "cohens-h": "Cohen's h (arcsine transformation for proportions)",
    "glass-delta": "Glass's Δ (experimental SD as reference)",
}


def _check_deps():
    if not HAS_NUMERIC:
        print("Error: scipy required. pip install scipy numpy", file=sys.stderr)
        sys.exit(1)


def cohens_d_from_means(m1, m2, sd1, sd2, n1=None, n2=None):
    """Cohen's d with pooled SD."""
    pooled_sd = math.sqrt(((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2)) if n1 and n2 else math.sqrt((sd1**2 + sd2**2) / 2)
    d = (m1 - m2) / pooled_sd
    return d, pooled_sd


def cohens_d_from_t(t, df, n1, n2):
    """Cohen's d from t-statistic."""
    d = t * math.sqrt((n1 + n2) / (n1 * n2))
    return d


def hedges_g(d, n1, n2):
    """Convert Cohen's d to Hedges' g (small sample correction)."""
    df = n1 + n2 - 2
    correction = 1 - (3 / (4 * df - 1))
    return d * correction


def ci_cohens_d(d, n1, n2, alpha=0.05):
    """Confidence interval for Cohen's d using non-central t."""
    _check_deps()
    t_val = d * math.sqrt((n1 * n2) / (n1 + n2))
    df = n1 + n2 - 2
    try:
        # Non-central t confidence interval
        ncp_lower = sp_stats.nct.ppf(alpha / 2, df, t_val)
        ncp_upper = sp_stats.nct.ppf(1 - alpha / 2, df, t_val)
        d_lower = ncp_lower * math.sqrt((n1 + n2) / (n1 * n2))
        d_upper = ncp_upper * math.sqrt((n1 + n2) / (n1 * n2))
        return round(d_lower, 4), round(d_upper, 4)
    except Exception:
        # Fallback: delta method approximation
        se_d = math.sqrt((n1 + n2) / (n1 * n2) + d**2 / (2 * (n1 + n2)))
        z = sp_stats.norm.ppf(1 - alpha / 2)
        return round(d - z * se_d, 4), round(d + z * se_d, 4)


def eta_squared(ss_between, ss_total):
    """η² = SS_between / SS_total"""
    return ss_between / ss_total


def cohens_f_from_eta2(eta2):
    """f = sqrt(η² / (1 - η²))"""
    return math.sqrt(eta2 / (1 - eta2))


def cohens_f2_from_r2(r2):
    """f² = R² / (1 - R²)"""
    return r2 / (1 - r2)


def cramers_v(chi2, n, min_dim):
    """V = sqrt(χ² / (n * min(r-1, c-1)))"""
    return math.sqrt(chi2 / (n * min_dim))


def odds_ratio(a, b, c, d):
    """OR = (a/c) / (b/d) = ad / bc"""
    return (a * d) / (b * c)


def risk_ratio(a, b, c, d):
    """RR = (a/(a+b)) / (c/(c+d))"""
    p1 = a / (a + b) if (a + b) > 0 else 0
    p2 = c / (c + d) if (c + d) > 0 else 0
    return p1 / p2 if p2 > 0 else float('inf')


def risk_difference(a, b, c, d):
    """RD = a/(a+b) - c/(c+d)"""
    p1 = a / (a + b) if (a + b) > 0 else 0
    p2 = c / (c + d) if (c + d) > 0 else 0
    return p1 - p2


def ci_odds_ratio(a, b, c, d, alpha=0.05):
    """Woolf's CI for odds ratio."""
    _check_deps()
    or_val = odds_ratio(a, b, c, d)
    se_log_or = math.sqrt(1/a + 1/b + 1/c + 1/d)
    z = sp_stats.norm.ppf(1 - alpha / 2)
    lo = math.exp(math.log(or_val) - z * se_log_or)
    hi = math.exp(math.log(or_val) + z * se_log_or)
    return round(lo, 4), round(hi, 4)


def ci_pearson_r(r, n, alpha=0.05):
    """Fisher z-transformation CI for Pearson r."""
    _check_deps()
    z_r = 0.5 * math.log((1 + r) / (1 - r))
    se_z = 1 / math.sqrt(n - 3)
    z = sp_stats.norm.ppf(1 - alpha / 2)
    lo = math.tanh(z_r - z * se_z)
    hi = math.tanh(z_r + z * se_z)
    return round(lo, 4), round(hi, 4)


def cohens_h(p1, p2):
    """h = 2 * arcsin(sqrt(p1)) - 2 * arcsin(sqrt(p2))"""
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def r_squared_from_r(r):
    """R² = r²"""
    return r ** 2


def interpret_cohens_d(d):
    if abs(d) < 0.2:
        return "negligible"
    elif abs(d) < 0.5:
        return "small"
    elif abs(d) < 0.8:
        return "medium"
    else:
        return "large"


def run(args):
    result = {}

    if args.design == "cohens-d":
        if args.mean1 is not None and args.mean2 is not None and args.sd1 is not None and args.sd2 is not None and args.n1 and args.n2:
            d, pooled = cohens_d_from_means(args.mean1, args.mean2, args.sd1, args.sd2, args.n1, args.n2)
            ci = ci_cohens_d(d, args.n1, args.n2)
            result = {
                "effect_size": "Cohen's d",
                "d": round(d, 4),
                "pooled_sd": round(pooled, 4),
                "interpretation": interpret_cohens_d(d),
                "ci_95": ci,
                "parameters": {"mean1": args.mean1, "mean2": args.mean2, "n1": args.n1, "n2": args.n2}
            }
        elif args.t_stat is not None and args.df is not None:
            # Need n1 and n2 to compute d from t
            result = {"error": "t-statistic requires also --n1 and --n2 for Cohen's d"}
        else:
            result = {"error": "Provide --mean1 --mean2 --sd1 --sd2 --n1 --n2"}

    elif args.design == "hedges-g":
        if args.mean1 is not None and args.mean2 is not None and args.sd1 is not None and args.sd2 is not None and args.n1 and args.n2:
            d, pooled = cohens_d_from_means(args.mean1, args.mean2, args.sd1, args.sd2, args.n1, args.n2)
            g = hedges_g(d, args.n1, args.n2)
            result = {
                "effect_size": "Hedges' g",
                "g": round(g, 4),
                "cohens_d": round(d, 4),
                "interpretation": interpret_cohens_d(d),
                "parameters": {"mean1": args.mean1, "mean2": args.mean2, "n1": args.n1, "n2": args.n2}
            }
        else:
            result = {"error": "Provide --mean1 --mean2 --sd1 --sd2 --n1 --n2"}

    elif args.design == "eta-squared":
        if args.ss_between is not None and args.ss_total is not None:
            eta2 = eta_squared(args.ss_between, args.ss_total)
            f = cohens_f_from_eta2(eta2)
            result = {
                "effect_size": "Eta-squared",
                "eta_squared": round(eta2, 4),
                "cohens_f": round(f, 4),
                "interpretation": "small" if eta2 < 0.01 else ("medium" if eta2 < 0.06 else ("large" if eta2 < 0.14 else "very large")),
            }
        else:
            result = {"error": "Provide --ss-between and --ss-total"}

    elif args.design == "cohens-f2":
        if args.r_squared is not None:
            f2 = cohens_f2_from_r2(args.r_squared)
            result = {
                "effect_size": "Cohen's f²",
                "f_squared": round(f2, 4),
                "r_squared": args.r_squared,
                "interpretation": "small" if f2 < 0.02 else ("medium" if f2 < 0.15 else "large"),
            }
        else:
            result = {"error": "Provide --r-squared"}

    elif args.design == "cramers-v":
        if args.chi_sq is not None and args.n is not None and args.min_dim is not None:
            v = cramers_v(args.chi_sq, args.n, args.min_dim)
            result = {
                "effect_size": "Cramér's V",
                "V": round(v, 4),
                "parameters": {"chi_sq": args.chi_sq, "n": args.n, "min_dim": args.min_dim},
                "interpretation": "small" if v < 0.1 else ("medium" if v < 0.3 else "large"),
            }
        else:
            result = {"error": "Provide --chi-sq --n --min-dim"}

    elif args.design == "odds-ratio":
        if args.a is not None and args.b is not None and args.c is not None and args.d is not None:
            or_val = odds_ratio(args.a, args.b, args.c, args.d)
            ci = ci_odds_ratio(args.a, args.b, args.c, args.d)
            rr = risk_ratio(args.a, args.b, args.c, args.d)
            rd = risk_difference(args.a, args.b, args.c, args.d)
            result = {
                "effect_size": "Odds ratio",
                "OR": round(or_val, 4),
                "ci_95": ci,
                "RR": round(rr, 4),
                "risk_difference": round(rd, 4),
                "log_OR": round(math.log(or_val), 4),
                "interpretation": "OR = 1 (no effect)" if 0.95 <= or_val <= 1.05 else
                                 f"OR > 1 (increased odds)" if or_val > 1 else "OR < 1 (decreased odds)",
            }
        else:
            result = {"error": "Provide --a --b --c --d (2×2 table counts)"}

    elif args.design == "risk-ratio":
        if args.a is not None and args.b is not None and args.c is not None and args.d is not None:
            rr = risk_ratio(args.a, args.b, args.c, args.d)
            result = {
                "effect_size": "Risk ratio",
                "RR": round(rr, 4),
                "interpretation": "RR = 1 (no effect)" if 0.95 <= rr <= 1.05 else ("RR > 1 (increased risk)" if rr > 1 else "RR < 1 (decreased risk)"),
            }
        else:
            result = {"error": "Provide --a --b --c --d"}

    elif args.design == "risk-difference":
        if args.a is not None and args.b is not None and args.c is not None and args.d is not None:
            rd = risk_difference(args.a, args.b, args.c, args.d)
            result = {
                "effect_size": "Risk difference",
                "RD": round(rd, 4),
                "interpretation": f"Absolute difference of {abs(rd):.1%} in risk",
            }
        else:
            result = {"error": "Provide --a --b --c --d"}

    elif args.design in ("pearson-r", "correlation"):
        if args.r is not None and args.n is not None:
            ci = ci_pearson_r(args.r, args.n)
            result = {
                "effect_size": "Pearson r",
                "r": args.r,
                "r_squared": round(args.r ** 2, 4),
                "ci_95": ci,
                "n": args.n,
                "interpretation": "small" if abs(args.r) < 0.1 else ("medium" if abs(args.r) < 0.3 else "large"),
            }
        else:
            result = {"error": "Provide --r and --n"}

    elif args.design == "r-squared":
        if args.r is not None:
            r2 = r_squared_from_r(args.r)
            result = {
                "effect_size": "R-squared",
                "r_squared": round(r2, 4),
                "r": args.r,
            }
        else:
            result = {"error": "Provide --r"}

    elif args.design == "cohens-h":
        if args.p1 is not None and args.p2 is not None:
            h = cohens_h(args.p1, args.p2)
            result = {
                "effect_size": "Cohen's h",
                "h": round(h, 4),
                "parameters": {"p1": args.p1, "p2": args.p2},
                "interpretation": "small" if abs(h) < 0.2 else ("medium" if abs(h) < 0.5 else "large"),
            }
        else:
            result = {"error": "Provide --p1 and --p2"}

    else:
        result = {"error": f"Unknown design '{args.design}'"}

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"## {result.get('effect_size', 'Effect Size')}")
        print(f"Value: {result.get(list(result.keys())[1], '?')}")
        if "ci_95" in result:
            print(f"95% CI: ({result['ci_95'][0]:.4f}, {result['ci_95'][1]:.4f})")
        if "interpretation" in result:
            print(f"Interpretation: {result['interpretation']}")
        if "r_squared" in result:
            print(f"R²: {result['r_squared']}")
        print()
        # Report template
        print("Reporting template:")
        if result.get("effect_size") == "Cohen's d":
            print(f"  d = {result['d']:.2f}, 95% CI [{result['ci_95'][0]:.2f}, {result['ci_95'][1]:.2f}]")
        elif result.get("effect_size") == "Odds ratio":
            print(f"  OR = {result['OR']:.2f}, 95% CI [{result['ci_95'][0]:.2f}, {result['ci_95'][1]:.2f}]")
        elif result.get("effect_size") == "Cramér's V":
            print(f"  V = {result['V']:.2f}")

        if args.engine == "r":
            print("\n--- R equivalent ---")
            print("library(effectsize)")
            if result.get("effect_size") == "Cohen's d":
                print(f"cohens_d({args.mean1}, {args.mean2}, pooled_sd = TRUE)" if args.mean1 else "# Provide data vectors")
            elif result.get("effect_size") == "Pearson r":
                print(f"library(psych); r.con(r = {args.r}, n = {args.n}, p = 0.95)")
            elif result.get("effect_size") == "Cramér's V":
                print(f"cramers_v(chi2 = {args.chi_sq}, n = {args.n}, nrow = {args.min_dim + 1})")


def main():
    parser = argparse.ArgumentParser(description="Effect Size Calculator")
    parser.add_argument("--design", choices=list(DESIGNS.keys()), required=True,
                        help="Effect size type")
    # Means/SDs
    parser.add_argument("--mean1", type=float)
    parser.add_argument("--mean2", type=float)
    parser.add_argument("--sd1", type=float)
    parser.add_argument("--sd2", type=float)
    parser.add_argument("--n1", type=int)
    parser.add_argument("--n2", type=int)
    parser.add_argument("--t-stat", type=float)
    parser.add_argument("--df", type=int)
    # ANOVA
    parser.add_argument("--ss-between", type=float)
    parser.add_argument("--ss-total", type=float)
    # Regression
    parser.add_argument("--r-squared", type=float)
    parser.add_argument("--r", type=float)
    # Categorical
    parser.add_argument("--chi-sq", type=float)
    parser.add_argument("--n", type=int)
    parser.add_argument("--min-dim", type=int, help="Cramér's V: min(rows-1, cols-1). For a 2×2 table pass 1; for 3×4 table pass 2 (min(2,3)=2)")
    parser.add_argument("--a", type=float)
    parser.add_argument("--b", type=float)
    parser.add_argument("--c", type=float)
    parser.add_argument("--d", type=float)
    # Proportions
    parser.add_argument("--p1", type=float)
    parser.add_argument("--p2", type=float)
    # General
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--engine", choices=["python", "r"], default="python",
                        help="Output language")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
