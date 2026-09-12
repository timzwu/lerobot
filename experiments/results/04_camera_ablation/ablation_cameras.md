# Camera ablation (R6): which camera carries the task? — 2026-09-11

SmolVLA fine-tuned three times on the same 100 pair episodes (50 per task) with the same recipe (20k × 64, 24
passes), differing only in which camera streams the model gets. Same 20 trials each (sync rollout, stickers 1–20,
red→left / blue→right, 30 s).

| cameras | success | 95% interval | red | blue | failure buckets |
|---|---|---|---|---|---|
| overhead + wrist | 9/20 (45%) | 26–66% | 3/10 | 6/10 | touch_no_grip 6, no_reach 3, timeout 1, other 1 |
| overhead only | 4/20 (20%) | 8–42% | 2/10 | 2/10 | touch_no_grip 8, no_reach 8 |
| wrist only | 12/20 (60%) | 39–78% | 7/10 | 5/10 | touch_no_grip 5, no_reach 2, timeout 1 |

Reading: the wrist camera carries the task. Overhead only reaches the right neighbourhood but lands at an offset
and cannot close (the wrist view was doing the last centimetre). Wrist only scores at least as well as both cameras
together (12 vs 9; the intervals overlap, so "adding the overhead view hurt" is not a claim these 20 trials support). What the overhead view
contributes is state: knowing when the task is done (the wrist-only arm wanders and hovers after a successful drop
instead of returning to rest), where the block sits relative to the bowls, and pointing the wrist camera at the
block instead of leaving it to search. Whether it also costs something at this data size is an open question. For a teleop
station this says the cheap wrist camera is the one to keep. Raw trials: `smolvla_toponly_pair.csv`,
`smolvla_wristonly_pair.csv`; geography panels in `failure_geography_ablation.png`.
