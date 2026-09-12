# Scaling sweep: predictions before results (written 2026-09-09, before the sweep was launched)

SmolVLA fine-tuned on nested subsets of the two-task pool (red→left, blue→right), same recipe (20k × 64), same
20-trial eval on the trained pair.

| episodes (per task) | predicted successes / 20 | measured |
|---|---|---|
| 10 (5) | 0 | 0 (no_reach 15, touch_no_grip 4, drop 1) |
| 25 (12) | 1 | 1 (no_reach 10, touch_no_grip 8, drop 1) |
| 50 (25) | 4 | 8 (touch_no_grip 6, no_reach 6) |
| 100 (50) | — | 9 (measured first, 2026-09-09) |

Prediction: Tim. The 100 point was known when the guesses were made; the shape below it was not. Reasoning: success
probably scales superlinearly with demos at this range, so the low end should be near zero; the one way 10 or 25
episodes could score is if the SmolVLA base model already carries most of the skill from its SO-100 pretraining,
which would show up as a flat curve rather than a rising one.

## Result (2026-09-11)

Measured: 0, 1, 8, 9 of 20 for 10, 25, 50, 100 episodes. Predicted 0, 1, 4. The low end was right; the jump came
earlier than guessed, between 25 and 50 episodes (12 → 25 per task), and 50 → 100 added one success, inside the
noise of 20 trials. Plot: `scaling.png`. Reading: at this task the model needs on the order of 25 demos per task
to work at all, and doubling past that bought little; the failures that remain (grasp offsets) look like a
different problem from "not enough demos". Same recipe at every size, so the small subsets were over-trained
(≈240 passes at 10 episodes); a matched-passes sweep would be the next question.
