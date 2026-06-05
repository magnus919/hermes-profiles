# Docker Experiment Isolation

**When to load this reference:** Running resource-intensive experiments (deep learning training, hyperparameter sweeps) that could destabilize the host if they go wrong. Use Docker containers to contain crashes, limit resource usage, and ensure reproducibility.

---

## Why Containerize Experiments

| Risk | Without Docker | With Docker |
|---|---|---|
| OOM kills the experiment AND your SSH session | Host runs out of swap, becomes unresponsive | Container hits memory limit, gets OOM-killed. Host is fine. |
| Experiment fills up disk | `/tmp` fills, other processes fail | Container disk limit, clean shutdown |
| Python dependency conflict | `pip install` breaks other projects | Isolated Python environment per container |
| "It works on my machine" | Hours of debugging environment differences | Same Docker image = same environment |
| GPU memory leak over many trials | VRAM fragments, subsequent trials crash | Containers freed after each trial |

---

## Quick Start: Single Experiment

### Dockerfile

```dockerfile
FROM pytorch/pytorch:2.5.0-cuda12.4-cudnn9-devel

# Install Python dependencies
RUN pip install --no-cache-dir \
    scikit-learn \
    pandas \
    numpy \
    scipy \
    optuna \
    tensorboard \
    mlflow

# Copy experiment code
COPY src/ /workspace/src/
COPY config/ /workspace/config/
WORKDIR /workspace

# Run training by default
ENTRYPOINT ["python", "src/train.py"]
```

### Build and Run with Resource Limits

```bash
# Build
docker build -t experiment-runner -f Dockerfile .

# Run with resource constraints
docker run --rm \
    --gpus '"device=0"' \          # Use GPU 0 only
    --memory=16g \                  # Hard memory limit
    --memory-swap=16g \             # Disable swap (prevents swapping to disk)
    --cpus=4 \                      # Limit to 4 CPU cores
    --shm-size=8g \                 # Increased /dev/shm (needed for DataLoader with many workers)
    -v /mnt/data:/workspace/data \  # Mount data directory
    -v $(pwd)/output:/workspace/output \
    -e CUDA_VISIBLE_DEVICES=0 \
    -e WANDB_API_KEY=$WANDB_API_KEY \
    experiment-runner \
    --config config/experiment.yaml
```

---

## Resource Limit Reference

| Flag | Recommended Setting | Why |
|---|---|---|
| `--memory` | 75% of host RAM | Leaves headroom for system processes |
| `--memory-swap` | Same as `--memory` | Disables swap — OOM kills the container instead of thrashing |
| `--cpus` | Host CPU count - 2 | Leaves CPUs for system, Docker daemon, monitoring |
| `--gpus` | `"device=0"` or `"all"` | Pin to specific GPU to avoid conflicts |
| `--shm-size` | `8g` or more | PyTorch DataLoader uses `/dev/shm` for shared memory. Default 64MB is too small. |
| `--pids-limit` | `1000` | Prevents fork bombs from runaway experiments |
| `--ulimit nofile` | `1024` | Prevents file descriptor exhaustion |
| `--storage-opt size` | `50GB` | Limits container disk usage |

### Full Resource-Constrained Run

```bash
docker run --rm \
    --gpus '"device=0"' \
    --memory=16g --memory-swap=16g \
    --cpus=4 \
    --shm-size=8g \
    --pids-limit=1000 \
    --storage-opt size=50GB \
    --ulimit nofile=1024:1024 \
    -v /mnt/data:/workspace/data:ro \    # Read-only data mount
    -v $(pwd)/output:/workspace/output \
    experiment-runner
```

---

## Log Collection Pattern

### Write Logs to stdout (Docker-Friendly)

```python
# In your training script — write all logs to stdout so docker logs works
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,  # ← Write to stdout, not stderr or a file
    force=True,
)

# Now docker logs captures everything
logger = logging.getLogger(__name__)
logger.info(f"Starting training with config: {config}")
```

### Capturing Logs from Container

```bash
# Run container in background
CONTAINER_ID=$(docker run -d --gpus all --memory=16g experiment-runner)

# Stream logs live
docker logs -f $CONTAINER_ID

# Wait for completion and get exit code
EXIT_CODE=$(docker wait $CONTAINER_ID)
echo "Exit code: $EXIT_CODE"

# Save logs to file
docker logs $CONTAINER_ID > "experiment_log_$(date +%Y%m%d_%H%M%S).txt"
```

---

## Experiment Sweep (Multiple Containers)

```bash
for trial in {1..10}; do
    docker run -d \
        --gpus '"device=0"' \
        --memory=16g \
        --name "experiment_trial_$trial" \
        -v $(pwd)/output:/workspace/output \
        experiment-runner \
        --trial $trial
done

# Monitor
watch -n 30 "docker ps --filter name=experiment_trial --format 'table {{.Names}}\t{{.Status}}'"

# Wait for all to finish
echo "Waiting for trials to complete..."
while [ "$(docker ps -q --filter name=experiment_trial | wc -l)" -gt 0 ]; do
    sleep 30
done
echo "All trials complete."

# Collect results
for trial in {1..10}; do
    LOG=$(docker logs "experiment_trial_$trial" 2>&1 | tail -5)
    echo "Trial $trial: $LOG"
    docker rm "experiment_trial_$trial" > /dev/null 2>&1
done
```

### Sequence of GPUs

To parallelize across multiple GPUs without conflicts:

```bash
for trial in {1..8}; do
    GPU_ID=$((trial % NUM_GPUS))
    docker run -d \
        --gpus "\"device=$GPU_ID\"" \
        --name "trial_$trial" \
        experiment-runner \
        --trial $trial
done
```

---

## Cleanup Patterns

### Always Clean Up (Prevent Disk Overload)

```bash
# Remove container on exit (--rm flag handles this)
docker run --rm ...

# Manual cleanup of all stopped experiment containers
docker container prune --filter "name=experiment_trial" --force

# Clean dangling images (old builds)
docker image prune --force --filter "until=24h"

# Clean all build cache
docker builder prune --force

# Check disk usage
docker system df
```

### GPU Memory Leak Protection

```bash
# After each trial, verify GPU memory is freed
nvidia-smi --query-gpu=memory.used --format=csv,noheader

# If VRAM isn't released, restart Docker (last resort)
# sudo systemctl restart docker
```

---

## Docker Compose for Multi-Container Campaigns

```yaml
# docker-compose.yml
version: "3.9"

services:
  baseline:
    build: .
    command: --config config/baseline.yaml
    deploy:
      resources:
        limits:
          memory: 8g
          cpus: "4"
    volumes:
      - ./data:/workspace/data:ro
      - ./output:/workspace/output
    environment:
      - CUDA_VISIBLE_DEVICES=0
    shm_size: 4g

  experiment_a:
    build: .
    command: --config config/experiment_a.yaml
    deploy:
      resources:
        limits:
          memory: 16g
          cpus: "8"
    volumes:
      - ./data:/workspace/data:ro
      - ./output:/workspace/output
    environment:
      - CUDA_VISIBLE_DEVICES=1
    shm_size: 8g
    depends_on:
      - baseline
```

```bash
# Run all experiments
docker compose up --abort-on-container-exit

# Run specific experiment
docker compose run experiment_a
```

---

## When Docker Is Not Available

### Conda Environments

```bash
# Create isolated environment
conda create -n experiment_001 python=3.12
conda activate experiment_001
pip install -r requirements.txt

# Remove when done
conda remove -n experiment_001 --all
```

### Virtual Environments

```bash
python3 -m venv .venv_experiment
source .venv_experiment/bin/activate
pip install -r requirements.txt
# ... run experiment ...
deactivate
rm -rf .venv_experiment
```

---

## See Also

- `references/subagent-experiment-supervision.md` — automated failure recovery (works inside containers)
- `references/experimental-campaign-protocol.md` — the campaign workflow
- `scripts/detect-compute.py` — know your hardware before setting limits
