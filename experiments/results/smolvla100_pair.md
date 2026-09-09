# SmolVLA, 100 episodes (50 per task), 20,000 × 64 — trained-pair eval, 2026-09-09

Checkpoint `smolvla_so101_blocks_n100_s0`, fine-tuned from `lerobot/smolvla_base` (24 passes over the data).
Synchronous chunked rollout on the Mac (`sync_rollout.py`): predict a 50-step chunk (~0.8 s), execute it,
repeat. 20 trials, stickers 1–20, alternating red→left / blue→right, 30 s of motion each.

| result | count |
|---|---|
| success | 9 / 20 (45%, 95% Wilson interval 26–66%) |
| reached block, never closed on it | 6 |
| never reached block | 3 |
| timeout (returned to rest without the block, then re-tried too late) | 1 |
| other (edge grip launched the block off the table) | 1 |

By task: blue→right 6/10, red→left 3/10. Two successes were recoveries (missed grasp, second attempt worked);
several failures showed the same retry behaviour without landing it. Grasps along the block's edges succeeded
twice and failed once. Hypothesis to test (Tim): red does worse because the left bowl is pinkish, so a red
block near it is harder to separate from the bowl in the overhead view; the right bowl is green and blue stands
out. To do: plot successes and failures on the sticker map per model and task (failure geography), and consider an orange block for the next dataset.

Same checkpoint through the LeRobot async server twitched at rest (see `training_runs.md` notes); the sync
rollout is the eval path until that is fixed. Raw trials: `smolvla100_pair.csv`.
