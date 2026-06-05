# Scikit-Learn Integration Reference

**Source validated against:** scikit-learn 1.8.0 (scikit-learn.org/stable)  
**Last reviewed:** 2026-05-23  
**When to load:** The campaign protocol (Phase 2, 4, 6), baseline modeling, preprocessing, or any task involving sklearn estimators.

---

## Pipeline Composition

Pipelines chain preprocessing and modeling into a single estimator. This enables proper cross-validation (no data leakage from preprocessing) and simplifies deployment.

### Basic Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
])

# Use like a regular estimator
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

### Shortcut: `make_pipeline`

```python
from sklearn.pipeline import make_pipeline

pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
# Step names are auto-generated: "standardscaler", "logisticregression"
```

### Accessing Step Attributes

```python
# After fitting
pipeline.fit(X_train, y_train)

# Access the trained scaler
scaler = pipeline.named_steps["scaler"]
print(f"Mean: {scaler.mean_}")

# Access coefficients from the classifier
coefs = pipeline.named_steps["classifier"].coef_
```

---

## ColumnTransformer (Heterogeneous Data)

When your data has both numeric and categorical columns, use `ColumnTransformer` to apply different preprocessing to different columns.

```python
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder

numeric_features = ["age", "income", "score"]
categorical_features = ["gender", "region", "education"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
])

# Or use column type selectors
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), make_column_selector(dtype_include="number")),
    ("cat", OneHotEncoder(handle_unknown="ignore"),
     make_column_selector(dtype_include="object")),
])
```

### Full Pipeline with ColumnTransformer

```python
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
])

# Grid search over both preprocessing and model params
param_grid = {
    "preprocessor__num__with_mean": [True, False],
    "classifier__n_estimators": [100, 200, 500],
    "classifier__max_depth": [10, 20, None],
}

grid = GridSearchCV(pipeline, param_grid, cv=5, scoring="f1_macro")
grid.fit(X_train, y_train)
```

**Memory-Efficient ColumnTransformer:** Set `remainder="passthrough"` to keep columns not specified, or `remainder="drop"` (default) to drop them.

---

## Preprocessing

### Scaling & Normalization

| Scaler | Description | When |
|---|---|---|
| `StandardScaler` | Z-score: (x - μ) / σ | Default for most models. Assumes roughly Gaussian data. |
| `MinMaxScaler` | Scale to [0, 1] | When bounded ranges matter (neural nets, distance-based). |
| `RobustScaler` | Uses median and IQR | When data has outliers. More robust than StandardScaler. |
| `MaxAbsScaler` | Scale to [-1, 1] | For sparse data (preserves sparsity). |
| `Normalizer` | Unit norm per sample | Text classification, cosine similarity. |

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# StandardScaler is the default
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Always fit on training, transform both train and test
X_test_scaled = scaler.transform(X_test)
```

### Encoding Categorical Features

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

# One-hot (nominal categories — no ordering)
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
X_encoded = encoder.fit_transform(X_categorical)

# Ordinal (ordered categories)
encoder = OrdinalEncoder(categories=[["low", "medium", "high"]])
X_encoded = encoder.fit_transform(X_ordinal)
```

### Handling Missing Values

```python
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer

# Simple imputation (fast)
imputer = SimpleImputer(strategy="median")  # "mean", "median", "most_frequent", "constant"

# KNN imputation (better for local patterns, slower)
imputer = KNNImputer(n_neighbors=5)

# Iterative imputation (MICE-style, best but slow)
imputer = IterativeImputer(max_iter=10, random_state=42)  # Experimental — requires explicit import

# In a pipeline:
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression()),
])
```

---

## Model Selection

### Cross-Validation Strategies

| Splitter | Use Case |
|---|---|
| `KFold(n_splits=5, shuffle=True)` | Default for most tasks |
| `StratifiedKFold(n_splits=5)` | Classification — preserves class proportions |
| `GroupKFold(n_splits=5)` | When samples belong to groups (e.g., same patient) |
| `TimeSeriesSplit(n_splits=5)` | Temporal data — train on past, test on future |
| `RepeatedStratifiedKFold(n_repeats=3)` | More robust estimate, higher variance |
| `LeaveOneOut()` | Very small datasets (< 100 samples) |

```python
from sklearn.model_selection import (
    KFold, StratifiedKFold, GroupKFold, TimeSeriesSplit, cross_val_score, cross_validate
)

# Quick cross-validation score
scores = cross_val_score(pipeline, X, y, cv=StratifiedKFold(5), scoring="f1_macro")
print(f"F1: {scores.mean():.4f} ± {scores.std():.4f}")

# Detailed cross-validation
cv_results = cross_validate(
    pipeline, X, y,
    cv=StratifiedKFold(5),
    scoring=["f1_macro", "accuracy", "roc_auc"],
    return_estimator=True,  # Return fitted models for inspection
    return_train_score=True,  # Detect overfitting
)
```

### Grid Search

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, HalvingGridSearchCV

# Grid search (exhaustive)
grid = GridSearchCV(
    pipeline,
    param_grid={
        "classifier__C": [0.01, 0.1, 1.0, 10.0],
        "classifier__penalty": ["l2"],
    },
    cv=5,
    scoring="f1_macro",
    n_jobs=-1,  # Use all CPU cores
    verbose=1,
)
grid.fit(X_train, y_train)

print(f"Best params: {grid.best_params_}")
print(f"Best score: {grid.best_score_:.4f}")

# Random search (better for high-dimensional spaces)
random_search = RandomizedSearchCV(
    pipeline,
    param_distributions={
        "classifier__C": [0.01, 0.1, 1.0, 10.0, 100.0],
        "classifier__max_iter": [500, 1000, 2000],
    },
    n_iter=20,  # Number of random combinations to try
    cv=5,
    scoring="f1_macro",
    n_jobs=-1,
    random_state=42,
)

# Halving search (successive halving — tries many candidates, prunes poor ones fast)
halving_search = HalvingGridSearchCV(
    pipeline,
    param_grid={"classifier__C": [0.01, 0.1, 1.0, 10.0]},
    factor=3,  # Reduce candidates by factor 3 each iteration
    cv=5,
    scoring="f1_macro",
    n_jobs=-1,
    verbose=1,
)
```

### Nested Cross-Validation (Unbiased Performance Estimate)

```python
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

# Inner CV: model selection
inner_cv = StratifiedKFold(3, shuffle=True, random_state=42)
grid = GridSearchCV(DecisionTreeClassifier(),
                    {"max_depth": [3, 5, 10, None]},
                    cv=inner_cv)

# Outer CV: performance estimation
outer_cv = StratifiedKFold(5, shuffle=True, random_state=42)
nested_scores = cross_val_score(grid, X, y, cv=outer_cv, scoring="f1_macro")
# This gives an unbiased estimate of the tuned model's performance
print(f"Unbiased F1: {nested_scores.mean():.4f} ± {nested_scores.std():.4f}")
```

---

## Ensemble Methods

```python
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    StackingClassifier,
    VotingClassifier,
    AdaBoostClassifier,
    BaggingClassifier,
)

# Stacking (meta-model combines base models)
stack = StackingClassifier(
    estimators=[
        ("rf", RandomForestClassifier(n_estimators=100, random_state=42)),
        ("gb", GradientBoostingClassifier(n_estimators=100, random_state=42)),
        ("svc", LinearSVC(random_state=42)),
    ],
    final_estimator=LogisticRegression(),
    cv=5,
)

# Voting (simple majority or weighted average)
vote = VotingClassifier(
    estimators=[
        ("lr", LogisticRegression()),
        ("rf", RandomForestClassifier(n_estimators=100)),
        ("gnb", GaussianNB()),
    ],
    voting="soft",  # "hard" for majority vote, "soft" for probability average
)
```

### XGBoost / LightGBM Integration

```python
# sklearn-compatible API
import xgboost as xgb
import lightgbm as lgb

xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    eval_metric="logloss",
    use_label_encoder=False,
    random_state=42,
)

lgb_model = lgb.LGBMClassifier(
    n_estimators=200,
    num_leaves=31,
    learning_rate=0.1,
    random_state=42,
    verbose=-1,
)

# Both work in sklearn pipelines and GridSearchCV
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", xgb_model),
])
```

---

## Custom Estimators

### Custom Transformer

```python
from sklearn.base import BaseEstimator, TransformerMixin

class LogTransformer(BaseEstimator, TransformerMixin):
    """Apply log(1 + x) to specified columns."""

    def __init__(self, columns=None):
        self.columns = columns  # None = all columns

    def fit(self, X, y=None):
        # LogTransform doesn't need fitting, but fit must return self
        return self

    def transform(self, X):
        X = X.copy()
        cols = self.columns if self.columns is not None else X.columns
        X[cols] = X[cols].applymap(lambda x: np.log1p(x))  # log1p = log(1+x)
        return X
```

### Custom Estimator

```python
from sklearn.base import BaseEstimator, ClassifierMixin

class SimpleThresholdClassifier(BaseEstimator, ClassifierMixin):
    """Classify based on a learned threshold on one feature."""

    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def fit(self, X, y):
        # Learn optimal threshold
        # Implementation here
        self.is_fitted_ = True
        return self

    def predict(self, X):
        check_is_fitted(self)
        return (X[:, 0] > self.threshold).astype(int)

    def predict_proba(self, X):
        # Not implemented — raises error if called
        raise NotImplementedError("This estimator doesn't support probabilities")
```

### FunctionTransformer (Quick Custom Transform)

```python
import numpy as np
from sklearn.preprocessing import FunctionTransformer

# No class needed for simple transforms
log_transform = FunctionTransformer(func=np.log1p, validate=True)

# In a pipeline:
pipeline = Pipeline([
    ("log", log_transform),
    ("scaler", StandardScaler()),
])
```

---

## Persistence

```python
import joblib

# Save
joblib.dump(pipeline, "model.pkl")

# Load
loaded_pipeline = joblib.load("model.pkl")
predictions = loaded_pipeline.predict(X_new)
```

**⚠️ Security:** `joblib.load` can execute arbitrary code on deserialization. Only load models from trusted sources. Use `pickle` with the same caveat.

**Model portability:** sklearn models versioned with the sklearn version that created them. Cross-version compatibility is not guaranteed. Always save the sklearn version alongside the model.

---

## Imbalanced Data

### Built-in sklearn Support

```python
from sklearn.linear_model import LogisticRegression
from sklearn.utils.class_weight import compute_class_weight

# Option 1: Use class_weight parameter
model = LogisticRegression(class_weight="balanced", max_iter=1000)

# Option 2: Manual class weights
weights = compute_class_weight("balanced", classes=np.unique(y), y=y)
class_weight_dict = dict(zip(np.unique(y), weights))
model = LogisticRegression(class_weight=class_weight_dict, max_iter=1000)
```

### imbalanced-learn Library

```python
from imblearn.over_sampling import SMOTE, ADASYN, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler, NearMiss
from imblearn.pipeline import Pipeline as ImbPipeline  # Note: different import!

# SMOTE in pipeline (SMOTE + classifier)
pipeline = ImbPipeline([
    ("sampler", SMOTE(random_state=42)),
    ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
])
```

---

## Calibration

```python
from sklearn.calibration import CalibratedClassifierCV

# Most sklearn classifiers output uncalibrated probabilities
# Calibrate after training for reliable probability estimates

# Method 1: Platt scaling (sigmoid) — default, good for SVMs, boosting
calibrated = CalibratedClassifierCV(model, method="sigmoid", cv=5)
calibrated.fit(X_train, y_train)
probabilities = calibrated.predict_proba(X_test)

# Method 2: Isotonic regression — non-parametric, needs more data
calibrated = CalibratedClassifierCV(model, method="isotonic", cv=5)
```

---

## Dimensionality Reduction

### PCA

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=0.95)  # Keep 95% of variance
X_pca = pca.fit_transform(X_scaled)

print(f"Components: {pca.n_components_}")  # How many components retained
print(f"Explained variance: {pca.explained_variance_ratio_}")
```

**PCA assumptions:** Data should be scaled first (use `StandardScaler`). PCA assumes linear relationships. PCA is exploratory / descriptive, not inferential — it cannot confirm a hypothesis.

### t-SNE / UMAP (Visualization Only)

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)
```

**⚠️ t-SNE is for visualization only.** The embedding is stochastic and non-parametric. Different runs produce different results. Do not use t-SNE embeddings as input to other models.

---

## Feature Selection

```python
from sklearn.feature_selection import (
    SelectKBest,
    SelectFromModel,
    RFE,
    mutual_info_classif,
    chi2,
)

# Filter method (fast, univariate)
selector = SelectKBest(mutual_info_classif, k=20)
X_selected = selector.fit_transform(X, y)

# Wrapper method (RFE — Recursive Feature Elimination)
selector = RFE(estimator=RandomForestClassifier(), n_features_to_select=20)
X_selected = selector.fit_transform(X, y)

# Embedded method (from model coefficients)
selector = SelectFromModel(
    LogisticRegression(C=1.0, max_iter=1000, penalty="l1", solver="libao"),
    max_features=20,
    threshold="median",
)

# In a pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("feature_selection", SelectKBest(mutual_info_classif, k=20)),
    ("classifier", RandomForestClassifier(n_estimators=200)),
])
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Data leakage from preprocessing | Overly optimistic CV scores | Always use `Pipeline` for preprocessing |
| `OneHotEncoder` creates too many features | High-dimensional sparse matrix | Use `min_frequency=0.01` to group rare categories |
| `KNNImputer` on unscaled data | Poor imputation | Scale before imputing |
| `GridSearchCV` on entire parameter space | Search takes days | Use `RandomizedSearchCV` for > 5 params |
| Using `PCA` before train/test split | Data leakage | PCA in pipeline, fitted on training only |
| `stratify` parameter in `train_test_split` | Uneven class distribution in splits | Always `stratify=y` for classification |
| Not setting `random_state` | Non-reproducible results | Set `random_state=42` on every estimator |
| `joblib.load` from untrusted source | Code execution vulnerability | Only load models you trained |

---

## Reproducibility

```python
import numpy as np

# Set random state on every estimator
model = RandomForestClassifier(n_estimators=200, random_state=42)

# Set numpy seed for reproducibility in preprocessing
np.random.seed(42)

# Use the same seed in train_test_split and CV
from sklearn.model_selection import train_test_split, KFold
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
cv = KFold(n_splits=5, shuffle=True, random_state=42)
```

---

## See Also

- `references/experimental-campaign-protocol.md` — where this reference fits in the campaign workflow (Baseline phase)
- `references/pytorch-integration.md` — for deep learning methods
- `references/data-science-coding-workflow.md` — project structure, experiment logging
- scikit-learn.org/stable/user_guide — official user guide
