#!/usr/bin/env python3
"""
Power Analysis Calculator

Computes sample size from effect size (and vice versa) for common designs.
Supports Python default with --engine r for R output.

Usage:
  python power-analysis.py --design ttest-ind --effect-size 0.5 --alpha 0.05 --power 0.80
  python power-analysis.py --design ttest-paired --n-per-group 30 --alpha 0.05 --power 0.80
  python power-analysis.py --design anova --k 3 --effect-size 0.25 --alpha 0.05 --power 0.80
  python power-analysis.py --design prop --p1 0.10 --p2 0.15 --alpha 0.05 --power 0.80
  python power-analysis.py --design correlation --effect-size 0.3 --alpha 0.05 --power 0.80
  python power-analysis.py --design regression --predictors 5 --effect-size 0.15 --alpha 0.05 --power 0.80
  python power-analysis.py --design chi-square --df 2 --effect-size 0.3 --alpha 0.05 --power 0.80
  python power-analysis.py --design equivalence --effect-size 0.5 --alpha 0.05 --power 0.80
  python power-analysis.py --list-designs
  python power-analysis.py ... --json
  python power-analysis.py ... --engine r
"""

import argparse
import math
import json
import sys

try:
    import numpy as np
    from scipy import stats as sp_stats
    HAS_NUMERIC = True
except ImportError:
    HAS_NUMERIC = False


def _check_deps():
    if not HAS_NUMERIC:
        print("Error: scipy and numpy are required. Install with: pip install scipy numpy",
              file=sys.stderr)
        sys.exit(1)


DESIGNS = {
    "ttest-ind": "Two-sample independent t-test (equal n per group)",
    "ttest-ind-unequal": "Two-sample independent t-test (unequal n, specify ratio)",
    "ttest-paired": "Paired t-test",
    "onesample": "One-sample t-test",
    "prop": "Two-proportion z-test",
    "onesample-prop": "One-sample proportion test",
    "anova": "One-way ANOVA (k groups, equal n per group)",
    "anova-interaction": "ANOVA interaction effect (2×2 factorial)",
    "correlation": "Pearson correlation test",
    "regression": "Multiple linear regression (F-test for R²)",
    "logistic": "Logistic regression (Wald test for single coefficient)",
    "chi-square": "Chi-square test of independence (contingency table)",
    "equivalence": "Two one-sided tests (TOST) for equivalence",
    "survival": "Survival analysis (log-rank test)",
}


def solve_power_ttest_ind(d, alpha=0.05, power=0.80, ratio=1.0, alternative="two-sided"):
    """Compute per-group sample size for independent t-test. Returns n_per_group."""
    _check_deps()
    if alternative == "two-sided":
        alpha /= 2
    z_beta = sp_stats.norm.ppf(power)
    z_alpha = sp_stats.norm.ppf(1 - alpha)
    n_per_group = ((z_alpha + z_beta) ** 2 * (1 + 1/ratio) / (d ** 2)) + 2
    return int(math.ceil(n_per_group))


def solve_power_ttest_paired(d, alpha=0.05, power=0.80):
    """Compute number of pairs for paired t-test."""
    _check_deps()
    z_beta = sp_stats.norm.ppf(power)
    z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
    n = ((z_alpha + z_beta) ** 2 / (d ** 2)) + 2
    return int(math.ceil(n))


def solve_power_onesample(d, alpha=0.05, power=0.80):
    """Compute sample size for one-sample t-test."""
    return solve_power_ttest_paired(d, alpha, power)


def solve_power_prop(p1, p2, alpha=0.05, power=0.80, ratio=1.0):
    """Compute per-group sample size for two-proportion z-test."""
    _check_deps()
    p_bar = (p1 + ratio * p2) / (1 + ratio)
    z_beta = sp_stats.norm.ppf(power)
    z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
    n = ((z_alpha + z_beta) ** 2 *
         (p1 * (1 - p1) / 1 + p2 * (1 - p2) / ratio)) / ((p1 - p2) ** 2)
    return int(math.ceil(n))


def solve_power_anova(f, k, alpha=0.05, power=0.80):
    """Compute per-group sample size for one-way ANOVA using non-central F distribution.

    More accurate than the normal approximation. Uses iterative search.
    f = Cohen's f = sqrt(η² / (1 - η²))
    Non-centrality parameter λ = n * k * f²
    df1 = k - 1,  df2 = k * (n - 1)
    """
    _check_deps()
    f2 = f ** 2

    def _power_at_n(n):
        df1 = k - 1
        df2 = k * (n - 1)
        if df2 < 1:
            return 0.0
        f_crit = sp_stats.f.ppf(1 - alpha, df1, df2)
        lam = n * k * f2
        return 1.0 - sp_stats.ncf.cdf(f_crit, df1, df2, lam)

    # Binary search for minimum n that achieves desired power
    lo, hi = 2, 10000
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _power_at_n(mid) >= power:
            hi = mid
        else:
            lo = mid
    return hi


def solve_power_correlation(r, alpha=0.05, power=0.80):
    """Compute sample size for Pearson correlation test."""
    _check_deps()
    z_beta = sp_stats.norm.ppf(power)
    z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
    z_r = 0.5 * math.log((1 + r) / (1 - r))
    n = ((z_alpha + z_beta) / z_r) ** 2 + 3
    return int(math.ceil(n))


def solve_power_regression(f2, p, alpha=0.05, power=0.80):
    """Compute total sample size for multiple regression. f2 = Cohen's f² = R²/(1-R²)."""
    _check_deps()
    z_beta = sp_stats.norm.ppf(power)
    z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
    n = ((z_alpha + z_beta) ** 2 / f2) + p + 1
    return int(math.ceil(n))


def solve_power_chisquare(w, df, alpha=0.05, power=0.80):
    """Compute total sample size for chi-square test. w = Cohen's w = Cramér's V × sqrt(min(r,c)-1)."""
    _check_deps()
    # Non-central chi-square approximation
    z_beta = sp_stats.norm.ppf(power)
    z_alpha = sp_stats.norm.ppf(1 - alpha)
    ncp = (z_alpha + z_beta) ** 2
    n = ncp / (w ** 2)
    return int(math.ceil(n))


def solve_power_equivalence(d, alpha=0.05, power=0.80):
    """TOST equivalence test sample size. d is equivalence bound in Cohen's d units."""
    _check_deps()
    # Two one-sided tests: approximate
    z_beta = sp_stats.norm.ppf(power)
    z_alpha = sp_stats.norm.ppf(1 - alpha)
    n = ((z_alpha + z_beta) ** 2) / (2 * (d ** 2))
    return int(math.ceil(n))


def solve_power_logistic(or_val, p_base, alpha=0.05, power=0.80):
    """Approximate per-group sample for logistic regression."""
    _check_deps()
    p1 = p_base * or_val / (1 - p_base + p_base * or_val)
    d = p1 - p_base
    p_bar = (p1 + p_base) / 2
    n = ((sp_stats.norm.ppf(1 - alpha/2) + sp_stats.norm.ppf(power)) ** 2 *
         (2 * p_bar * (1 - p_bar))) / (d ** 2)
    return int(math.ceil(n))


def run(args):
    if args.list_designs:
        print("Available designs:\n")
        for key, desc in DESIGNS.items():
            print(f"  {key:25s} {desc}")
        return

    if not args.design:
        print("Error: --design is required (use --list-designs to see options)", file=sys.stderr)
        sys.exit(1)

    design = args.design
    alpha = args.alpha
    power = args.power

    result = {"design": design, "alpha": alpha, "power": power, "parameters": {}}

    if design == "ttest-ind":
        if args.effect_size is not None:
            n = solve_power_ttest_ind(args.effect_size, alpha, power, args.ratio)
            result["type"] = "sample_size"
            result["n_per_group"] = n
            result["n_total"] = n * 2
            result["parameters"]["effect_size_d"] = args.effect_size
            result["note"] = f"Need {n} per group ({n * 2} total) for d = {args.effect_size}"
        elif args.n_per_group is not None:
            # Compute detectable effect size
            _check_deps()
            z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
            z_beta = sp_stats.norm.ppf(power)
            d = (z_alpha + z_beta) / math.sqrt(args.n_per_group / 2)
            result["type"] = "detectable_effect"
            result["effect_size_d"] = round(d, 4)
            result["parameters"]["n_per_group"] = args.n_per_group
            result["note"] = f"With {args.n_per_group} per group, can detect d = {d:.4f}"
        else:
            print("Error: provide --effect-size or --n-per-group for ttest-ind", file=sys.stderr)
            sys.exit(1)

    elif design == "ttest-paired":
        if args.effect_size is not None:
            n = solve_power_ttest_paired(args.effect_size, alpha, power)
            result["type"] = "sample_size"
            result["n_pairs"] = n
            result["parameters"]["effect_size_dz"] = args.effect_size
            result["note"] = f"Need {n} pairs for d_z = {args.effect_size}"
        elif args.n_per_group is not None:
            _check_deps()
            z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
            z_beta = sp_stats.norm.ppf(power)
            d = (z_alpha + z_beta) / math.sqrt(args.n_per_group - 2)
            result["type"] = "detectable_effect"
            result["effect_size_dz"] = round(d, 4)
            result["parameters"]["n_pairs"] = args.n_per_group
            result["note"] = f"With {args.n_per_group} pairs, can detect d_z = {d:.4f}"
        else:
            print("Error: provide --effect-size or --n-per-group for ttest-paired", file=sys.stderr)
            sys.exit(1)

    elif design == "prop":
        if args.p1 is not None and args.p2 is not None:
            n = solve_power_prop(args.p1, args.p2, alpha, power, args.ratio)
            mde = args.p2 - args.p1
            result["type"] = "sample_size"
            result["n_per_group"] = n
            result["n_total"] = n * 2
            result["parameters"]["p1"] = args.p1
            result["parameters"]["p2"] = args.p2
            result["note"] = f"Need {n} per group ({n * 2} total) to detect {mde:.1%} difference (base={args.p1:.1%})"
        else:
            print("Error: provide --p1 and --p2 for proportion test", file=sys.stderr)
            sys.exit(1)

    elif design == "anova":
        if args.k is None:
            print("Error: --k required for ANOVA", file=sys.stderr)
            sys.exit(1)
        if args.effect_size is not None:
            n = solve_power_anova(args.effect_size, args.k, alpha, power)
            eta2 = args.effect_size ** 2 / (1 + args.effect_size ** 2)
            result["type"] = "sample_size"
            result["n_per_group"] = n
            result["n_total"] = n * args.k
            result["parameters"]["k"] = args.k
            result["parameters"]["cohens_f"] = args.effect_size
            result["parameters"]["eta_squared"] = round(eta2, 4)
            result["note"] = f"Need {n} per group ({n * args.k} total) for f = {args.effect_size} (η² = {eta2:.4f})"
        elif args.n_per_group is not None:
            _check_deps()
            z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
            z_beta = sp_stats.norm.ppf(power)
            f = (z_alpha + z_beta) / math.sqrt(args.n_per_group * args.k - 1)
            result["type"] = "detectable_effect"
            result["cohens_f"] = round(f, 4)
            result["parameters"]["k"] = args.k
            result["parameters"]["n_per_group"] = args.n_per_group
            result["note"] = f"With {args.n_per_group} per group ({args.k} groups), can detect f = {f:.4f}"
        else:
            print("Error: provide --effect-size or --n-per-group for ANOVA", file=sys.stderr)
            sys.exit(1)

    elif design == "correlation":
        if args.effect_size is not None:
            n = solve_power_correlation(args.effect_size, alpha, power)
            result["type"] = "sample_size"
            result["n_total"] = n
            result["parameters"]["r"] = args.effect_size
            result["note"] = f"Need N = {n} to detect r = {args.effect_size}"
        elif args.n_per_group is not None:
            _check_deps()
            z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
            z_beta = sp_stats.norm.ppf(power)
            z_r_thresh = z_alpha + z_beta / math.sqrt(args.n_per_group - 3)
            r = math.tanh(z_r_thresh)
            result["type"] = "detectable_effect"
            result["r"] = round(r, 4)
            result["parameters"]["n"] = args.n_per_group
            result["note"] = f"With N = {args.n_per_group}, can detect r = {r:.4f}"
        else:
            print("Error: provide --effect-size or --n-per-group for correlation", file=sys.stderr)
            sys.exit(1)

    elif design == "regression":
        if args.predictors is None:
            print("Error: --predictors required for regression", file=sys.stderr)
            sys.exit(1)
        if args.effect_size is not None:
            f2 = args.effect_size  # Cohen's f²
            n = solve_power_regression(f2, args.predictors, alpha, power)
            r2 = f2 / (1 + f2)
            result["type"] = "sample_size"
            result["n_total"] = n
            result["parameters"]["predictors"] = args.predictors
            result["parameters"]["cohens_f2"] = f2
            result["parameters"]["r_squared"] = round(r2, 4)
            result["note"] = f"Need N = {n} for {args.predictors} predictors, f² = {f2} (R² = {r2:.4f})"
        elif args.n_per_group is not None:
            _check_deps()
            z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
            z_beta = sp_stats.norm.ppf(power)
            f2 = ((z_alpha + z_beta) ** 2) / (args.n_per_group - args.predictors - 1)
            result["type"] = "detectable_effect"
            result["cohens_f2"] = round(f2, 4)
            result["parameters"]["predictors"] = args.predictors
            result["parameters"]["n"] = args.n_per_group
            result["note"] = f"With N = {args.n_per_group}, {args.predictors} predictors, can detect f² = {f2:.4f}"
        else:
            print("Error: provide --effect-size or --n-per-group for regression", file=sys.stderr)
            sys.exit(1)

    elif design == "chi-square":
        if args.df is None:
            print("Error: --df required for chi-square", file=sys.stderr)
            sys.exit(1)
        if args.effect_size is not None:
            n = solve_power_chisquare(args.effect_size, args.df, alpha, power)
            result["type"] = "sample_size"
            result["n_total"] = n
            result["parameters"]["df"] = args.df
            result["parameters"]["w"] = args.effect_size
            result["note"] = f"Need N = {n} for χ² test, df = {args.df}, w = {args.effect_size}"
        elif args.n_per_group is not None:
            _check_deps()
            z_alpha = sp_stats.norm.ppf(1 - alpha)
            z_beta = sp_stats.norm.ppf(power)
            w = (z_alpha + z_beta) / math.sqrt(args.n_per_group)
            result["type"] = "detectable_effect"
            result["w"] = round(w, 4)
            result["parameters"]["n"] = args.n_per_group
            result["parameters"]["df"] = args.df
            result["note"] = f"With N = {args.n_per_group}, df = {args.df}, can detect w = {w:.4f}"
        else:
            print("Error: provide --effect-size or --n-per-group for chi-square", file=sys.stderr)
            sys.exit(1)

    elif design == "equivalence":
        if args.effect_size is not None:
            n = solve_power_equivalence(args.effect_size, alpha, power)
            result["type"] = "sample_size"
            result["n_total"] = n if args.design == "onesample" else n
            result["n_per_group"] = n
            result["parameters"]["equivalence_bound_d"] = args.effect_size
            result["note"] = f"Need N = {n} per group for equivalence TOST, bound d = {args.effect_size}"
        else:
            print("Error: provide --effect-size for equivalence test", file=sys.stderr)
            sys.exit(1)

    elif design == "logistic":
        if args.or_val is not None and args.p_base is not None:
            n = solve_power_logistic(args.or_val, args.p_base, alpha, power)
            p1 = args.p_base * args.or_val / (1 - args.p_base + args.p_base * args.or_val)
            result["type"] = "sample_size"
            result["n_per_group"] = n
            result["n_total"] = n * 2
            result["parameters"]["or"] = args.or_val
            result["parameters"]["p_base"] = args.p_base
            result["parameters"]["p_treated"] = round(p1, 4)
            result["note"] = f"Need N = {n} per group to detect OR = {args.or_val} from base {args.p_base}"
        else:
            print("Error: provide --or-val and --p-base for logistic power", file=sys.stderr)
            sys.exit(1)

    else:
        print(f"Error: unknown design '{design}'. Use --list-designs.", file=sys.stderr)
        sys.exit(1)

    if args.engine == "r":
        print(_to_r_code(design, result))
    elif args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result.get("note", ""))
        for k, v in result.items():
            if k not in ("note", "type", "parameters"):
                if isinstance(v, float):
                    print(f"  {k}: {v:.4f}")
                else:
                    print(f"  {k}: {v}")


def _to_r_code(design, result):
    lines = ["# R power analysis code", "# Run in R with: install.packages('pwr')", ""]
    lines.append("library(pwr)")
    lines.append("")
    if result.get("type") == "sample_size":
        n = result.get("n_per_group") or result.get("n_total")
        if design == "ttest-ind":
            lines.append(f"# Two-sample t-test: n = {n} per group")
            d = result.get("parameters", {}).get("effect_size_d", "?")
            lines.append(f'pwr.t.test(d = {d}, power = {result.get("power", 0.8)}, '
                         f'sig.level = {result.get("alpha", 0.05)}, type = "two.sample")')
        elif design == "ttest-paired":
            lines.append(f'pwr.t.test(d = {result.get("parameters", {}).get("effect_size_dz", "?")}, '
                         f'power = {result.get("power", 0.8)}, sig.level = {result.get("alpha", 0.05)}, '
                         f'type = "paired")')
        elif design == "prop":
            h = 2 * math.asin(math.sqrt(result.get("parameters", {}).get("p2", 0.15))) - \
                2 * math.asin(math.sqrt(result.get("parameters", {}).get("p1", 0.10)))
            lines.append(f'h = ES.h({result.get("parameters", {}).get("p1", 0.1)}, '
                         f'{result.get("parameters", {}).get("p2", 0.15)})')
            lines.append(f'pwr.2p.test(h = {h:.4f}, n = {n}, '
                         f'sig.level = {result.get("alpha", 0.05)}, power = {result.get("power", 0.8)})')
        elif design == "correlation":
            lines.append(f'pwr.r.test(r = {result.get("parameters", {}).get("r", "?")}, '
                         f'power = {result.get("power", 0.8)}, sig.level = {result.get("alpha", 0.05)})')
        elif design == "anova":
            lines.append(f'pwr.anova.test(k = {result.get("parameters", {}).get("k", "?")}, '
                         f'f = {result.get("parameters", {}).get("cohens_f", "?")}, '
                         f'power = {result.get("power", 0.8)}, sig.level = {result.get("alpha", 0.05)})')
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Power Analysis Calculator")
    parser.add_argument("--design", choices=list(DESIGNS.keys()), help="Study design")
    parser.add_argument("--list-designs", action="store_true", help="List available designs")
    parser.add_argument("--effect-size", type=float, help="Standardized effect size")
    parser.add_argument("--n-per-group", type=int, help="Sample size per group (for computing detectable effect)")
    parser.add_argument("--alpha", type=float, default=0.05, help="Type I error rate")
    parser.add_argument("--power", type=float, default=0.80, help="Desired statistical power")
    parser.add_argument("--ratio", type=float, default=1.0, help="Control:treated ratio")
    parser.add_argument("--k", type=int, help="Number of groups (ANOVA)")
    parser.add_argument("--df", type=int, help="Degrees of freedom (chi-square)")
    parser.add_argument("--predictors", type=int, help="Number of predictors (regression)")
    parser.add_argument("--p1", type=float, help="Proportion in group 1 (proportion test)")
    parser.add_argument("--p2", type=float, help="Proportion in group 2 (proportion test)")
    parser.add_argument("--or-val", type=float, help="Odds ratio to detect (logistic)")
    parser.add_argument("--p-base", type=float, help="Baseline proportion (logistic)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--engine", choices=["python", "r"], default="python",
                        help="Output language (python = compute now, r = generate R code)")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
