# Scaling sweep: predictions before results (written 2026-09-09, before the sweep was launched)

SmolVLA fine-tuned on nested subsets of the two-task pool (red→left, blue→right), same recipe (20k × 64), same
20-trial eval on the trained pair.

| episodes (per task) | predicted successes / 20 | measured |
|---|---|---|
| 10 (5) | 0 | 0 (no_reach 15, touch_no_grip 4, drop 1) |
| 25 (12) | 1 | 1 (no_reach 10, touch_no_grip 8, drop 1) |
| 50 (25) | 4 | |
| 100 (50) | — | 9 (measured first, 2026-09-09) |

Prediction: Tim. The 100 point was known when the guesses were made; the shape below it was not. Reasoning: success
probably scales superlinearly with demos at this range, so the low end should be near zero; the one way 10 or 25
episodes could score is if the SmolVLA base model already carries most of the skill from its SO-100 pretraining,
which would show up as a flat curve rather than a rising one.
