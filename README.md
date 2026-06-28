# lerobot — learning & scratch

Personal workspace for self-learning robotics with [HuggingFace LeRobot](https://github.com/huggingface/lerobot).

> Note: this repo is *my own* scratch/learning code. The actual `lerobot` library is
> installed as a dependency — see [Setup](#setup).

## Layout

| Path         | Purpose                                                    |
|--------------|------------------------------------------------------------|
| `scratch/`   | Throwaway experiments, one-off scripts                     |
| `notebooks/` | Jupyter notebooks for exploration                          |
| `notes/`     | Markdown learning notes (concepts, course progress)        |
| `scripts/`   | Reusable utilities worth keeping                           |
| `data/`      | Datasets & artifacts (gitignored — large files live on HF Hub) |

## Setup

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install lerobot (see notes/setup.md for Python-version caveats)
pip install lerobot
```

## Progress

See [`notes/`](notes/) for running notes as I work through the material.
