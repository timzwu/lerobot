# Setup notes

## Environment

- Machine: macOS (Apple Silicon)
- System Python: 3.13 (Homebrew) — **caveat below**

### Python version

Per the [official install guide](https://huggingface.co/docs/lerobot/installation),
lerobot needs **Python >= 3.12** (and PyTorch >= 2.10). System Python here is 3.13,
but the guide recommends an isolated **Miniforge (conda)** env so you don't touch
Homebrew's Python:

```bash
# Install Miniforge (conda-forge based, open source) — one-time, machine-wide
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash "Miniforge3-$(uname)-$(uname -m).sh"

# Create and activate the env
conda create -y -n lerobot python=3.12
conda activate lerobot   # run this each new shell

# ffmpeg is required for video decoding (TorchCodec)
brew install ffmpeg      # Apple Silicon w/ PyTorch >= 2.10
# fallback if torchcodec complains: conda install ffmpeg=7.1.1 -c conda-forge

pip install lerobot                 # core
# pip install 'lerobot[all]'        # all features
# pip install 'lerobot[feetech]'    # SO100/SO101 motor support
```

Verify the install:

```bash
python -c "import lerobot; print(lerobot.__version__)"
```

## Secrets — don't leak keys

Layered protection so API keys / tokens never land in a commit:

1. **Never hardcode tokens.** Read from env (`os.environ["HF_TOKEN"]`) or a
   gitignored `.env`. Never paste a literal key into code or a notebook.
2. **Authenticate via login commands** — each stores its secret *outside* this repo:
   - `gh auth login` → macOS Keychain
   - `huggingface-cli login` → `~/.cache/huggingface/`
   - `wandb login` → `~/.netrc`
3. **Watch notebooks** — cell outputs are saved JSON. Never `print()` a token; clear
   outputs before committing.
4. **gitleaks pre-commit hook** (`.git/hooks/pre-commit`) scans staged changes and
   blocks any commit containing a detected secret. Bypass a false positive with
   `git commit --no-verify`.
   - Note: this hook is local to this clone (`.git/hooks/` is untracked) — it won't
     follow a fresh `git clone`. Reinstall it, or move to a tracked pre-commit config.

## TODO

- [x] GitHub auth (gh, HTTPS) + gitleaks pre-commit hook
- [ ] Install Miniforge + create the `lerobot` conda env (Python 3.12)
- [ ] Install ffmpeg + lerobot
- [ ] Run a first example / dataset visualization
