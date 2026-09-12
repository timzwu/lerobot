# SmolVLA, 100 episodes (pair only) — four-task pass, 2026-09-09

Same checkpoint as `smolvla100_pair.md` (trained on red→left and blue→right only, 50 demos each; it never saw a
red→right or blue→left demo). 20 trials cycling all four combos, sync rollout, 30 s of motion each.

| combo | demos in training | success |
|---|---|---|
| red→left | 50 | 3/5 |
| blue→right | 50 | 4/5 |
| red→right | 0 | 1/5 |
| blue→left | 0 | 2/5 |
| all | | 10/20 (50%, 95% Wilson interval 30–70%) |

Trained combos 7/10, in line with the pair pass (9/20). Untrained combos 3/10, and all three successes went to
the bowl the instruction named; there were no wrong-bowl outcomes in the pass. So the language input steers the
policy even for instructions it never trained on, about a third of the time; a color-only policy (ACT) cannot do
this by construction. Failures were the usual grasp misses (touch_no_grip 5, no_reach 4, drop 1).

Next comparison: the same recipe trained on all 150 episodes (25 demos of each crossed task) to see how much
those 25 demos add over zero-shot instruction following. Raw trials: `smolvla100_all4.csv`.
