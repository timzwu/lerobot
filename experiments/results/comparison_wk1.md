# Week 1 comparison: ACT vs SmolVLA on the same 100 episodes

Two tasks, 50 demos each (red→left, blue→right), same 20 trials per model (stickers 1–20, alternating task,
30 s), same failure buckets. "Passes" = steps × batch ÷ ~54k frames.

| model | recipe | passes | rollout | success | 95% interval | red | blue | most common failure | failure buckets |
|---|---|---|---|---|---|---|---|---|---|
| ACT, from scratch | 20k × 8 | 3 | local, 100-step chunks | 1/20 (5%) | 1–24% | 0/10 | 1/10 | reaches the block, closes early or beside it, then retries in place until time runs out | touch_no_grip 12, no_reach 4, collision 2, drop 1 |
| ACT, from scratch | 100k × 8 (LeRobot default) | 15 | local, 100-step chunks | 4/20 (20%) | 8–42% | 3/10 | 1/10 | touches the block but the jaws land a few mm off; several blue trials hover mid-mat and never commit | touch_no_grip 9, no_reach 6, drop 1 |
| SmolVLA, fine-tuned from smolvla_base | 20k × 64 (LeRobot default) | 24 | sync on the Mac, 50-step chunks | 9/20 (45%) | 26–66% | 3/10 | 6/10 | missed first grasp then a retry that lands slightly off; recoveries do succeed (2) | touch_no_grip 6, no_reach 3, timeout 1, other 1 |

Caveats stated up front: SmolVLA starts from a model pretrained on SO-100 data, a head start ACT doesn't get;
ACT at 3 passes is a fifth of its default recipe (the 15-pass row is the fair one); both rollouts are
look-then-commit, ACT every 3.3 s, SmolVLA every 1.7 s with a 0.8 s think pause.

## Reading (2026-09-09)

- Training length matters for ACT: 3 → 15 passes took it from 1/20 to 4/20, with more reaches landing. The grasp
  is still where it fails.
- The pretrained model wins at this data size: SmolVLA fine-tuned from a base that had seen SO-100 arms scored
  9/20 against ACT's 4/20 at each library's default recipe. Intervals overlap (8–42% vs 26–66%), so 20 trials
  says "likely better," not "certainly better."
- Both fail the same way, at the grasp; SmolVLA recovers from a missed grasp more often (two recoveries
  succeeded), which the recovery episodes in R2 were meant to teach.
- Color split flips between models (ACT red 3 / blue 1; SmolVLA red 3 / blue 6); with 10 trials per color, no
  conclusion yet. Failure-geography plot pending.

## Instruction following (SmolVLA only)

`smolvla100_all4.md`: the pair-trained SmolVLA on all four combos. Trained combos 7/10; untrained combos 3/10,
every success to the bowl the words named, no wrong-bowl failures. Zero-shot instruction following is real but
weak at this scale; the 150-episode run will show what 25 demos per crossed task add.

## Failure geography

`failure_geography_wk1.png` (on the overhead photo, solid circles) and `failure_geography_wk1_abstract.png` (smoothed success/failure
field per model, red to blue, plus a fifth panel combining the three pair runs): the 20 stickers, four panels (ACT 20k, ACT 100k, SmolVLA pair,
SmolVLA all-four with untrained combos starred), green = success, orange = reached but no grip / dropped /
collision, red = never reached. Sticker pixel positions in `sticker_map.json`.
First read: SmolVLA's successes sit in the upper and middle rows (far from the arm base) and its failures at
the bottom row (nearest the base) and the two top corners; ACT-100k's four successes are all in the bottom
row. Ten trials per row is too few to call either a pattern yet.

Raw data: one row per trial across all four passes in `all_trials_wk1.csv` (sticker, task, outcome, failure bucket,
notes, timestamp, checkpoint); per-pass CSVs alongside.
