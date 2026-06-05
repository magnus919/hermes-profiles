# PCA Workflow

Principal Component Analysis (PCA) is a linear dimensionality reduction technique. It identifies orthogonal axes (principal components) that capture maximum variance in the data. Use it for exploratory analysis, multicollinearity diagnosis, feature engineering, visualization, and noise reduction.

---

## When to Use PCA

| Good Fit | Poor Fit |
|----------|----------|
| Many correlated numeric features | Mostly categorical/binary data |
| Exploratory phase — "what's the structure here?" | Confirmatory hypothesis testing |
| Multicollinearity (PCA handles this natively) | You need interpretable individual features |
| Preprocessing for downstream models | Missingness is >30% with no defensible imputation |
| Visualization (2D/3D projection of high-dim data) | Data is already low-dim (<5 features) |

---

## Assumptions

1. **Linearity** — PCA captures linear relationships. Non-linear structure (manifolds, clusters) may be missed or split across components.
2. **Variance = information** — Components are ordered by variance explained. Components with very low variance may still carry signal (especially in zero-inflated data).
3. **Scale matters** — Variables with larger scales dominate unstandardized PCA. **Always standardize** when variables are on different units (counts, dollars, square footage).
4. **Outlier sensitivity** — Extreme observations can distort the eigen-decomposition. Check for univariate and multivariate outliers before running.
5. **Continuous-ish** — Binary variables and sparse dummy indicators can be included but will form their own components rather than integrating with continuous structure.

---

## Data Preparation Protocol

### Step 1: Select Features

Exclude IDs, names, dates, spatial identifiers (unless spatial PCA is the goal). Keep:
- Numeric measurements (counts, amounts, rates)
- Ordered categoricals with sufficient levels (consider encoding)
- Binary indicators (use with caution — see pitfall below)

### Step 2: Handle Missing Values

PCA cannot handle NaN. Choose a strategy:

| Strategy | When | Example |
|----------|------|---------|
| Fill with 0 | Count data where NaN ≈ absence | "Zero units of this type" |
| Mean/median imputation | Continuous data, low missingness (<10%) | "Missing sensor reading ≈ average" |
| Row-wise drop | Minimal missingness, complete-case analysis | <5% of rows affected |
| KNN imputation | Moderate missingness, correlated features | 10-30% missing with good predictors |
| Flag + impute | Missingness itself is informative | Add a binary "was_missing" column |

**Count data pitfall:** When count columns are mostly 0 but stored as NaN, filling with 0 is often correct — but it creates zero-inflated distributions that violate normality assumptions. PCA still works (it's finding variance structure), but variance ratios will be lower. This is not a bug — low variance per PC in zero-inflated data *is* informative (it means no single factor dominates).

### Step 3: Encode Categoricals

- **Nominal** (borough, construction type): One-hot encode. Each dummy becomes a binary variable.
- **Ordinal** (income tier, star rating): Consider ordinal encoding if levels have meaningful spacing.
- **Dropping first category** (drop='first'): Avoids perfect multicollinearity of the dummy set.

**Important:** Dummy variables form their own geometric structure in PCA space. A component dominated by one-hot encoded borough variables is a "geography component," not a "housing characteristic component." Interpret accordingly.

### Step 4: Standardize

Always use `StandardScaler` (z-scores: center to 0, scale to unit variance).

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

**Do not standardize** binary dummy variables — they lose their 0/1 interpretability. Either:
- Keep them unscaled alongside scaled continuous variables (they'll have smaller influence), or
- Accept that the component is a weighted sum of z-scores where binary variables contribute less.

### Step 5: Run PCA

```python
from sklearn.decomposition import PCA
pca = PCA()
X_pca = pca.fit_transform(X_scaled)
```

---

## Interpreting PCA Output

### Variance Explained

The primary diagnostic. Print first N components:

| Information | What to Look For |
|-------------|------------------|
| `explained_variance_ratio_` | Proportion of total variance per PC |
| `cumsum()` | Cumulative variance explained by first K PCs |
| Eigenvalues > 1 (Kaiser rule) | Components that explain more than one variable's worth of variance |
| Scree plot elbow | Diminishing returns — the point where additional PCs add little |

**Low variance per PC (<30% for PC1) is not a failure.** It means the data is genuinely high-dimensional — many independent sources of variation. This is common in:
- Zero-inflated count data (housing units, purchase data)
- Heterogeneous populations with many sub-types
- Spatial data with multiple geographic regimes

### Loadings (Components_)

The weight of each original variable on each PC. These are the key interpretable output.

**Reading a loading vector:**
- Variables with |loading| > 0.25 contribute meaningfully
- Variables with the same sign move together (positive correlation on that axis)
- Variables with opposite signs represent a trade-off on that axis
- The sum of squared loadings per PC = 1 (unit length)

**Labeling a component:** Look at the 3-5 highest |loading| variables and ask "what concept do they share?"

```
PC1: +0.39 All Counted Units, +0.34 1-BR Units, +0.33 2-BR Units, +0.32 Total Units
→ Label: "Building Size"
```

### Projections (X_pca)

The coordinates of each observation in the new PC space. Use these for:
- **Visualization:** Scatter plot of PC1 vs PC2, colored by a grouping variable
- **Outlier detection:** Points far from origin in PC space
- **Clustering input:** PCs as features for K-means or hierarchical clustering
- **Regression input:** PCs as orthogonal predictors (solves multicollinearity)

### Adding Group Means

Compute mean PC1, PC2 by a grouping variable (borough, construction type, etc.) to see how categories separate in the latent space. This reveals which dimensions drive group differences.

---

## Common Pitfalls

### 1. Assuming PCs Have Intrinsic Meaning
A component labeled "Building Size" isn't the same as the variable "Total Units." It's a latent construct that loads on Total Units plus correlated features (1-BR, 2-BR, rental counts). Label descriptively, not reductively.

### 2. Interpreting Non-Significant Loadings
Loading of 0.05 on a variable with others at 0.40 is noise. Focus on the high-magnitude loadings. A common heuristic: interpret loadings with |value| > 0.3 or above the threshold where a meaningful gap appears.

### 3. Over-Rotating Components
Varimax rotation can make loadings sparser and more interpretable, but it changes the variance distribution. Report unrotated results first; use rotation only as a communication aid.

### 4. Ignoring Negative Space
A variable with near-zero loading on PC1-PC5 is *interesting* — it means that variable varies independently of the major variance components. This is a finding worth reporting.

### 5. PCA on Mixed Data Types
Binary dummies + count data + continuous measurements in the same PCA is common practice but the components will be influenced heavily by the largest-variance block. Consider running separate PCAs per data type (unit-mix PCA, income-level PCA, spatial PCA) and then comparing.

---

## Worked Example: NYC Housing Data

From a session on the NYC Affordable Housing dataset (9,250 buildings, 25 features after encoding):

- **PC1 (26.3%)** — "Building Size": All unit counts load positively. Manhattan buildings score highest; Staten Island lowest.
- **PC2 (8.9%)** — "Rental vs Homeownership": Homeownership units (+), studio rentals (-). Preservation clusters positive; new construction clusters negative.
- **PC3 (7.0%)** — "Policy × Geography": Preservation + Extended Affordability + Manhattan load together.

**Key insight:** Only 26% of variance in PC1 despite strong correlation structure in unit counts. The zero-inflation and geographic heterogeneity disperse variance across many dimensions. This IS the finding — affordable housing production is not a one-dimensional phenomenon.

---

## Alternative Methods

| Method | When Over PCA |
|--------|--------------|
| **t-SNE** | Visualization of non-linear structure; not for downstream modeling |
| **UMAP** | Visualization + some structure preservation for clustering |
| **Factor Analysis** | You believe latent factors generated the observed data (model-based) |
| **ICA** | You want statistically independent components, not just uncorrelated |
| **NMF** | Non-negative data where you want additive parts-based representation |
| **Sparse PCA** | Many noise variables; you want interpretable components with few non-zero loadings |
| **Kernel PCA** | Non-linear relationships in the data |
