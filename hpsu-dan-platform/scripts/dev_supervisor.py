from __future__ import annotations

import os
import json
import signal
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


load_env_file(ROOT / ".env")

PYTHON = Path(os.environ.get("HPSU_DAN_PYTHON", sys.executable))
RUNTIME_PYTHON = Path(
    r"C:\Users\KMYH\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
)
if RUNTIME_PYTHON.exists():
    PYTHON = RUNTIME_PYTHON
raw_inference_python = os.environ.get("HPSU_DAN_INFERENCE_PYTHON", "").strip()
INFERENCE_PYTHON = Path(raw_inference_python) if raw_inference_python else None
FDD_PYTHON = Path(r"C:\Users\KMYH\miniconda3\envs\fdd\python.exe")
if INFERENCE_PYTHON is None and FDD_PYTHON.exists():
    INFERENCE_PYTHON = FDD_PYTHON
if INFERENCE_PYTHON is None:
    INFERENCE_PYTHON = PYTHON

PID_DIR = ROOT / ".tmp" / "pids"
LOG_DIR = ROOT / "storage"
WEB_PORT = int(os.environ.get("WEB_PORT", os.environ.get("APP_PORT", "8080")))
API_PORT = int(os.environ.get("API_PORT", "8000"))
INFERENCE_PORT = int(os.environ.get("INFERENCE_PORT", "8010"))
EXPECTED_INFERENCE_MODE = os.environ.get("INFERENCE_MODE", "demo").lower()


def env(include_runtime_packages: bool = True) -> dict[str, str]:
    values = os.environ.copy()
    python_paths = [str(ROOT / "packages" / "hpsu_dan_adapter")]
    if include_runtime_packages:
        python_paths.insert(0, str(ROOT / ".python_packages"))
    existing = values.get("PYTHONPATH")
    if existing:
        python_paths.append(existing)
    values["PYTHONPATH"] = os.pathsep.join(python_paths)
    return values


def start_process(name: str, args: list[str], cwd: Path | None = None, include_runtime_packages: bool = True) -> int:
    PID_DIR.mkdir(parents=True, exist_ok=True)
    stdout = (LOG_DIR / f"{name}-dev.out.log").open("ab", buffering=0)
    stderr = (LOG_DIR / f"{name}-dev.err.log").open("ab", buffering=0)
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    proc = subprocess.Popen(
        args,
        cwd=str(cwd or ROOT),
        env=env(include_runtime_packages=include_runtime_packages),
        stdout=stdout,
        stderr=stderr,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
        close_fds=True,
    )
    (PID_DIR / f"{name}.pid").write_text(str(proc.pid), encoding="ascii")
    return proc.pid


def is_healthy(name: str, url: str, timeout: float = 1.5) -> bool:
    try:
        with urlopen(url, timeout=timeout) as response:
            if not (200 <= response.status < 500):
                return False
            if name != "inference":
                return True
            payload = json.loads(response.read().decode("utf-8"))
            if payload.get("engine_mode") != EXPECTED_INFERENCE_MODE:
                return False
            if EXPECTED_INFERENCE_MODE == "real" and not payload.get("model_registered"):
                return False
            return True
    except Exception:
        return False


def stop_port_process(port: int) -> None:
    if os.name != "nt":
        return
    result = subprocess.run(
        ["netstat", "-ano"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    pids: set[str] = set()
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[0].upper() == "TCP" and parts[3].upper() == "LISTENING":
            if parts[1].endswith(f":{port}"):
                pids.add(parts[4])
    for pid in pids:
        subprocess.run(
            ["taskkill", "/PID", pid, "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def start() -> None:
    checks = {
        "inference": f"http://127.0.0.1:{INFERENCE_PORT}/health",
        "api": f"http://127.0.0.1:{API_PORT}/health",
        "web": f"http://127.0.0.1:{WEB_PORT}/health",
    }
    services = {
        "inference": [
            str(INFERENCE_PYTHON),
            "-m",
            "uvicorn",
            "app.main:app",
            "--app-dir",
            str(ROOT / "services" / "inference"),
            "--port",
            str(INFERENCE_PORT),
        ],
        "api": [
            str(PYTHON),
            "-m",
            "uvicorn",
            "app.main:app",
            "--app-dir",
            str(ROOT / "services" / "api"),
            "--port",
            str(API_PORT),
        ],
        "web": [
            str(PYTHON),
            str(ROOT / "scripts" / "static_web_server.py"),
            "--host",
            "0.0.0.0",
            "--port",
            str(WEB_PORT),
        ],
    }
    for name in ("inference", "api", "web"):
        if is_healthy(name, checks[name]):
            print(f"{name} already healthy")
            continue
        if name == "inference":
            stop_port_process(INFERENCE_PORT)
            time.sleep(1)
        cwd = ROOT / "apps" / "web" if name == "web" else ROOT
        print(
            f"Starting {name} pid={start_process(name, services[name], cwd, include_runtime_packages=(name != 'inference'))}"
        )
        time.sleep(1)


def stop() -> None:
    for pid_file in PID_DIR.glob("*.pid"):
        try:
            pid = int(pid_file.read_text(encoding="ascii").strip())
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/PID", str(pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            else:
                os.kill(pid, signal.SIGTERM)
            print(f"Stopped {pid_file.stem} pid={pid}")
        except ProcessLookupError:
            print(f"{pid_file.stem} was not running")
        except Exception as exc:
            print(f"Could not stop {pid_file.stem}: {exc}")
        finally:
            try:
                pid_file.unlink(missing_ok=True)
            except OSError as exc:
                print(f"Could not remove pid file {pid_file}: {exc}")
    for port in (INFERENCE_PORT, API_PORT, WEB_PORT):
        stop_port_process(port)


def health() -> None:
    for name, url in {
        "inference": f"http://127.0.0.1:{INFERENCE_PORT}/health",
        "api": f"http://127.0.0.1:{API_PORT}/health",
        "web": f"http://127.0.0.1:{WEB_PORT}/health",
    }.items():
        try:
            with urlopen(url, timeout=5) as response:
                body = response.read().decode("utf-8")
                print(f"{name}: {response.status} {body[:300]}")
        except Exception as exc:
            print(f"{name}: failed ({exc})")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "start"
    if action == "start":
        start()
    elif action == "stop":
        stop()
    elif action == "health":
        health()
    elif action == "restart":
        stop()
        time.sleep(1)
        start()
    else:
        raise SystemExit(f"Unknown action: {action}")
