# Setup notes

## Environment

- Machine: macOS (Apple Silicon)
- System Python: 3.13 (Homebrew) — **caveat below**

### Python version caveat

LeRobot has historically required **Python 3.10**. If `pip install lerobot` fails
on 3.13, install an older interpreter and point the venv at it:

```bash
brew install python@3.10
python3.10 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install lerobot
```

Verify the install:

```bash
python -c "import lerobot; print(lerobot.__version__)"
```

## TODO

- [ ] Decide Python version (3.10 vs whatever lerobot currently supports)
- [ ] Install lerobot
- [ ] Run a first example / dataset visualization
