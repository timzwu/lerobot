# Week 1 comparison: ACT vs SmolVLA vs π0.5 on the same 100 episodes

Two tasks, 50 demos each (red→left, blue→right), same 20 trials per model (stickers 1–20, alternating task,
30 s), same failure buckets. "Passes" = steps × batch ÷ ~54k frames.

| model | recipe | passes | rollout | success | 95% interval | red | blue | most common failure | failure buckets |
|---|---|---|---|---|---|---|---|---|---|
| ACT, from scratch | 20k × 8 | 3 | local, 100-step chunks | 1/20 (5%) | 1–24% | 0/10 | 1/10 | reaches the block, closes early or beside it, then retries in place until time runs out | touch_no_grip 12, no_reach 4, collision 2, drop 1 |
| ACT, from scratch | 100k × 8 (LeRobot default) | 15 | local, 100-step chunks | 4/20 (20%) | 8–42% | 3/10 | 1/10 | touches the block but the jaws land a few mm off; several blue trials hover mid-mat and never commit | touch_no_grip 9, no_reach 6, drop 1 |
| SmolVLA, fine-tuned from smolvla_base | 20k × 64 (LeRobot default) | 24 | sync on the Mac, 50-step chunks | 9/20 (45%) | 26–66% | 3/10 | 6/10 | missed first grasp then a retry that lands slightly off; recoveries do succeed (2) | touch_no_grip 6, no_reach 3, timeout 1, other 1 |
| π0.5, fine-tuned from pi05_base (vision frozen, action expert only) | 40k × 32 (matched to SmolVLA's passes) | 24 | sync via a Modal server, 50-step chunks | 5/20 (25%) | 11–47% | 2/10 | 3/10 | reaches and touches the block but the jaws land beside it or close a moment early; almost never adjusts once there | touch_no_grip 11, no_reach 4 |

Caveats stated up front: SmolVLA starts from a model pretrained on SO-100 data, a head start ACT doesn't get;
ACT at 3 passes is a fifth of its default recipe (the 15-pass row is the fair one); every rollout is
look-then-commit, ACT every 3.3 s, SmolVLA every 1.7 s with a 0.8 s think pause, π0.5 every 1.85 s with a 1–2.5 s pause
(the round trip to the GPU on Modal). π0.5's fine-tune froze the same parts as SmolVLA's (vision encoder frozen, action
expert trained), so the recipes match; what differs is what the frozen parts had seen before (SmolVLA: SO-100/101
community data; π0.5: Physical Intelligence's own robots, no SO-101) and the picture each model gets (π0.5 224×224 per
camera, SmolVLA 512×512). Model chart: `model_comparison.png`.

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

## Instruction following

`smolvla100_all4.md`: the pair-trained SmolVLA on all four combos. Trained combos 7/10; untrained combos 3/10,
every success to the bowl the words named, no wrong-bowl failures. Zero-shot instruction following is real but
weak at this scale; the 150-episode run will show what 25 demos per crossed task add.

π0.5 on the same four-combo pass (`pi05.md`): 2/20, trained combos 1/10, untrained 1/10, again no wrong-bowl failure.
Too few successes to say anything about its instruction following; the grasp fails before the bowl choice matters.

## Failure geography

`failure_geography_wk1.png` (on the overhead photo, solid circles) and `failure_geography_wk1_abstract.png` (smoothed success/failure
field per model, red to blue, plus a fifth panel combining the three pair runs): the 20 stickers, four panels (ACT 20k, ACT 100k, SmolVLA pair,
SmolVLA all-four with untrained combos starred), green = success, orange = reached but no grip / dropped /
collision, red = never reached. Sticker pixel positions in `sticker_map.json`.
First read: SmolVLA's successes sit in the upper and middle rows (far from the arm base) and its failures at
the bottom row (nearest the base) and the two top corners; ACT-100k's four successes are all in the bottom
row. Ten trials per row is too few to call either a pattern yet.

π0.5 vs SmolVLA maps: `failure_geography_pi05.png`. π0.5's five pair successes are spread (center 3/10, edge 2/10) with no
region it owns; SmolVLA's sit in the upper-middle (center 7/10, edge 2/10).

Raw data: one row per trial across all passes in `all_trials_wk1.csv` (sticker, task, outcome, failure bucket,
notes, timestamp, checkpoint); per-pass CSVs alongside.

## Scaling sweep (2026-09-11)

SmolVLA at 10 / 25 / 50 / 100 episodes of the pair, same recipe, same 20 trials: 0 / 1 / 8 / 9 of 20. Blind
prediction before the sweep: 0 / 1 / 4. Plot `scaling.png`; per-checkpoint geography `failure_geography_sweep.png`;
details and reading in `scaling_predictions.md`. Short version: nothing works below ~12 demos per task, the jump
is between 12 and 25 per task, and 25 → 50 per task added one success, inside the noise.

## Camera ablation (R6)

See `ablation_cameras.md`: both cameras 9/20, overhead only 4/20, wrist only 12/20. The wrist camera carries the grasp; the overhead view supplies state (done, relative position, where to look). Wrist alone is at least as good as both within 20-trial error.

## Geography, quantified (2026-09-11)

Pooling five SmolVLA pair passes (100 trials): the ten stickers nearest the zone's center succeed 50% of the time,
the ten nearest the edges 18%, and the four corners 0 of 5 each. Distance from the arm base makes no difference
(26% near, 31% far), so it is not reach length. Coverage explains about half of it: counting training starts
within ~45 px of each sticker, the low-coverage half of the stickers scores 22% and the high-coverage half 46%
(correlation 0.49). The exceptions are informative: stickers 14 and 1, on the bottom edge next to the base, have
plenty of nearby demos and still score 0 of 5, so the bottom edge is hard for the arm itself (the wrist has to
fold under). Lesson for the next dataset: place blocks deliberately at the edges and corners, since random
placement under-samples them, and expect the base-side edge to stay hard regardless.

## Open questions after week 1

- Does success keep rising past 50 demos per task with more varied data, as the papers suggest, or is this task
  saturated at 9/20 for reasons of precision rather than quantity?
- When does the overhead camera earn its place? Probably with more data, and probably with tasks that need state
  the wrist can't see: e.g. placing several colored blocks in a given order, where the sequence lives in the
  overhead view.
- A matched-passes sweep (same passes over the data at every subset size), since the fixed-step sweep over-trains
  the small subsets.
- The crossed tasks with real demos: the run on all 150 episodes, versus the 3/10 zero-shot instruction following.
- The deliberate recovery episodes in R2 look like the cheapest good decision of the week (SmolVLA's second-try
  grasps); a controlled test would train with and without them.

## Progress scoring (2026-09-11)

Every trial scored by the stage it reached: 0 never reached the block, 1 touched it but never closed on it,
2 grasped it then dropped / collided / ran out of time, 3 success. Same idea as π0.5's task-progress rubric.
Plot: `progress_by_model.png`.

| model | never reached | reached, no grip | grasped, lost | success | mean progress / 3 |
|---|---|---|---|---|---|
| ACT, 100 ep, 3 passes | 4 | 12 | 3 | 1 | 1.05 |
| ACT, 100 ep, 15 passes | 6 | 9 | 1 | 4 | 1.15 |
| SmolVLA, 10 ep | 15 | 4 | 1 | 0 | 0.30 |
| SmolVLA, 25 ep | 10 | 8 | 1 | 1 | 0.65 |
| SmolVLA, 50 ep | 6 | 6 | 0 | 8 | 1.50 |
| SmolVLA, 100 ep | 3 | 7 | 1 | 9 | 1.80 |
| SmolVLA, 100 ep, overhead only | 8 | 8 | 0 | 4 | 1.00 |
| SmolVLA, 100 ep, wrist only | 2 | 5 | 1 | 12 | 2.15 |
| π0.5, 100 ep, 24 passes | 4 | 11 | 0 | 5 | 1.30 |

Reading: the scaling curve is smoother in progress than in success (0.30 → 0.65 → 1.50 → 1.80): the 25-episode
model had mostly learned to reach, which the 1/20 headline hides. ACT's extra training moved trials from "no
grip" to success without changing how many never reached. Cameras: wrist-only fails less at every stage, not just
the last one, which argues the wrist view helps the approach as well as the grasp; overhead-only's extra failures
are in the first two stages. The middle stage, grasped then lost, is small everywhere: once these models close on
the block they usually finish, so the bottleneck is closing on it. π0.5 makes the point most sharply: it reaches the block
as often as SmolVLA (16/20 vs 17/20 got past stage 0) and converts 5 of those 16 touches into a grasp where SmolVLA converts
10 of 17.

Regenerate every chart with `python experiments/plot_results.py` (stage rules and the one notes-based override live there).

## Execution method (2026-09-11)

`smolvla100_rtc.md`: the 100-episode SmolVLA run stop-and-go scored 9/20; the same checkpoint under LeRobot's
Real-Time Chunking scored 3/20, with more back-and-forth near the block and two grasps that opened again. RTC
enforces agreement between consecutive chunks; when the policy's chunks disagree, that locks in the wrong plan.
Not part of the model comparison. Execution in the model rows: ACT ran through LeRobot's real-time rollout (one 100-step
chunk every 3.3 s, it is fast enough to run live); SmolVLA and π0.5 ran through our stop-and-go loop (`sync_rollout.py`)
because their inference is too slow per step, SmolVLA on the Mac, π0.5 on a Modal GPU. Each step is paced to 30 Hz;
with recording on (π0.5 passes) the measured rate was 27 Hz, close to the ~27 Hz the SmolVLA passes ran at under the
earlier loop (which slept a full frame after each command). Think pauses never count toward the 30 s of motion.

## π0.5 (2026-09-12)

Same 100 episodes, matched passes, same 20 trials, `pi05.md`: 5/20 on the trained pair, 2/20 on the four-combo pass.
Below SmolVLA (9/20, 10/20) and about level with ACT at its default recipe (4/20). The failure is the grasp: it reaches
and touches the block on 16 of 20 trials and then leaves the jaws a few millimetres off, or closes a beat early, and it
rarely adjusts once there.

Hypotheses, in the order we'd test them:
- Embodiment. Both fine-tunes trained only the action expert on top of frozen perception. SmolVLA's frozen parts had
  been pretrained on SO-100/101 data; π0.5's had never seen this arm, so its expert had to learn the arm from 100
  episodes through features that don't know it. The "big, general" model is general to other robots.
- Picture size. π0.5 shrinks each camera to 224×224 before looking, SmolVLA to 512×512. At 224 the block edge on the
  wrist camera is a few pixels at grasp distance, and the last two centimetres are exactly where π0.5 fails. Test:
  a bigger block, or the wrist camera mounted closer.
- Not latency. The arm is stationary while the model thinks, so the picture is never stale; the gripper drifting away
  before closing is the 50-step open-loop chunk, which SmolVLA shares.
- Frozen backbone. Unfreezing the vision tower (or full fine-tuning on a bigger GPU) is the direct test of the first
  hypothesis; PI's own recipes fine-tune more of the model than we did.
