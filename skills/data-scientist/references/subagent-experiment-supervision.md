# Subagent Experiment Supervision

**When to load this reference:** Running a multi-experiment campaign (Phase 4-7 of the experimental protocol) and want automated failure recovery without manual intervention. Requires a subagent-capable harness (Hermes `delegate_task`, OpenCode subagents, or similar).

---

## Architecture

```
┌───────────────────────────────────────────────────┐
│                  Orchestrator                     │
│  (responsible for the overall experiment campaign) │
└────┬──────────────┬──────────────────┬────────────┘
     │              │                  │
     ▼              ▼                  ▼
┌──────────┐ ┌──────────┐     ┌──────────────┐
│ Worker 1 │ │ Worker 2 │ ... │ Supervisor   │
│ Runner   │ │ Runner   │     │ (one per     │
│          │ │          │     │  experiment) │
└──────────┘ └──────────┘     └──────┬───────┘
                                     │ watches logs
                                     │ auto-fixes
                                     │ escalates
```

**Key insight:** The supervisor is not a separate process. It's a lightweight monitoring loop that runs *alongside* the experiment, checking logs and applying known fixes. The orchestrator spawns one supervisor per experiment worker.

---

## Supervision Loop

```python
import re
import time
import subprocess
from pathlib import Path

FAILURE_PATTERNS = {
    "cuda_oom": {
        "pattern": r"CUDA out of memory",
        "fix": "reduce_batch_size",
        "priority": 1,
    },
    "cpu_oom": {
        "pattern": r"MemoryError|Cannot allocate memory",
        "fix": "reduce_memory",
        "priority": 2,
    },
    "nan_loss": {
        "pattern": r"loss.*nan|Loss.*NaN|nan.*loss",
        "fix": "gradient_clipping",
        "priority": 3,
    },
    "import_error": {
        "pattern": r"ModuleNotFoundError|ImportError.*No module named",
        "fix": "pip_install",
        "priority": 4,
    },
    "cuda_mismatch": {
        "pattern": r"CUDA error.*no kernel image|CUDA driver error",
        "fix": "fallback_cpu",
        "priority": 5,
    },
    "disk_full": {
        "pattern": r"No space left on device|Disk quota exceeded",
        "fix": "clean_disk",
        "priority": 6,
    },
    "timeout": {
        "pattern": r"TIMEOUT|killed|SIGTERM|SIGKILL",
        "fix": "reduce_scope",
        "priority": 7,
    },
}
```

### Supervisor Function

```python
def supervise_experiment(
    experiment_cmd: list,
    log_path: Path,
    max_retries: int = 3,
    check_interval: float = 5.0,
    timeout_hours: float = 24,
) -> dict:
    """
    Run an experiment with automated failure recovery.

    Args:
        experiment_cmd: Command to run (e.g., ["python", "train.py", "--config", "x.yaml"])
        log_path: Path to capture logs
        max_retries: Max consecutive auto-fix attempts before escalation
        check_interval: How often to check for errors (seconds)
        timeout_hours: Max wall time before considering the experiment hung

    Returns:
        Dict with status ("success", "fixed", "escalated", "timeout"), logs, fix_history
    """
    fix_history = []
    log_path.parent.mkdir(parents=True, exist_ok=True)
    start_time = time.time()

    for attempt in range(max_retries + 1):
        with open(log_path, "w") as log_file:
            process = subprocess.Popen(
                experiment_cmd,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
            )

            # Monitoring loop
            while True:
                # Check for timeout
                elapsed = (time.time() - start_time) / 3600
                if elapsed > timeout_hours:
                    process.kill()
                    return {
                        "status": "timeout",
                        "log_path": str(log_path),
                        "elapsed_hours": elapsed,
                    }

                # Check if process finished
                retcode = process.poll()
                if retcode is not None:
                    if retcode == 0:
                        return {
                            "status": "success" if attempt == 0 else "fixed",
                            "fix_history": fix_history,
                            "log_path": str(log_path),
                            "attempts": attempt,
                        }
                    break  # Process failed — try to diagnose

                time.sleep(check_interval)

        # Process failed — check logs for known patterns
        log_text = log_path.read_text()
        fix = diagnose_failure(log_text)

        if fix is None:
            # Unknown failure — escalate
            return {
                "status": "escalated",
                "log_path": str(log_path),
                "fix_history": fix_history,
                "error_snippet": log_text[-2000:],
            }

        # Apply fix
        fix_result = apply_fix(fix, experiment_cmd)
        fix_history.append({"attempt": attempt, "fix": fix, "result": fix_result})
        print(f"  [supervisor] Applied fix: {fix}")
```

### Failure Diagnosis

```python
def diagnose_failure(log_text: str) -> str | None:
    """Check logs against known failure patterns. Returns fix name or None."""
    for name, info in sorted(FAILURE_PATTERNS.items(), key=lambda x: x[1]["priority"]):
        if re.search(info["pattern"], log_text, re.IGNORECASE):
            return info["fix"]
    return None
```

---

## Failure Catalog with Fixes

| Signature | Detection (log pattern) | Fix |
|---|---|---|
| **CUDA OOM** | `CUDA out of memory` in stderr | Reduce `batch_size` by 50%, re-run |
| **CPU OOM** | `MemoryError` or system OOM killer | Halve data loading. Use `--data-fraction 0.5`. Re-run. |
| **NaN loss** | `loss: nan` or `Loss is NaN` or `nan in loss` | Add gradient clipping (`max_norm=1.0`). Reduce LR by 10x. Check for NaN in input data. Re-run. |
| **ImportError** | `ModuleNotFoundError: No module named 'X'` | `pip install X` and re-run |
| **CUDA version mismatch** | `CUDA error: no kernel image is available` or `CUDA driver version is insufficient` | Fall back to CPU: set `CUDA_VISIBLE_DEVICES=""` and re-run. Log the constraint. |
| **Disk full** | `No space left on device` or `Disk quota exceeded` | Clean temp files (`rm -rf /tmp/*.pt /tmp/__pycache__`). Alert user if < 1GB free. |
| **Timeout / Hung** | Process exceeds expected wall time with no log output for 30+ minutes | Kill process. Re-run with `--max-epochs 5 --max-steps 1000` (reduced scope). |
| **OOM during data loading** | `RuntimeError: DataLoader worker` + OOM | Reduce `num_workers` to 0. Set `persistent_workers=False`. Re-run. |
| **cuDNN init error** | `cuDNN error: CUDNN_STATUS_NOT_INITIALIZED` | Restart with fresh CUDA context. `torch.cuda.empty_cache()`. Re-run. |
| **Checkpoint corruption** | `RuntimeError: Error(s) in loading state_dict` | Remove corrupted checkpoint, restart from last known good epoch. |

---

## Fix Implementations

### Fix: Reduce Batch Size

```python
def fix_reduce_batch_size(cmd: list) -> list:
    """Modify command to use half the batch size."""
    new_cmd = cmd[:]
    for i, arg in enumerate(new_cmd):
        if arg == "--batch-size" or arg == "--batch_size":
            try:
                current = int(new_cmd[i + 1])
                new_cmd[i + 1] = str(max(1, current // 2))
                return new_cmd
            except (ValueError, IndexError):
                break
    # If no batch-size flag, append one
    new_cmd.extend(["--batch_size", "16"])
    return new_cmd
```

### Fix: Gradient Clipping

```python
def fix_gradient_clipping(cmd: list) -> list:
    """Add gradient clipping to the command."""
    if "--grad_clip" not in cmd and "--gradient-clip" not in cmd:
        cmd.extend(["--grad_clip", "1.0"])
    return cmd
```

### Fix: Reduce Scope (for timeouts)

```python
def fix_reduce_scope(cmd: list) -> list:
    """Limit epochs and data for a quick smoke test."""
    cmd.extend(["--max-epochs", "5", "--data-fraction", "0.1", "--quick-test"])
    return cmd
```

### Fix: Fall Back to CPU

```python
def fix_fallback_cpu(cmd: list) -> list:
    """Set environment to disable CUDA."""
    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    return cmd  # Same command, but CUDA is now invisible
```

### Fix: Install Missing Package

```python
def fix_pip_install(log_text: str) -> str:
    """Extract missing module name from ImportError and install it."""
    match = re.search(
        r"ModuleNotFoundError: No module named '([^']+)'",
        log_text
    )
    if match:
        module = match.group(1)
        import subprocess
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", module],
            capture_output=True,
        )
        return f"installed {module}"
    return "unknown"
```

---

## Escalation Path

When 3 consecutive auto-fixes fail (or the supervisor encounters an unknown error):

1. **Save experiment context** — log file, fix history, snapshot of current state
2. **Send notification** to the user via Telegram (or configured alert channel)
3. **Include enough context** for the user to make a decision:

> **⚠️ Experiment supervision escalation**
>
> Experiment `run_007` failed after 3 auto-fix attempts.
>
> Last fix tried: `reduce_batch_size` (batch 64 → 32) — still OOM on a 24GB GPU.
>
> Next steps available:
> 1. Try gradient checkpointing (--gradient-checkpoint)
> 2. Use CPU offloading (--cpu-offload)
> 3. Abort this experiment, move to next candidate
>
> Log snippet: .../experiments/logs/run_007.log (last 50 lines attached)

**Telegram notification pattern** (when available):
```
python3 -c "
import urllib.request, json
urllib.request.urlopen(
    'https://api.telegram.org/bot<TOKEN>/sendMessage',
    data=json.dumps({
        'chat_id': '<CHAT_ID>',
        'text': '<message>',
        'parse_mode': 'Markdown'
    }).encode()
)
"
```

If Telegram is not configured, fall back to writing escalation to a file and continuing with the next experiment. The orchestrator should check for escalation files at the end of the campaign.

---

## Integration with the Campaign Protocol

### When to Use Supervision

| Protocol Phase | Supervision Value |
|---|---|
| Phase 2 (Baselines) | Low — baselines are fast enough to re-run manually |
| Phase 4 (Moonshots) | **High** — these are the most likely to fail |
| Phase 5 (Transfer Learning) | Medium — download failures, size mismatches |
| Phase 6 (HP Search) | **High** — 100+ trials, many will fail |
| Phase 7 (Distillation) | Medium — complex loss functions, convergence issues |

### What the Orchestrator Does

```python
# Pseudocode for the orchestrator's experiment loop
results = []
for candidate in shortlist:
    for trial in range(num_trials):
        supervisor = spawn_supervisor(
            experiment_cmd=["python", "train.py", "--config", candidate.config],
            log_path=f"logs/{candidate.name}_trial_{trial}.log",
        )
        result = supervisor.run()
        results.append(result)
        if result["status"] == "escalated":
            notify_user(result)
            # Continue with other candidates while waiting
```

---

## Harness-Specific Implementation Notes

### Hermes Agent (delegate_task)

```python
# The supervisor is spawned as a delegate_task that monitors the experiment
from hermes_tools import delegate_task  # if available

# Or: The orchestrator runs inline with subprocess monitoring
import subprocess, time

def run_supervised(experiment_cmd, log_path, max_retries=3):
    """Simple supervised experiment runner without subagent framework."""
    for attempt in range(max_retries + 1):
        with open(log_path, "w") as f:
            proc = subprocess.Popen(experiment_cmd, stdout=f, stderr=subprocess.STDOUT)

        while True:
            retcode = proc.poll()
            if retcode is not None:
                if retcode == 0:
                    return {"status": "success", "log_path": str(log_path)}
                break
            time.sleep(5)

        # Diagnose and fix (see functions above)
        log_text = Path(log_path).read_text()
        fix = diagnose_failure(log_text)
        if fix is None:
            return {"status": "escalated", "log_path": str(log_path)}
        experiment_cmd = apply_fix(fix, experiment_cmd)

    return {"status": "escalated", "log_path": str(log_path)}
```

### OpenCode / Claude Code

These harnesses don't have `delegate_task` but can use subprocess-based supervision. The same pattern applies — the agent runs the experiment as a subprocess and reads its logs periodically.

---

## Limitations

| Limitation | Mitigation |
|---|---|
| Only catches known failure patterns | The failure catalog is extensible — add patterns as you encounter them |
| Some fixes require code changes, not just CLI flags | For complex failures (architectural bugs), escalate immediately |
| Distributed training failures are more complex | DDP failures often require restarting the entire process group |
| Supervisor consumes monitoring overhead | Negligible (< 0.1% GPU) for the check_interval=5s pattern |
| Can't fix fundamental problems (bad architecture, wrong loss) | Escalate those — no auto-fix can rescue a fundamentally wrong approach |

---

## See Also

- `references/experimental-campaign-protocol.md` — the campaign workflow this supports
- `references/docker-experiment-isolation.md` — running experiments in containers
- `scripts/detect-compute.py` — know your hardware limits before scheduling
