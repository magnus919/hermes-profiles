#!/usr/bin/env python3
"""
detect-compute.py — Probe hardware and software environment for ML feasibility.

Outputs structured recommendations so the agent can self-constrain its approach
based on available compute. Run before any experiment campaign to determine
what model sizes, batch sizes, and techniques are feasible.

Usage:
  python detect-compute.py                # Pretty-printed system overview
  python detect-compute.py --json          # Machine-readable JSON output
  python detect-compute.py --minimal       # Only the recommendations object
  python detect-compute.py --verbose       # Show every probe and its result
  python detect-compute.py --list-gpus     # Quick GPU inventory only

Exit codes:
  0 — Success
  1 — Probe completed but with warnings or degraded environment
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import warnings

# ── Argument parsing ──────────────────────────────────────────────
FLAGS = {
    "json": False,
    "minimal": False,
    "verbose": False,
    "list_gpus": False,
}

for arg in sys.argv[1:]:
    if arg == "--json":
        FLAGS["json"] = True
    elif arg == "--minimal":
        FLAGS["minimal"] = True
    elif arg == "--verbose":
        FLAGS["verbose"] = True
    elif arg == "--list-gpus":
        FLAGS["list_gpus"] = True
    elif arg in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)


# ── Probe functions ───────────────────────────────────────────────

def _run(cmd: list[str], timeout: int = 15) -> tuple[str, str, int]:
    """Run a subprocess, return (stdout, stderr, exit_code)."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.stdout.strip(), proc.stderr.strip(), proc.returncode
    except FileNotFoundError:
        return "", f"command not found: {cmd[0]}", -1
    except subprocess.TimeoutExpired:
        return "", f"timed out after {timeout}s", -1


def _nvidia_smi() -> dict:
    """Parse nvidia-smi for GPU inventory. Returns empty dict if unavailable."""
    stdout, _, rc = _run(["nvidia-smi", "--query-gpu=index,name,memory.total,compute_cap",
                          "--format=csv,noheader,nounits"])
    if rc != 0:
        return {}

    gpus = []
    for line in stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(", ")]
        if len(parts) >= 4:
            try:
                gpus.append({
                    "index": int(parts[0]),
                    "name": parts[1],
                    "vram_mb": int(float(parts[2])),
                    "compute_capability": parts[3],
                })
            except (ValueError, IndexError):
                continue

    if not gpus:
        return {}

    # Get driver version
    drv_stdout, _, _ = _run(["nvidia-smi", "--query-gpu=driver_version",
                             "--format=csv,noheader,nounits"])
    driver_version = drv_stdout.strip().split("\n")[0].strip() if drv_stdout else ""

    return {"gpu_count": len(gpus), "gpus": gpus, "driver_version": driver_version}


def _cuda_version() -> str:
    """Detect CUDA version from nvcc or nvidia-smi."""
    stdout, _, rc = _run(["nvcc", "--version"])
    if rc == 0:
        for line in stdout.split("\n"):
            if "release" in line:
                parts = line.split("release ")
                if len(parts) > 1:
                    return parts[1].split(",")[0].strip()
    # Fallback: try nvidia-smi topo
    stdout, _, _ = _run(["nvidia-smi"])
    for line in stdout.split("\n"):
        if "CUDA Version:" in line:
            return line.split("CUDA Version:")[-1].strip()
    return ""


def _torch_info() -> dict:
    """Probe PyTorch availability and capabilities via subprocess."""
    probe = r"""
import json, sys
try:
    import torch
    info = {
        "available": True,
        "version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count() if hasattr(torch.cuda, 'device_count') else 0,
        "mps_available": getattr(torch.backends, 'mps', None) is not None and torch.backends.mps.is_available(),
        "cuda_version": torch.version.cuda if hasattr(torch.version, 'cuda') else None,
    }
    if info["cuda_available"] and info["cuda_device_count"] > 0:
        info["current_device"] = torch.cuda.current_device()
        props = torch.cuda.get_device_properties(0)
        info["gpu_name"] = props.name
        info["vram_total_mb"] = props.total_memory // (1024 * 1024)
    print(json.dumps(info))
except Exception as e:
    print(json.dumps({"available": False, "error": str(e)}))
"""
    stdout, _, rc = _run([sys.executable, "-c", probe])
    if rc != 0 or not stdout:
        return {"available": False}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"available": False}


def _sklearn_info() -> dict:
    """Probe scikit-learn availability and version."""
    probe = r"""
import json, sys
try:
    import sklearn
    print(json.dumps({"available": True, "version": sklearn.__version__}))
except Exception as e:
    print(json.dumps({"available": False, "error": str(e)}))
"""
    stdout, _, rc = _run([sys.executable, "-c", probe])
    if rc != 0 or not stdout:
        return {"available": False}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"available": False}


def _get_ram_mb() -> int:
    """Get total physical RAM in MB."""
    try:
        import psutil
        return psutil.virtual_memory().total // (1024 * 1024)
    except ImportError:
        pass
    # Fallback: /proc/meminfo on Linux
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    return kb // 1024
    except (FileNotFoundError, ValueError, IndexError):
        pass
    # Fallback: sysctl on macOS
    stdout, _, _ = _run(["sysctl", "-n", "hw.memsize"])
    if stdout:
        try:
            return int(stdout.strip()) // (1024 * 1024)
        except ValueError:
            pass
    return 0


def _get_disk_free_mb(path: str = ".") -> int:
    """Get free disk space at path in MB."""
    try:
        import shutil
        _, _, free = shutil.disk_usage(path)
        return free // (1024 * 1024)
    except (ImportError, FileNotFoundError):
        pass
    # Fallback: df on Unix
    stdout, _, _ = _run(["df", "-P", path])
    for line in stdout.split("\n")[1:]:
        parts = line.strip().split()
        if len(parts) >= 4:
            try:
                return int(parts[3])  # Free in KB → convert
            except ValueError:
                pass
    return 0


def _has_jax() -> bool:
    """Check if JAX is available."""
    stdout, _, rc = _run([sys.executable, "-c", "import jax; print(jax.__version__)"])
    return rc == 0 and bool(stdout.strip())


def _has_optuna() -> bool:
    """Check if Optuna is available."""
    stdout, _, rc = _run([sys.executable, "-c", "import optuna; print(optuna.__version__)"])
    return rc == 0 and bool(stdout.strip())


# ── Recommendation engine ────────────────────────────────────────

def _recommendations(info: dict) -> dict:
    """Generate actionable recommendations based on detected hardware."""
    recs = {}
    vram_mb = 0

    # Get VRAM from the most reliable source
    torch_avail = info.get("torch", {}).get("available", False)
    if torch_avail and info["torch"].get("vram_total_mb"):
        vram_mb = info["torch"]["vram_total_mb"]
    elif info.get("nvidia", {}).get("gpus"):
        vram_mb = info["nvidia"]["gpus"][0].get("vram_mb", 0)

    has_cuda = info.get("nvidia", {}).get("gpu_count", 0) > 0
    has_torch = torch_avail
    has_sklearn = info.get("sklearn", {}).get("available", False)

    # Model size tier
    if vram_mb >= 24000:
        recs["model_size_tier"] = "13B-70B"
        recs["feasible_techniques"] = ["full_fine_tuning", "lora", "qlora", "distillation"]
    elif vram_mb >= 16000:
        recs["model_size_tier"] = "7B-13B"
        recs["feasible_techniques"] = ["full_fine_tuning", "lora", "qlora", "distillation"]
    elif vram_mb >= 8000:
        recs["model_size_tier"] = "3B-7B"
        recs["feasible_techniques"] = ["lora", "qlora", "distillation"]
        recs["notes"] = "Full fine-tuning may be tight for 7B. Prefer LoRA/QLoRA."
    elif vram_mb >= 4000:
        recs["model_size_tier"] = "up_to_3B"
        recs["feasible_techniques"] = ["qlora", "distillation"]
        recs["notes"] = "Full fine-tuning only for models <= 1.5B. Use QLoRA for larger."
    elif has_cuda:
        recs["model_size_tier"] = "up_to_1B"
        recs["feasible_techniques"] = ["qlora", "cpu_offloading"]
        recs["notes"] = "Limited VRAM. Consider cloud GPU or CPU-based methods."
    else:
        recs["model_size_tier"] = "cpu_only"
        recs["feasible_techniques"] = ["sklearn", "xgboost", "lightgbm"]
        recs["notes"] = "No GPU detected. Use sklearn/xgboost/lightgbm. No deep learning."

    # Batch size guidance
    if vram_mb >= 24000:
        recs["batch_size_guide"] = "LoRA: 128, Full FT: 32, Inference: 4096"
    elif vram_mb >= 16000:
        recs["batch_size_guide"] = "LoRA: 64, Full FT: 16, Inference: 2048"
    elif vram_mb >= 8000:
        recs["batch_size_guide"] = "LoRA: 32, Full FT: 8, Inference: 1024"
    elif vram_mb >= 4000:
        recs["batch_size_guide"] = "LoRA: 16, Full FT: 4, Inference: 512"
    elif has_cuda:
        recs["batch_size_guide"] = "LoRA: 8, Full FT: 2, Inference: 256"
    else:
        recs["batch_size_guide"] = "CPU-based. Batch size less relevant — use sklearn pipelines."

    # Quantization guidance
    if vram_mb >= 8000:
        recs["quantization_available"] = ["int8", "fp4", "fp8"]
    elif vram_mb >= 4000:
        recs["quantization_available"] = ["int8", "fp4"]
    elif has_cuda:
        recs["quantization_available"] = ["int8"]
    else:
        recs["quantization_available"] = []

    # Distillation
    recs["distillation_feasible"] = has_torch and vram_mb >= 4000

    # Fallback if no deep learning at all
    if not has_torch and not has_sklearn:
        recs["notes"] = "Neither PyTorch nor scikit-learn detected. Install: pip install torch scikit-learn"
    elif not has_torch and has_sklearn:
        recs["notes"] = recs.get("notes", "") + " PyTorch not found. sklearn/xgboost available."
    elif has_torch and not has_sklearn:
        recs["notes"] = recs.get("notes", "") + " scikit-learn not found. PyTorch available."

    return recs


# ── Main probe ────────────────────────────────────────────────────

def run_probes() -> dict:
    """Run all hardware and software probes, return structured results."""
    info = {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "python_executable": sys.executable,
        "platform": sys.platform,
        "platform_detail": platform.platform(),
        "hostname": platform.node(),
    }

    # NVIDIA GPU probe
    nvidia = _nvidia_smi()
    info["nvidia"] = nvidia
    info["has_cuda"] = nvidia.get("gpu_count", 0) > 0
    info["cuda_version"] = _cuda_version() if info["has_cuda"] else None

    if FLAGS["verbose"] and info["has_cuda"]:
        info["_nvidia_smi_raw"] = _run(["nvidia-smi"])[0]

    # Torch
    info["torch"] = _torch_info()

    # sklearn
    info["sklearn"] = _sklearn_info()

    # JAX
    info["has_jax"] = _has_jax()

    # Optuna
    info["has_optuna"] = _has_optuna()

    # System resources
    ram_mb = _get_ram_mb()
    info["ram_mb"] = ram_mb
    info["ram_gb"] = round(ram_mb / 1024, 1) if ram_mb else 0

    disk_free_mb = _get_disk_free_mb()
    info["disk_free_mb"] = disk_free_mb
    info["disk_free_gb"] = round(disk_free_mb / 1024, 1) if disk_free_mb else 0

    # Recommendations
    info["recommendations"] = _recommendations(info)

    return info


def _format_verbose(info: dict) -> str:
    """Produce verbose human-readable output."""
    lines = []

    def kv(k: str, v: object) -> None:
        lines.append(f"  {k}: {v}")

    lines.append("── System ──────────────────────────────")
    kv("Python", info["python_version"])
    kv("Platform", info["platform"])
    kv("Host", info["hostname"])

    lines.append("\n── GPU ─────────────────────────────────")
    if info["has_cuda"]:
        for gpu in info["nvidia"]["gpus"]:
            kv(f"GPU {gpu['index']}", f"{gpu['name']} ({gpu['vram_mb']} MB VRAM, CC {gpu['compute_capability']})")
        kv("CUDA", info["cuda_version"] or "unknown")
        kv("Driver", info["nvidia"].get("driver_version", "unknown"))
    else:
        lines.append("  (none detected)")

    lines.append("\n── ML Frameworks ───────────────────────")
    t = info["torch"]
    if t.get("available"):
        kv("PyTorch", t["version"])
        kv("  CUDA avail", t.get("cuda_available", False))
        kv("  MPS avail", t.get("mps_available", False))
        if t.get("gpu_name"):
            kv("  Torch GPU", f"{t['gpu_name']} ({t.get('vram_total_mb', '?')} MB)")
    else:
        kv("PyTorch", "not installed")

    s = info["sklearn"]
    if s.get("available"):
        kv("scikit-learn", s["version"])
    else:
        kv("scikit-learn", "not installed")

    kv("JAX", "yes" if info["has_jax"] else "no")
    kv("Optuna", "yes" if info["has_optuna"] else "no")

    lines.append("\n── Resources ───────────────────────────")
    kv("RAM", f"{info['ram_gb']} GB" if info["ram_gb"] else "unknown")
    kv("Disk free", f"{info['disk_free_gb']} GB" if info["disk_free_gb"] else "unknown")

    lines.append("\n── Recommendations ─────────────────────")
    for k, v in info["recommendations"].items():
        lines.append(f"  {k}: {v}")

    return "\n".join(lines)


# ── Entry point ──────────────────────────────────────────────────

def main():
    info = run_probes()

    # Handle --list-gpus (fast path)
    if FLAGS["list_gpus"]:
        if info["has_cuda"]:
            for gpu in info["nvidia"]["gpus"]:
                print(f"GPU {gpu['index']}: {gpu['name']} ({gpu['vram_mb']} MB)")
        else:
            print("No NVIDIA GPUs detected")
        return

    # Handle output formats
    if FLAGS["json"]:
        if FLAGS["minimal"]:
            print(json.dumps(info["recommendations"], indent=2))
        else:
            print(json.dumps(info, indent=2, default=str))
    elif FLAGS["minimal"]:
        print(json.dumps(info["recommendations"], indent=2))
    elif FLAGS["verbose"]:
        print(_format_verbose(info))
    else:
        # Default: pretty human-readable, recommendations-focused
        print(json.dumps(info, indent=2, default=str))


if __name__ == "__main__":
    main()
