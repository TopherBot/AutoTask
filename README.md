# AutoTask

**AutoTask** is a lightweight, zero‑dependency‑ish Python utility that turns a simple `tasks.yaml` file into a powerful command runner. Write a list of shell commands, give each a friendly name, and let AutoTask execute them sequentially while logging output.

---

## Features
- Declarative task definitions in YAML (no code required).
- Automatic logging of stdout/stderr to `autotask.log`.
- Optional dry‑run mode to preview commands.
- Simple, single‑file implementation – perfect for hacking and extending.

---

## Installation
```bash
# Clone the repo and run the script directly (requires Python 3.8+)
git clone https://github.com/yourname/autotask.git
cd autotask
python3 -m pip install --user pyyaml    # optional – only needed for YAML parsing
```

If you want it globally:
```bash
sudo cp autotask.py /usr/local/bin/autotask
chmod +x /usr/local/bin/autotask
```

---

## Usage
1. Create a `tasks.yaml` in the working directory:
```yaml
# tasks.yaml
clean:
  cmd: "rm -rf build/ dist/ *.egg-info"
build:
  cmd: "python -m build"
test:
  cmd: "pytest -q"
```
2. Run AutoTask:
```bash
python3 autotask.py run   # runs all tasks in order
python3 autotask.py run --dry   # shows what would be executed
python3 autotask.py list  # lists available task names
```

---

## Contributing
Feel free to open issues or submit pull‑requests. The project is intentionally tiny, so any improvement that keeps the core simple is welcome.

---

## License
MIT – see the bundled `LICENSE` file.
