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
- **ffmpeg required** (TorchCodec video decoding): installed *into* the env via
  `conda install -c conda-forge ffmpeg` (8.1.2, incl. libsvtav1).
- Install: `pip install 'lerobot[feetech]'` — the Feetech SDK is required (SO-101 uses
  Feetech servos). Installed: **lerobot 0.5.1, torch 2.10.0**.

## Hardware — SO-101 (current state)

Pre-assembled kit → assembly and `lerobot-setup-motors` are **skipped** (motor IDs were
set at the factory). Both arms are **calibrated**; calibration lives in
`~/.cache/huggingface/lerobot/calibration/` and persists across unplugs — do NOT
recalibrate each session.

- Arm ids (use these everywhere — teleop, record, eval): **`follower_arm`**, **`leader_arm`**
- Ports (machine-specific, can change on replug → re-run `lerobot-find-port`):
  follower `/dev/tty.usbmodem5B610339821`, leader `/dev/tty.usbmodem5B3D0414741`
- **⚡ Power: 12V 5A → follower, 5V 4A → leader. Swapping them burns the motors.**
- Flag gotcha: follower uses `--robot.*`, leader uses `--teleop.*`.
- Teleoperation works: `bash scripts/teleop.sh`.
- Long CLI invocations break when pasted into the terminal — **put them in `scripts/`**
  rather than handing Tim wall-of-flags pastes.
- `objc[...] libavdevice ... implemented in both` warnings on macOS are harmless noise.

Next up: workspace (clamp the follower) → camera setup → record first dataset → train
(ACT) → evaluate. See `notes/setup.md` for the full walkthrough and rationale.

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
