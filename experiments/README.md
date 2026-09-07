# experiments/

Imitation learning on a $200 arm, measured honestly. One task, three policies, one scaling curve.

**Setup:** SO-101 follower + leader arm, overhead and wrist cameras at 640x480, a cutting mat with a taped
randomization zone, 20 numbered dot stickers as fixed eval positions, two bowls.

**Task:** "put the [red|blue] block in the [left|right] bowl."

**Questions**
1. On one task with ~50 teleop demos, does a pretrained vision-language-action model (SmolVLA, pi0.5)
   beat a small policy trained from scratch (ACT)?
2. How does success scale with demos: 10 / 25 / 50 / 100 episodes, nested subsets, same eval?
3. Is the wrist camera worth it? Same data, wrist stream excluded.

**Eval protocol:** 20 fixed positions, one trial each, 30 s per trial, same positions for every model.
Outcome + failure type per trial. With N=20 the 95% interval at 50% success is roughly +/-22 points,
so results are reported with intervals, not point estimates.

## Files

| File | What | Runs where |
|---|---|---|
| `modal_hello.py` | Prove Modal auth, billing, and GPU work | Modal |
| `modal_train.py` | `lerobot-train` on Modal (ACT / SmolVLA / pi0.5); checkpoints on a Volume | Modal |
| `sweep.py` | Data-scaling sweep: nested seeded episode subsets trained in parallel | Modal |
| `eval.py` | 20-position eval protocol -> `results/<name>.csv` + summary with 95% Wilson CI | Mac |
| `robot.json` | Ports, arm ids, cameras for this rig | Mac |
| `results/` | CSVs, comparison tables, plots | - |

## Dry run on public data

Proves dataset -> Modal -> checkpoint -> Mac before any of our own data exists.

```bash
# 1. ACT, 2000 steps, on lerobot/svla_so101_pickplace (50 eps, cameras up+side, red cube -> gray bowl)
modal run --detach experiments/modal_train.py --steps 2000 --batch-size 8
# 2. parallel sweep launches (tiny)
modal run experiments/sweep.py::sweep --sizes 5,10 --steps 200 --policy act --batch-size 8
# 3. pull the checkpoint (exact command is printed at the end of step 1; plain `modal volume get` on
#    checkpoints/last fails because `last` is a symlink and the dir may hold a stray .tmp save file)
modal run experiments/modal_train.py::pull --job-name act_svla_so101_pickplace_2000
# 4. load it on the Mac
python -c "from lerobot.policies.act.modeling_act import ACTPolicy; p=ACTPolicy.from_pretrained('experiments/checkpoints/act_svla_so101_pickplace_2000'); print(p.config)"
```

## Real runs

```bash
# record (dataset is created private; flip to public in the repo settings later)
lerobot-record ... --dataset.repo_id=$HF_USER/so101_blocks --dataset.private=true --dataset.single_task="put the red block in the left bowl"

export HF_TOKEN=...   # so Modal can read the private dataset
modal run --detach experiments/modal_train.py --dataset $HF_USER/so101_blocks --policy act --steps 20000
modal run --detach experiments/modal_train.py --dataset $HF_USER/so101_blocks --policy smolvla --steps 20000 --batch-size 64 --gpu L40S
modal run --detach experiments/sweep.py::sweep --dataset $HF_USER/so101_blocks --policy smolvla --sizes 10,25,50,100 --steps 20000 --batch-size 64 --gpu L40S

# eval: ACT locally; VLAs through async inference (policy server on a GPU, Mac as client)
python experiments/eval.py --mode local --name act_50 --policy experiments/checkpoints/<job>
python experiments/eval.py --mode async --name smolvla_50 --policy-type smolvla --policy <hub-id> --server <host:port>
python experiments/eval.py --summary experiments/results/act_50.csv
```

Notes
- Modal Volumes: `lerobot-hf-cache` (datasets, base models), `lerobot-outputs` (checkpoints). `modal volume ls lerobot-outputs`.
- `HF_TOKEN` is also needed for gated models (pi0.5 uses the PaliGemma tokenizer; accept its license on the Hub).
- Camera ablation: decide the mechanism (`--rename_map` / `--policy.empty_cameras` / a dataset copy without the wrist key) once the real camera keys exist.
- `results/` is committed; `checkpoints/` is not.
