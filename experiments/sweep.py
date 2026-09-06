"""Data-scaling sweep: train the same policy on nested, seeded episode subsets, in parallel on Modal.

Subsets are nested (the 10 are inside the 25, inside the 50, inside the 100) from one seeded shuffle,
so the curve measures "more of the same data", not different data.

Dry run on the public dataset (50 episodes), tiny steps, just to prove parallel launch:
    modal run experiments/sweep.py::sweep --sizes 5,10 --steps 200

Real sweep on your own dataset:
    modal run experiments/sweep.py::sweep --dataset $HF_USER/so101_blocks --policy smolvla \
        --sizes 10,25,50,100 --steps 20000 --batch-size 64 --gpu L40S

Writes experiments/results/sweep_<policy>_<seed>.json (the subsets + job names + results) so eval.py and
the plot know exactly which episodes each checkpoint saw. Add `--dry-run` to print commands only.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import modal  # noqa: E402

from modal_train import DEFAULT_DATASET, DEFAULT_GPU, app, build_argv, pull_command, train  # noqa: E402

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def dataset_num_episodes(repo_id: str) -> int:
    """Read total_episodes from meta/info.json on the Hub without downloading the dataset."""
    from urllib.request import urlopen

    url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/meta/info.json"
    with urlopen(url, timeout=30) as r:  # noqa: S310
        return int(json.load(r)["total_episodes"])


def nested_subsets(total: int, sizes: list[int], seed: int) -> dict[int, list[int]]:
    order = list(range(total))
    random.Random(seed).shuffle(order)
    return {n: sorted(order[:n]) for n in sizes}


@app.local_entrypoint()
def sweep(
    dataset: str = DEFAULT_DATASET,
    policy: str = "smolvla",
    sizes: str = "10,25,50,100",
    steps: int = 20000,
    batch_size: int = 64,
    gpu: str = DEFAULT_GPU,
    seed: int = 0,
    tag: str = "",
    dry_run: bool = False,
):
    wanted = [int(s) for s in sizes.split(",") if s.strip()]
    total = dataset_num_episodes(dataset)
    usable = [n for n in wanted if n <= total]
    skipped = [n for n in wanted if n > total]
    if skipped:
        print(f"[sweep] dataset has {total} episodes; skipping sizes {skipped}")
    if not usable:
        raise SystemExit("[sweep] nothing to run")

    subsets = nested_subsets(total, usable, seed)
    name = dataset.split("/")[-1]
    jobs = {n: f"{policy}_{name}_n{n}_s{seed}{('_' + tag) if tag else ''}" for n in usable}

    manifest = {
        "dataset": dataset,
        "policy": policy,
        "seed": seed,
        "steps": steps,
        "batch_size": batch_size,
        "gpu": gpu,
        "subsets": {str(n): subsets[n] for n in usable},
        "jobs": {str(n): jobs[n] for n in usable},
        "results": {},
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = RESULTS_DIR / f"sweep_{policy}_{name}_s{seed}{('_' + tag) if tag else ''}.json"

    argvs = {n: build_argv(dataset, policy, jobs[n], steps, batch_size, episodes=subsets[n]) for n in usable}
    for n in usable:
        print(f"[sweep] n={n:>3} job={jobs[n]} episodes={subsets[n]}")
        print("        lerobot-train", " ".join(argvs[n]))
    if dry_run:
        manifest_path.write_text(json.dumps(manifest, indent=2))
        print(f"[sweep] dry run; manifest at {manifest_path}")
        return

    fn = train if gpu == DEFAULT_GPU else train.with_options(gpu=gpu)
    handles = {n: fn.spawn(argvs[n], jobs[n]) for n in usable}  # all sizes train at once
    print(f"[sweep] launched {len(handles)} jobs on {gpu}; waiting...")

    for n, h in handles.items():
        try:
            res = h.get()
        except Exception as e:  # one failure shouldn't hide the others
            res = {"job_name": jobs[n], "returncode": -1, "error": repr(e)}
        manifest["results"][str(n)] = {k: v for k, v in res.items() if k != "tail"}
        status = "ok" if res.get("returncode") == 0 else f"FAILED rc={res.get('returncode')}"
        print(f"[sweep] n={n:>3} {status} {res.get('elapsed_min', '?')} min")
        if res.get("tail"):
            print(res["tail"])
        manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"\n[sweep] manifest: {manifest_path}")
    print("[sweep] pull checkpoints with:")
    for n in usable:
        if manifest["results"].get(str(n), {}).get("returncode") == 0:
            print("  " + pull_command(jobs[n]))
