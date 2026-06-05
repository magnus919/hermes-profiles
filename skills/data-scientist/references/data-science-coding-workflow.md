# Data Science Coding Workflow

**Source validated against:** Cookiecutter Data Science, MLflow documentation, DVC documentation, Kedro documentation, established DS project conventions.  
**Last reviewed:** 2026-05-23  
**When to load:** The campaign protocol has produced results and you need to structure them into a reproducible project; or the user asks "how should I set up this DS project?"

---

## Project Directory Structure

A consistent project structure makes experiments reproducible, results findable, and collaboration possible.

### Recommended Layout

```
project/
├── data/
│   ├── raw/               # Immutable original data
│   ├── processed/          # Cleaned, feature-engineered data
│   └── external/           # External reference data (lookups, metadata)
├── notebooks/              # Exploratory analysis, prototypes
│   └── 01-exploration.ipynb
├── src/                    # Reusable code
│   ├── __init__.py
│   ├── features/           # Feature engineering
│   ├── models/             # Model definitions, training logic
│   └── utils/              # Helper functions (logging, metrics)
├── models/                 # Trained model artifacts
│   └── run_001/
│       ├── model.pt
│       └── config.json
├── reports/                # Generated analysis, figures
│   └── figures/
├── config/
│   ├── config.yaml         # Experiment configuration
│   └── params.yaml         # Hyperparameters
├── experiments/
│   └── experiment_log.json  # Structured experiment record
├── requirements.txt
├── environment.yaml        # Conda env export
├── setup.py                # If src/ is a Python package
├── Makefile                # Common commands (make train, make test)
└── README.md
```

### Quick Bootstrap

```bash
# Using Cookiecutter Data Science (cookiecutter)
python -m pip install cookiecutter
cookiecutter https://github.com/drivendata/cookiecutter-data-science
```

### The Golden Rule

**Raw data is read-only.** Never modify `data/raw/`. Always create derived data in `data/processed/` with explicit scripts. This ensures reproducibility — any change to processing is captured in the script, not hidden in a manual edit.

---

## Configuration Management

### YAML Config Pattern

```yaml
# config/config.yaml
data:
  raw_path: "data/raw/dataset.csv"
  test_size: 0.2
  random_state: 42

preprocessing:
  scaling: "standard"
  handle_missing: "median"
  categorical_encoding: "onehot"

model:
  name: "random_forest"
  params:
    n_estimators: 200
    max_depth: 10
    random_state: 42

training:
  batch_size: 32
  learning_rate: 0.001
  epochs: 100
```

### Loading Config in Python

```python
import yaml
from pathlib import Path

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

# Use config throughout the code
model_class = config["model"]["name"]
model_params = config["model"]["params"]
```

### Sweep Config (for Hyperparameter Search)

```yaml
# config/sweep.yaml
parameters:
  learning_rate: [0.0001, 0.001, 0.01]
  batch_size: [16, 32, 64]
  n_layers: [2, 4, 6]
```

### OmegaConf / Hydra (Advanced)

For complex experiment configurations with hierarchical overrides:

```python
# pip install omegaconf
from omegaconf import OmegaConf

config = OmegaConf.create("""
model:
  name: resnet50
  pretrained: true
data:
  path: ./data
  augment: true
""")

# Override from command line or code
config.model.name = "efficientnet"
```

---

## Experiment Logging

### Why Log Experiments

Without logging, you lose the mapping between code, data, hyperparameters, and results. A year later, "run_004" means nothing. Logging solves:
- **What** hyperparameters produced this result?
- **Where** is the trained model artifact?
- **When** was it trained (data version, code version)?
- **How** does this compare to previous runs?

### Minimal Logging (JSON File)

```python
import json
from datetime import datetime
from pathlib import Path

def log_experiment(
    experiment_dir: str,
    model_name: str,
    params: dict,
    metrics: dict,
    model_path: str = None,
) -> dict:
    """Log a single experiment to a JSON file."""
    log_path = Path(experiment_dir) / "experiment_log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "model_name": model_name,
        "params": params,
        "metrics": metrics,
        "model_path": model_path,
    }

    # Append to log
    if log_path.exists():
        with open(log_path) as f:
            log = json.load(f)
    else:
        log = []
    log.append(entry)

    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)

    return entry
```

### MLflow Tracking

```python
# pip install mlflow
import mlflow

mlflow.set_experiment("customer-churn")

with mlflow.start_run(run_name="random_forest_v2"):
    # Log parameters
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("max_depth", 10)

    # Log metrics
    mlflow.log_metric("f1", 0.87)
    mlflow.log_metric("accuracy", 0.91)

    # Log model
    mlflow.sklearn.log_model(pipeline, "model")

    # Log artifacts (figures, configs)
    mlflow.log_artifact("config/config.yaml")
    mlflow.log_artifact("reports/confusion_matrix.png")

    # Log tags for searchability
    mlflow.set_tag("dataset_version", "v2.1")
    mlflow.set_tag("status", "candidate")
```

### TensorBoard (for Deep Learning)

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter(log_dir="runs/experiment_1")

# Log per-epoch metrics
for epoch in range(num_epochs):
    train_loss = train_one_epoch(model, dataloader)
    val_loss, val_acc = evaluate(model, val_loader)

    writer.add_scalar("Loss/train", train_loss, epoch)
    writer.add_scalar("Loss/val", val_loss, epoch)
    writer.add_scalar("Accuracy/val", val_acc, epoch)

    # Log model graph (once)
    if epoch == 0:
        writer.add_graph(model, example_input)

# Launch: tensorboard --logdir runs/
```

### WandB (Weights & Biases)

```python
# pip install wandb
import wandb

wandb.init(project="customer-churn", config={
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 100,
})

# Log metrics
for epoch in range(config["epochs"]):
    loss = train_step()
    wandb.log({"loss": loss, "epoch": epoch})

# Log model
wandb.save("model.pt")
```

**When to use what:**

| Tool | Best For | Hosting |
|---|---|---|
| JSON file | Single user, no infrastructure | Local |
| MLflow | Teams, experiment comparison | Self-hosted or Databricks |
| TensorBoard | Deep learning training curves | Local |
| WandB | Collaborative DL experiments | Cloud (SaaS) |

---

## Result Serialization

| Data Type | Format | Library | Notes |
|---|---|---|---|
| Tabular data | Parquet | `pandas.DataFrame.to_parquet()` | Fast, compressed, columnar. **Best choice for most data.** |
| Metrics / hyperparams | JSON | `json.dump()` | Human-readable, universally parseable |
| Model (sklearn) | `.pkl` / `.joblib` | `joblib.dump()` | Load with `joblib.load()` |
| Model (PyTorch) | `.pt` / `.pth` | `torch.save()` | Use state_dict format |
| Model (export) | `.onnx` | `torch.onnx.export()` | Framework-neutral, deployable anywhere |
| Figures | `.png` / `.pdf` | `matplotlib.savefig()` | 300 DPI minimum for publication |
| Intermediate data | Feather | `pandas.DataFrame.to_feather()` | Fast read/write, no compression |

```python
# Parquet — best for tabular data
df.to_parquet("data/processed/features.parquet")
df = pd.read_parquet("data/processed/features.parquet")

# JSON — best for metrics
with open("reports/metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

# Joblib — best for sklearn models
import joblib
joblib.dump(pipeline, "models/pipeline_v2.pkl")
```

---

## Reproducibility

### Seed Management

```python
import random
import numpy as np
import torch

def set_all_seeds(seed: int = 42):
    """Set seeds for all random number generators used in ML."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
```

### Environment Pinning

```bash
# pip: freeze exact versions
pip freeze > requirements.txt

# conda: export full environment
conda env export > environment.yaml

# pip-compile (pip-tools): layered requirements
# requirements.in has loose deps, requirements.txt has pinned
```

### Docker for Full Reproducibility

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY config/ config/
ENTRYPOINT ["python", "src/train.py"]
```

**When Docker is overkill:** Single-script analyses, exploration, individual experiment debugging. Use pinned requirements + seed setting instead.

**When Docker is necessary:** Team projects, production deployment, sharing with non-technical stakeholders, running experiments on different hardware.

### Code Version Tracking

```python
# Embed git commit hash in experiment log
import subprocess

def get_git_commit_hash():
    """Get the current git commit hash."""
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"

# Include in experiment log:
log_entry["git_commit"] = get_git_commit_hash()
```

---

## Data Versioning

### DVC (Data Version Control)

```bash
# pip install dvc
dvc init
dvc add data/raw/dataset.csv       # Tracks dataset with .dvc file
git add data/raw/dataset.csv.dvc    # Commit pointer, not data
git commit -m "add dataset v1"

# Push to remote storage
dvc remote add myremote s3://mybucket/dvc
dvc push

# Later, pull a specific version
git checkout <commit_hash>
dvc checkout  # Restores the matching data version
```

### Without DVC: Simple Hash-Based Cache

```python
import hashlib
from pathlib import Path

def hash_file(path: Path) -> str:
    """SHA-256 hash of a file for integrity checking."""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Store hash alongside experiment results
dataset_hash = hash_file("data/raw/dataset.csv")
log_entry["data_hash"] = dataset_hash
```

---

## Unit Testing for Data Science

### Test Data Pattern

```python
def test_feature_engineering():
    """Test feature engineering with a tiny known dataset."""
    # Arrange: create 5-sample dataset with known properties
    X_test = pd.DataFrame({
        "age": [25, 30, 45, 60, 35],
        "income": [50000, 60000, 80000, 120000, 75000],
        "gender": ["M", "F", "F", "M", "F"],
    })

    # Act
    result = create_features(X_test)

    # Assert: known properties
    assert result.shape[0] == 5, "Should preserve row count"
    assert "age_scaled" in result.columns, "Should have age_scaled column"
    assert result["age_scaled"].std() > 0, "Scaled values should have variance"
```

### Model Invariance Test

```python
def test_model_output_shape():
    """Model should produce correct output shape on valid input."""
    X_sample = np.random.randn(32, 10)  # 32 samples, 10 features
    y_sample = (X_sample[:, 0] > 0).astype(int)

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_sample, y_sample)

    predictions = model.predict(X_sample)
    assert predictions.shape == (32,), "Should output one prediction per sample"
    assert set(predictions).issubset({0, 1}), "Should predict binary classes"
```

### Data Integrity Tests

```python
def test_no_missing_values_after_imputation():
    """Preprocessing should handle all missing values."""
    # Load a sample of processed data
    X = pd.read_parquet("data/processed/features.parquet")
    assert X.isnull().sum().sum() == 0, "No missing values should remain"

def test_target_distribution():
    """Target variable should have expected distribution."""
    df = pd.read_parquet("data/processed/train.parquet")
    class_counts = df["target"].value_counts()
    # Warn if any class has < 1% prevalence
    for cls, count in class_counts.items():
        assert count / len(df) >= 0.01, f"Class {cls} has < 1% prevalence"
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Notebooks with unnumbered cells | Can't reproduce order | Number cells (01-load, 02-explore, 03-model). Convert to scripts before production. |
| Hardcoded file paths | Code breaks on different machines | Use `pathlib.Path`, config files, or `os.getenv` |
| No `random_state` | Results change each run | Set seeds at the top of every script |
| Data leakage in preprocessing | Overly optimistic results | Fit preprocessors on training data only, use `Pipeline` |
| Training on full data before evaluation | No held-out test set | Always split before any modeling |
| Git-ignored data/ directory | No one else can run the code | Use DVC or document how to obtain data |
| One giant `train.py` | Hard to debug, test, reuse | Split into `features.py`, `model.py`, `train.py`, `evaluate.py` |

---

## See Also

- `references/experimental-campaign-protocol.md` — the high-level workflow this supports
- `references/pytorch-integration.md` — training loops and model persistence
- `references/sklearn-integration.md` — pipelines and model selection
- `assets/experimental-plan-template.md` — pre-registration-style planning document
- `assets/report-template.md` — analysis report format
