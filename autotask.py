#!/usr/bin/env python3
"""AutoTask – a tiny YAML‑driven task runner.

Features:
- Read ``tasks.yaml`` from the current directory.
- ``run``   – execute all tasks in the order they appear.
- ``list``  – print available task names.
- ``--dry`` – preview commands without executing.

The script is deliberately simple: no external CLI frameworks, only the
standard library plus optional ``pyyaml`` for a nicer YAML experience.
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime

# Try to import yaml; fall back to a very tiny parser if unavailable.
try:
    import yaml
    _HAS_YAML = True
except ImportError:  # pragma: no cover
    _HAS_YAML = False
    import re
    def yaml_load(s):
        """Very limited YAML loader – works for ``key: value`` pairs only.
        This is only to keep the script runnable without extra deps.
        """
        data = {}
        for line in s.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r"^(?P<key>[^:]+):\s*\"?(?P<val>[^\"]*)\"?$", line)
            if m:
                data[m.group('key').strip()] = {'cmd': m.group('val').strip()}
        return data

LOG_FILE = "autotask.log"

def log(message: str) -> None:
    timestamp = datetime.now().isoformat(timespec='seconds')
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def load_tasks(path: str = "tasks.yaml") -> dict:
    if not os.path.exists(path):
        sys.stderr.write(f"Error: {path} not found.\n")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    if _HAS_YAML:
        try:
            data = yaml.safe_load(raw) or {}
        except yaml.YAMLError as e:
            sys.stderr.write(f"YAML parsing error: {e}\n")
            sys.exit(1)
    else:
        data = yaml_load(raw)
    # Validate structure
    for name, cfg in data.items():
        if not isinstance(cfg, dict) or "cmd" not in cfg:
            sys.stderr.write(f"Invalid task definition for '{name}'. Expected {{'cmd': '...'}}.\n")
            sys.exit(1)
    return data

def run_task(name: str, cmd: str, dry: bool) -> None:
    log(f"Task '{name}' started.")
    print(f"[{'DRY' if dry else 'RUN'}] {name}: {cmd}")
    if dry:
        log(f"Task '{name}' skipped (dry run).")
        return
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        # Log stdout and stderr
        if result.stdout:
            log(f"{name} stdout: {result.stdout.strip()}")
        if result.stderr:
            log(f"{name} stderr: {result.stderr.strip()}")
        if result.returncode != 0:
            log(f"Task '{name}' failed with exit code {result.returncode}.")
            sys.stderr.write(f"Task '{name}' failed (exit {result.returncode}).\n")
            sys.exit(result.returncode)
        else:
            log(f"Task '{name}' completed successfully.")
    except Exception as e:  # pragma: no cover
        log(f"Task '{name}' raised exception: {e}")
        sys.stderr.write(f"Error running task '{name}': {e}\n")
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="AutoTask – tiny YAML driven task runner.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    run_parser = subparsers.add_parser("run", help="Execute all tasks in order.")
    run_parser.add_argument("--dry", action="store_true", help="Show commands without executing.")

    subparsers.add_parser("list", help="List defined task names.")

    args = parser.parse_args()
    tasks = load_tasks()

    if args.action == "list":
        print("Available tasks:")
        for name in tasks:
            print(f" - {name}")
        return

    if args.action == "run":
        for name, cfg in tasks.items():
            run_task(name, cfg["cmd"], dry=args.dry)
        print("All tasks completed. See 'autotask.log' for details.")

if __name__ == "__main__":
    main()
