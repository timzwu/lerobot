# ACT, 100 episodes (50 per task), 20,000 steps — trained-pair eval, 2026-09-08

Checkpoint `act_so101_blocks_20000_ep0-49_100-149` (3 passes over the data). Local rollout on the Mac,
full 100-step chunks, no temporal ensembling. 20 trials, stickers 1–20, alternating red→left / blue→right.

| result | count |
|---|---|
| success | 1 / 20 (5%, 95% Wilson interval 1–24%) |
| reached block, never closed on it | 12 |
| never reached block | 4 |
| grasped, hit bowl rim | 2 |
| grasped, dropped | 1 |

By task: blue→right 1/10, red→left 0/10. Reaching works ~80% of the time; the grasp is the failure.

Probes on the same checkpoint (not scored): re-planning every 10 or 25 steps on the Mac dropped the control
loop to 13–15 Hz and the arm crept; async inference through the Modal policy server oscillated in place, with
the 5°/step clamp firing at chunk seams (raising it to 15° did not help). Reading: consecutive chunks disagree,
i.e. undertrained. Next: same checkpoint continued to 100,000 steps (LeRobot default), same 20 trials.
Raw trials: `act100_pair.csv`.
