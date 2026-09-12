# Execution-method experiment: stop-and-go vs Real-Time Chunking, same checkpoint — 2026-09-11

Checkpoint `smolvla_so101_blocks_n100_s0` (SmolVLA, 100 pair episodes, 24 passes), run two ways on the same 20
trials (stickers 1–20, red→left / blue→right, 30 s, Mac GPU):

| execution | success | 95% interval | red | blue | failure buckets |
|---|---|---|---|---|---|
| stop-and-go: one 50-step chunk, execute it, look again (~0.8 s pause) | 9/20 (45%) | 26–66% | 3/10 | 6/10 | touch_no_grip 6, no_reach 3, timeout 1, other 1 |
| Real-Time Chunking (LeRobot `--inference.type=rtc`, horizon 10, guidance 10): next chunk computed during the current one, inpainted to agree with the committed prefix | 3/20 (15%) | 5–36% | 1/10 | 2/10 | touch_no_grip 11, no_reach 4, drop 2 |

What it looked like (Tim's notes): motion continuous with no pauses, but a lot of back-and-forth and repeated
gripper open/close near the block; twice the arm grasped the block and then let go as the next chunk pulled it
toward the earlier plan. Stop-and-go would have seen the block already in the jaws and lifted.

Reading: RTC assumes consecutive chunks are consistent; it makes the new chunk agree with the old one. When the
policy's own chunks disagree, which ours do near the block, that consistency constraint keeps the arm faithful to
a plan that was already wrong, and the fluid motion has nothing precise to carry. For the record: the Mac's ~0.8 s inference froze about
24 of each 50-step chunk, settings were LeRobot's defaults, and the safety clamp still fired at times; none of
these is the main story. The paper's Skeptic question ("does inpainting smooth the motion or lock in the mistake on a
weaker model?") got its answer here: on this model, it locks in the mistake. Raw trials: `smolvla100_rtc_pair.csv`.
