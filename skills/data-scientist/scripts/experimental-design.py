#!/usr/bin/env python3
"""
Experimental Design Generator

Generates experimental designs (randomization schedules) for common designs.
Supports Python default with --engine r for R output.

Usage:
  python experimental-design.py --design crd --treatments A B C --n-per-group 10
  python experimental-design.py --design rcbd --treatments Control Treatment --blocks 6 --n-per-block 1
  python experimental-design.py --design latin-square --treatments A B C D
  python experimental-design.py --design factorial --factors "temp:2:low,high" "pressure:2:100,200" --reps 3
  python experimental-design.py --design crossover --treatments A B C --sequences 3 --subjects 6
  python experimental-design.py --list-designs
  python experimental-design.py ... --json
  python experimental-design.py ... --output schedule.csv
  python experimental-design.py ... --engine r
"""

import argparse
import csv
import itertools
import json
import math
import random
import sys

try:
    import numpy as np
    HAS_NP = True
except ImportError:
    HAS_NP = False


DESIGNS = {
    "crd": "Completely Randomized Design",
    "rcbd": "Randomized Complete Block Design",
    "latin-square": "Latin Square Design",
    "factorial": "Factorial Design (full)",
    "crossover": "Crossover Design (2×2)",
    "split-plot": "Split-Plot Design",
}


def generate_crd(treatments, n_per_group):
    """Generate completely randomized design."""
    units = []
    for t in treatments:
        for i in range(n_per_group):
            units.append({"treatment": t, "unit_id": f"{t}_{i+1}"})
    random.shuffle(units)
    for i, u in enumerate(units, 1):
        u["run_order"] = i
    return units


def generate_rcbd(treatments, blocks, n_per_block=1):
    """Generate randomized complete block design."""
    units = []
    for b in range(1, blocks + 1):
        block_units = []
        for t in treatments:
            for r in range(n_per_block):
                block_units.append({"treatment": t, "block": b, "unit_id": f"B{b}_{t}_{r+1}"})
        random.shuffle(block_units)
        for j, u in enumerate(block_units, 1):
            u["run_within_block"] = j
        units.extend(block_units)
    return units


def generate_latin_square(treatments):
    """Generate Latin square design. Uses cyclic method for odd n, then randomize."""
    n = len(treatments)
    if n < 2:
        raise ValueError("Need at least 2 treatments")

    # Generate cyclic Latin square
    square = []
    for i in range(n):
        row = [treatments[(i + j) % n] for j in range(n)]
        square.append(row)

    # Randomize rows and columns
    random.shuffle(square)
    col_order = list(range(n))
    random.shuffle(col_order)

    units = []
    for i in range(n):
        for j in range(n):
            units.append({
                "row": i + 1,
                "column": j + 1,
                "treatment": square[i][col_order[j]],
                "unit_id": f"R{i+1}C{j+1}"
            })
    return units


def generate_factorial(factors, reps):
    """Generate full factorial design.
    factors: list of dicts with name, levels, level_labels
    """
    # Build factor levels
    factor_names = []
    factor_levels = []
    level_labels_list = []
    for f in factors:
        factor_names.append(f["name"])
        n_levels = int(f["levels"])
        labels = f.get("labels", "").split(",")
        # If explicit labels provided, use them; otherwise use coded levels
        if len(labels) == n_levels and labels[0]:
            level_labels_list.append(labels)
        else:
            level_labels_list.append([str(i+1) for i in range(n_levels)])
        factor_levels.append(list(range(n_levels)))

    # All combinations
    combos = list(itertools.product(*factor_levels))
    units = []
    rep_count = 1
    for rep in range(1, reps + 1):
        for combo in combos:
            entry = {"rep": rep}
            for i, name in enumerate(factor_names):
                entry[name] = level_labels_list[i][combo[i]]
            entry["unit_id"] = f"R{rep}_" + "_".join(str(level_labels_list[i][combo[i]]) for i in range(len(combo)))
            units.append(entry)

    random.shuffle(units)
    for i, u in enumerate(units, 1):
        u["run_order"] = i
    return units


def generate_crossover_2x2(treatments, subjects_per_seq):
    """Generate 2×2 crossover design."""
    if len(treatments) < 2:
        raise ValueError("Need at least 2 treatments for crossover")

    t = treatments[:2]
    sequences = [
        [t[0], t[1]],  # Sequence 1: A → B
        [t[1], t[0]],  # Sequence 2: B → A
    ]

    units = []
    subj_id = 1
    for seq_idx, seq in enumerate(sequences):
        for s in range(subjects_per_seq):
            for period, treatment in enumerate(seq, 1):
                units.append({
                    "subject": subj_id,
                    "sequence": seq_idx + 1,
                    "period": period,
                    "treatment": treatment,
                    "unit_id": f"S{subj_id}_P{period}"
                })
            subj_id += 1
    return units


def output_schedule(units, output_path=None, fmt="text"):
    """Output design schedule."""
    if not units:
        return

    if fmt == "json":
        output = json.dumps(units, indent=2)
    else:
        # Determine columns
        keys = list(units[0].keys())
        header = "\t".join(keys)
        rows = []
        for u in units:
            rows.append("\t".join(str(u.get(k, "")) for k in keys))
        output = header + "\n" + "\n".join(rows)

    if output_path:
        with open(output_path, "w") as f:
            if fmt == "json":
                json.dump(units, f, indent=2)
            else:
                # Use CSV for file output
                keys = list(units[0].keys())
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(units)
        print(f"Schedule written to {output_path}")

    return output


def run(args):
    if args.list_designs:
        print("Available designs:\n")
        for key, desc in DESIGNS.items():
            print(f"  {key:20s} {desc}")
        return

    if not args.design:
        print("Error: --design required", file=sys.stderr)
        sys.exit(1)

    random.seed(args.seed) if args.seed else None

    units = []

    if args.design == "crd":
        if not args.treatments or not args.n_per_group:
            print("Error: --treatments and --n-per-group required for CRD", file=sys.stderr)
            sys.exit(1)
        units = generate_crd(args.treatments, args.n_per_group)

    elif args.design == "rcbd":
        if not args.treatments or not args.blocks:
            print("Error: --treatments and --blocks required for RCBD", file=sys.stderr)
            sys.exit(1)
        units = generate_rcbd(args.treatments, args.blocks, args.n_per_block or 1)

    elif args.design == "latin-square":
        if not args.treatments or len(args.treatments) < 2:
            print("Error: --treatments requires 2+ treatments for Latin square", file=sys.stderr)
            sys.exit(1)
        units = generate_latin_square(args.treatments)

    elif args.design == "factorial":
        if not args.factors:
            print("Error: --factors required for factorial (format: 'name:levels:label1,label2')", file=sys.stderr)
            sys.exit(1)
        factors = []
        for f_str in args.factors:
            parts = f_str.split(":")
            name = parts[0]
            levels = parts[1] if len(parts) > 1 else "2"
            labels = parts[2] if len(parts) > 2 else ""
            factors.append({"name": name, "levels": levels, "labels": labels})
        units = generate_factorial(factors, args.reps or 1)

    elif args.design == "crossover":
        if not args.treatments or len(args.treatments) < 2:
            print("Error: --treatments requires 2 treatments for crossover", file=sys.stderr)
            sys.exit(1)
        if not args.subjects:
            print("Error: --subjects required for crossover", file=sys.stderr)
            sys.exit(1)
        units = generate_crossover_2x2(args.treatments, args.subjects // 2)

    elif args.design == "split-plot":
        if not args.treatments:
            whole_plot = args.treatments[:2] if len(args.treatments) >= 2 else ["A", "B"]
            sub_plot = args.treatments[2:4] if len(args.treatments) >= 4 else ["C", "D"]
        else:
            whole_plot = ["WP1", "WP2"]
            sub_plot = ["SP1", "SP2"]
        n_reps = args.n_per_group or 3
        units = []
        for rep in range(1, n_reps + 1):
            for wp in whole_plot:
                for sp in sub_plot:
                    units.append({
                        "rep": rep,
                        "whole_plot": wp,
                        "sub_plot": sp,
                        "unit_id": f"R{rep}_{wp}_{sp}"
                    })
        random.shuffle(units)
        for i, u in enumerate(units, 1):
            u["run_order"] = i

    else:
        print(f"Error: unknown design '{args.design}'", file=sys.stderr)
        sys.exit(1)

    if not units:
        print("Error: no units generated", file=sys.stderr)
        sys.exit(1)

    # Summary
    n_total = len(units)
    n_treatments = len(set(u.get("treatment", u.get(units[0]["treatment"] if "treatment" in units[0] else "")) for u in units if "treatment" in u))

    summary = {
        "design": args.design,
        "n_units": n_total,
        "seed": args.seed,
    }

    if args.json:
        print(json.dumps({"summary": summary, "schedule": units}, indent=2, default=str))
    elif args.output:
        keys = list(units[0].keys())
        with open(args.output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(units)
        print(f"Design: {DESIGNS.get(args.design, args.design)}")
        print(f"Schedule: {n_total} experimental units → {args.output}")
        print(f"Seed: {args.seed or 'random'}")
    else:
        print(f"Design: {DESIGNS.get(args.design, args.design)}")
        print(f"Experimental units: {n_total}")
        print(f"Seed: {args.seed or 'random'}")
        print()
        # Show first few rows
        keys = list(units[0].keys())
        print("\t".join(keys))
        for u in units[:min(20, len(units))]:
            print("\t".join(str(u.get(k, "")) for k in keys))
        if len(units) > 20:
            print(f"... and {len(units) - 20} more units")

    if args.engine == "r":
        print("\n--- R equivalent ---")
        if args.design == "crd":
            print("library(agricolae)")
            treatments_str = ", ".join(f'"{t}"' for t in args.treatments)
            print(f'treatments <- c({treatments_str})')
            print(f'design.crd(treatments, r = {args.n_per_group}, seed = {args.seed or 42})')
        elif args.design == "rcbd":
            treatments_str = ", ".join(f'"{t}"' for t in args.treatments)
            print(f'treatments <- c({treatments_str})')
            print(f'design.rcbd(treatments, r = {args.blocks}, seed = {args.seed or 42})')
        elif args.design == "latin-square":
            treatments_str = ", ".join(f'"{t}"' for t in args.treatments)
            print(f'treatments <- c({treatments_str})')
            print(f'design.lsd(treatments, seed = {args.seed or 42})')


def main():
    parser = argparse.ArgumentParser(description="Experimental Design Generator")
    parser.add_argument("--design", choices=list(DESIGNS.keys()), help="Experimental design type")
    parser.add_argument("--list-designs", action="store_true", help="List available designs")
    parser.add_argument("--treatments", nargs="+", help="Treatment level names")
    parser.add_argument("--n-per-group", type=int, help="Subjects per group (CRD) or reps")
    parser.add_argument("--blocks", type=int, help="Number of blocks (RCBD)")
    parser.add_argument("--n-per-block", type=int, default=1, help="Subjects per block per treatment")
    parser.add_argument("--factors", nargs="+", help='Factor specs for factorial: "name:levels:l1,l2"')
    parser.add_argument("--reps", type=int, default=1, help="Replicates per combination (factorial)")
    parser.add_argument("--subjects", type=int, help="Total subjects (crossover)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--output", help="Output CSV file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--engine", choices=["python", "r"], default="python",
                        help="Output language")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
