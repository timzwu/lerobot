# ACT, 100 episodes (50 per task), 100,000 steps — trained-pair eval, 2026-09-09

Checkpoint `act_so101_blocks_100000_ep0-49_100-149` (continued from the 20k checkpoint; 15 passes over the data,
LeRobot's default length). Local rollout on the Mac, full 100-step chunks, no temporal ensembling. 20 trials,
stickers 1–20, alternating red→left / blue→right, 30 s each. Wrist servo horn tightened and wrist camera
remounted between the SmolVLA pair pass and this one (camera view verified against training frames).

| result | count |
|---|---|
| success | 4 / 20 (20%, 95% Wilson interval 8–42%) |
| reached block, never closed on it | 9 |
| never reached block | 6 |
| grasped, dropped at the bowl rim | 1 |

By task: red→left 3/10, blue→right 1/10. Versus the same model at 20k steps (1/20): more reaches land, the grasp is
still the failure, and several blue trials hover mid-mat and never commit. Raw trials: `act100k_pair.csv`.
