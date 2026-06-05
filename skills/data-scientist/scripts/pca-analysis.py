#!/usr/bin/env python3
"""
pca-analysis.py — Run PCA on a CSV dataset with standardized workflow.

Usage:
  python3 pca-analysis.py <csv_path> [options]

Options:
  --numeric COLS         Comma-separated list of numeric columns to include.
                         Default: all numeric columns except those in --exclude.
  --categorical COLS     Comma-separated list of categorical columns to one-hot encode.
                         Default: [].
  --exclude COLS         Comma-separated columns to exclude (e.g. IDs, names, dates).
                         Default: "Project ID,Building ID,Building Name,Project Name".
  --fillna VALUE         Value to fill NaN with. Use "0" for count data, "mean" for mean,
                         "median" for median, "drop" to drop rows with any NaN. [default: 0]
  --groupby COL          Categorical column to compute group means on PC1/PC2.
                         Default: None.
  --n-components N       Number of components to show in output. [default: 15]
  --output-csv PATH      Save PC projections to a CSV file. Optional.
  --no-standardize       Skip standardization (not recommended for mixed-scale data).
  --seed N               Random seed for reproducibility. [default: 42]

Examples:
  # Basic PCA on all numeric columns, NaN->0
  python3 pca-analysis.py data.csv

  # PCA with selected numeric columns + one-hot encoded borough
  python3 pca-analysis.py data.csv \\
    --numeric "Total Units,1-BR Units,2-BR Units,3-BR Units" \\
    --categorical "Borough" --groupby "Borough"

  # Mean-impute missing values, exclude ID columns
  python3 pca-analysis.py housing.csv \\
    --exclude "Project ID,BBL,BIN" --fillna mean

  # Save projections for downstream modeling
  python3 pca-analysis.py housing.csv --output-csv pca_projections.csv
"""
import sys
import argparse
import warnings
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')


def main():
    parser = argparse.ArgumentParser(description='Run PCA on a CSV dataset')
    parser.add_argument('csv_path', help='Path to input CSV file')
    parser.add_argument('--numeric', help='Comma-separated numeric columns')
    parser.add_argument('--categorical', default='', help='Comma-separated categorical columns to one-hot encode')
    parser.add_argument('--exclude', default='Project ID,Building ID,Building Name,Project Name',
                        help='Comma-separated columns to exclude')
    parser.add_argument('--fillna', default='0', choices=['0', 'mean', 'median', 'drop'],
                        help='NaN handling strategy')
    parser.add_argument('--groupby', default=None, help='Column for group-mean analysis on PCs')
    parser.add_argument('--n-components', type=int, default=15, help='Components to show (default: 15)')
    parser.add_argument('--output-csv', default=None, help='Save PC projections to CSV')
    parser.add_argument('--no-standardize', action='store_true', help='Skip standardization')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    args = parser.parse_args()

    np.random.seed(args.seed)
    print(f"Reading: {args.csv_path}")
    df = pd.read_csv(args.csv_path)
    print(f"  Shape: {df.shape[0]} rows x {df.shape[1]} cols\n")

    # Determine numeric columns
    exclude_cols = [c.strip() for c in args.exclude.split(',') if c.strip()]

    if args.numeric:
        numeric_cols = [c.strip() for c in args.numeric.split(',') if c.strip()]
        missing = [c for c in numeric_cols if c not in df.columns]
        if missing:
            print(f"  ERROR: numeric columns not found: {missing}", file=sys.stderr)
            sys.exit(1)
    else:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [c for c in numeric_cols if c not in exclude_cols]

    # Categorical columns
    cat_cols_arg = [c.strip() for c in args.categorical.split(',') if c.strip()]

    print(f"  Numeric features: {len(numeric_cols)}")
    for c in numeric_cols:
        nulls = df[c].isna().sum()
        print(f"    {c:45s}  nulls={nulls}")

    if cat_cols_arg:
        print(f"  Categorical features: {len(cat_cols_arg)} -> {len(cat_cols_arg)} dummy variables")
        for c in cat_cols_arg:
            print(f"    {c}: {df[c].nunique()} categories")
    else:
        print(f"  Categorical features: none")

    # Build feature matrix
    X_numeric = df[numeric_cols].values.copy()

    # Handle NaN
    if args.fillna == '0':
        X_numeric = np.nan_to_num(X_numeric, nan=0.0)
    elif args.fillna == 'mean':
        col_means = np.nanmean(X_numeric, axis=0)
        inds = np.where(np.isnan(X_numeric))
        X_numeric[inds] = np.take(col_means, inds[1])
    elif args.fillna == 'median':
        col_medians = np.nanmedian(X_numeric, axis=0)
        inds = np.where(np.isnan(X_numeric))
        X_numeric[inds] = np.take(col_medians, inds[1])
    elif args.fillna == 'drop':
        valid_rows = ~np.isnan(X_numeric).any(axis=1)
        if not valid_rows.all():
            print(f"\n  Dropping { (~valid_rows).sum() } rows with NaN")
            X_numeric = X_numeric[valid_rows]
            df = df.iloc[valid_rows].copy()

    # Categorical encoding
    X_cat = None
    feature_names = list(numeric_cols)
    if cat_cols_arg:
        dummies = pd.get_dummies(df[cat_cols_arg], drop_first=True)
        X_cat = dummies.values.astype(float)
        feature_names += list(dummies.columns)

    X = np.hstack([X_numeric, X_cat]) if X_cat is not None else X_numeric

    print(f"\n  Final feature matrix: {X.shape[0]} rows x {X.shape[1]} features\n")

    # Standardize
    if args.no_standardize:
        X_scaled = X.copy()
        print("  NOTE: Skipping standardization -- features on different scales will dominate")
    else:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        print("  Applied StandardScaler (z-scores)\n")

    # Run PCA
    pca = PCA()
    X_pca = pca.fit_transform(X_scaled)
    n_show = min(args.n_components, pca.n_components_)

    # Variance explained table
    cum_var = np.cumsum(pca.explained_variance_ratio_) * 100
    print(f"{'PC':>4s}  {'Eigenval':>10s}  {'Var %':>8s}  {'Cumul %':>8s}")
    print("-" * 38)
    for i in range(n_show):
        ev = pca.explained_variance_[i]
        vr = pca.explained_variance_ratio_[i] * 100
        cu = cum_var[i]
        marker = ""
        if i > 0 and vr < pca.explained_variance_ratio_[i-1]*100 * 0.5 and vr < 5:
            marker = " <-- elbow"
        print(f"PC{i+1:2d}  {ev:10.4f}  {vr:7.2f}%  {cu:7.2f}%{marker}")

    # Detect natural elbow
    ratios = pca.explained_variance_ratio_
    if len(ratios) > 2:
        drops = [(ratios[i] - ratios[i+1], i) for i in range(min(len(ratios)-1, 20))]
        max_drop = max(drops, key=lambda x: x[0])
        elbow_pc = max_drop[1] + 1
    else:
        elbow_pc = None

    print(f"\n  PCs with eigenvalue > 1: {(pca.explained_variance_ > 1).sum()}")
    if elbow_pc:
        print(f"  Scree elbow ~ PC{elbow_pc} (largest drop in variance ratio)")
    for threshold in [70, 80, 90]:
        n_needed = int(np.argmax(cum_var >= threshold)) + 1
        if n_needed <= n_show:
            print(f"  PCs to reach {threshold}% variance: {n_needed}")

    # Top loadings for PC1, PC2, PC3
    print(f"\n{'='*70}")
    print("TOP LOADINGS")
    print('='*70)

    loadings_df = pd.DataFrame(
        pca.components_.T,
        columns=[f'PC{i+1}' for i in range(pca.n_components_)],
        index=feature_names
    )

    for pc_idx in [0, 1, 2]:
        if pc_idx >= pca.n_components_:
            break
        pc_name = f'PC{pc_idx+1}'
        pc_var = pca.explained_variance_ratio_[pc_idx] * 100
        sorted_loadings = loadings_df[pc_name].abs().sort_values(ascending=False)
        top_n = sorted_loadings.head(10)

        print(f"\n--- {pc_name} ({pc_var:.1f}% variance) ---")
        for feat in top_n.index:
            val = loadings_df.loc[feat, pc_name]
            bar = chr(9608) * max(1, int(abs(val) * 20))
            print(f"  {feat:45s}  {val:+.4f}  {bar}")

    # Group means
    if args.groupby and args.groupby in df.columns:
        df_out = df.copy()
        df_out['PC1'] = X_pca[:, 0]
        df_out['PC2'] = X_pca[:, 1]
        if X_pca.shape[1] >= 3:
            df_out['PC3'] = X_pca[:, 2]

        print(f"\n{'='*70}")
        print(f"GROUP MEANS BY '{args.groupby}' ON PC1-PC3")
        print('='*70)
        group_cols = ['PC1', 'PC2']
        if X_pca.shape[1] >= 3:
            group_cols.append('PC3')
        grouped = df_out.groupby(args.groupby)[group_cols].agg(['mean', 'std', 'count'])
        print(grouped.round(3).to_string())

    # Save projections
    if args.output_csv:
        out = df.copy()
        for i in range(min(X_pca.shape[1], 10)):
            out[f'PC{i+1}'] = X_pca[:, i]
        out.to_csv(args.output_csv, index=False)
        print(f"\n  Projections saved to: {args.output_csv}")

    # Summary interpretation hints
    print(f"\n{'='*70}")
    print("INTERPRETATION GUIDE")
    print('='*70)
    main_loading_pc1 = loadings_df['PC1'].abs().idxmax()
    print(f"  PC1 shares direction with: {main_loading_pc1}")
    print(f"  PC1 opposes: {loadings_df['PC1'].idxmin()} vs {loadings_df['PC1'].idxmax()}")
    print(f"  PC2 shares direction with: {loadings_df['PC2'].abs().idxmax()}")
    least_influential = loadings_df[['PC1','PC2','PC3']].abs().sum(axis=1).idxmin()
    print(f"  Feature with least PC1-PC3 influence: {least_influential}")
    print()
    total_var_first_3 = pca.explained_variance_ratio_[:3].sum() * 100
    if total_var_first_3 < 50:
        print(f"  NOTE: First 3 PCs explain only {total_var_first_3:.1f}% of variance.")
        print(f"  The data is genuinely high-dimensional. Examine PC4-PC{min(10, n_show)}.")
    else:
        print(f"  First 3 PCs explain {total_var_first_3:.1f}% of variance.")
        print(f"  Moderate-to-strong dimensionality reduction achieved.")


if __name__ == '__main__':
    main()
