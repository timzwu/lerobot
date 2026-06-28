# CLAUDE.md

Agent-facing context for this repo. Terse and actionable. Growing over time —
add relevant context, themes, and conventions as the project evolves.

## What this repo is

Tim's personal **scratch/learning workspace** for self-learning robotics with
HuggingFace LeRobot. This is *not* a fork of `huggingface/lerobot` — the `lerobot`
library is a dependency. Code here is experiments and notes, not a shipped product.

## Layout

- `scratch/` — throwaway experiments, one-off scripts
- `notebooks/` — Jupyter exploration
- `notes/` — human-facing learning notes & the *why* behind decisions (see `notes/setup.md`)
- `scripts/` — reusable utilities worth keeping
- `data/` — datasets/artifacts, **gitignored** (large files live on HF Hub)

## Environment

- macOS (Apple Silicon). System Python is 3.13, but **lerobot needs Python >= 3.12**
  (PyTorch >= 2.10) per the official install guide.
- Use conda (Miniforge): env name `lerobot`, Python 3.12. Activate with
  `conda activate lerobot` before running anything.
- **ffmpeg required** (TorchCodec video decoding): `brew install ffmpeg`, or
  `conda install ffmpeg=7.1.1 -c conda-forge` if torchcodec complains.
- Install: `pip install lerobot` inside that env (extras: `lerobot[all]`, `[feetech]`, …).

## Secrets — never commit a key

- Never hardcode tokens; read from env or a gitignored `.env`.
- Authenticate via login commands (secrets stored outside the repo): `gh auth login`
  (Keychain), `huggingface-cli login` (`~/.cache/huggingface/`), `wandb login` (`~/.netrc`).
- Notebooks leak via saved cell outputs — never `print()` a token; clear outputs before commit.
- A **gitleaks pre-commit hook** (`.git/hooks/pre-commit`) blocks commits containing
  secrets. It is local-only (untracked) — won't survive a fresh clone.

## Git / GitHub

- Remote: `github.com/timzwu/lerobot` (account `timzwu`), HTTPS via `gh` credential helper.
- Default branch `main`. Commit/push only when Tim asks.

## Conventions & themes

<!-- Add learning themes, recurring decisions, and project context here as we go. -->
