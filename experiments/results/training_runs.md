# Training runs

Every run that started a GPU, with what it saw and what it cost. Loss curves (every 100 steps) are in
`training_loss.csv`. Costs are A10G at ~$1.10/h unless noted. Costs before Sept 12 are GPU-only: Modal also bills CPU and RAM (about $0.32/h per card), so the true bill is 10–30% higher; the launcher's estimates include it from Sept 12. Dataset `so101_blocks` is private on the Hub
until the footage is reviewed.

| date (UTC) | job | policy | data | per task | steps × batch | passes over data | GPU | wall | cost | loss start → end | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-06 | act_svla_so101_pickplace_2000 | ACT from scratch | public `lerobot/svla_so101_pickplace`, 50 ep | 50 | 2,000 × 8 | 1.3 | A10G | 6.2 min | $0.18 | 1.9 → 1.15 | pipeline dry run; cameras `up`/`side`, never driven |
| 2026-09-08 | act_so101_test_r1_…_2000 | ACT from scratch | 5 test episodes (deleted) | 5 | 2,000 × 8 | 4.2 | A10G | 6.2 min | $0.19 | 10.1 → 1.17 | smoke test: trainer accepts `top`/`wrist` keys |
| 2026-09-08 | act_so101_blocks_20000_ep0-49 | ACT from scratch (ResNet-18 ImageNet backbone) | `so101_blocks` ep 0–49: red→left, blue→right | 25 | 20,000 × 8 | 5.7 | A10G | 55.3 min | ≈$1.01 | 9.9 → 0.18 (l1 0.16 at the end) | shakedown on sticker 1: reaches toward the block, jerky, no grasp, returns |
| 2026-09-08 | act_so101_blocks_20000_ep0-49_100-149 | ACT from scratch (ResNet-18 ImageNet backbone) | `so101_blocks` ep 0–49 + 100–149: red→left, blue→right | 50 | 20,000 × 8 | ~2.9 | A10G | 55.3 min | ≈$1.01 | 10.0 → 0.19 (l1 0.17 at the end) | same steps as ACT-50, so the only difference is data; R3 eval checkpoint |
| 2026-09-09 | smolvla_so101_blocks_n100_s0 | SmolVLA fine-tune from `lerobot/smolvla_base` (cameras renamed top→camera1, wrist→camera2) | `so101_blocks` ep 0–49 + 100–149: red→left, blue→right | 50 | 20,000 × 64 | ~23 | L40S | 176.8 min | ≈$5.75 | see note | LeRobot default recipe; loss curve not captured (client detached, Modal CLI keeps only the log tail); final loss 0.027, 24 passes |
| 2026-09-09 | act_so101_blocks_100000_ep0-49_100-149 (attempt 1) | ACT continued from the 20k checkpoint | same 100 episodes | 50 | +80,000 × 8 planned | — | A10G | 164 min, killed at step 57,558 | ≈$3.00, nothing saved | — | died when the launching terminal was closed (`.remote()` under `modal run --detach` does not survive); saved only at the end. Fixed: spawn + `--save-freq 10000` |
| 2026-09-09 | act_so101_blocks_100000_ep0-49_100-149 | ACT continued from the 20k checkpoint (LeRobot default length) | same 100 episodes | 50 | +80,000 × 8 (100k total) | 15 total | A10G | ~3.75 h | ≈$4.10 | 0.19 → 0.118 | spawn-safe launch, checkpoints every 10k; the Mac client hit a DNS blip at the end and the run was unaffected; R3 eval checkpoint |
| 2026-09-10 | smolvla_so101_blocks_n10_s0 | SmolVLA fine-tune (sweep) | 10 episodes of the pair (5 per task), balanced | 5 | 20,000 × 64 | ~240 | L40S | 194 min | ≈$6.30 | → 0.01-class (over-fit by design: fixed steps) | scaling sweep point; input shape patched to 480x640 after training |
| 2026-09-10 | smolvla_so101_blocks_n25_s0 | SmolVLA fine-tune (sweep) | 25 episodes of the pair (12/13 per task) | 12 | 20,000 × 64 | ~95 | L40S | 196 min | ≈$6.40 | → 0.013 | container restarted mid-run (Modal preemption); second attempt wrote to a timestamp-suffixed folder; final checkpoint pulled from there |
| 2026-09-10 | smolvla_so101_blocks_n50_s0 | SmolVLA fine-tune (sweep) | 50 episodes of the pair (25 per task) | 25 | 20,000 × 64 | ~48 | L40S | ~195 min | ≈$6.30 | (log tail lost) | scaling sweep point |
| 2026-09-10 | smolvla_nowrist_n100 | SmolVLA fine-tune, OVERHEAD camera only (R6 ablation) | `so101_blocks_nowrist` ep 0–49 + 100–149 | 50 | 20,000 × 64 | ~24 | L40S | 111 min | ≈$3.60 | → 0.032 | wrist stream removed with `lerobot-edit-dataset remove_feature`; rename top→camera1 |
| 2026-09-10 | smolvla_notop_n100 | SmolVLA fine-tune, WRIST camera only (R6 ablation) | `so101_blocks_notop` ep 0–49 + 100–149 | 50 | 20,000 × 64 | ~24 | L40S | 110 min | ≈$3.60 | → 0.028 | overhead stream removed; rename wrist→camera1 |
| 2026-09-11 | pi05_fit_trial | π0.5 fine-tune, fit trial (backbone frozen, action expert only, bf16, grad checkpointing) | same 100 pair episodes | 50 | 200 × 32 | 0.1 | A100-80GB | 12.3 min incl. 14.5 GB model download | ≈$0.50 (+ two failed starts ≈$0.30: gated PaliGemma license, then a rename-map mismatch) | 0.25 → 0.19 | 18.7 GB, 3.07 s/step; output deleted |
| 2026-09-11 | pi05_so101_blocks_40000_ep0-49_100-149 (attempt 1) | π0.5 fine-tune, matched to SmolVLA (24 passes) | same 100 pair episodes | 50 | 40,000 × 32 planned | — | H100 | 6.0 h, killed at step 18,112 by the launcher's 6 h function timeout | ≈$24 (≈$9 lost past the 10k checkpoint) | 0.25 → 0.059 at 15k | 10k checkpoint + full training state saved; resumed exactly (attempt 2) |
| 2026-09-12 | pi05_so101_blocks_40000_ep0-49_100-149 (attempt 2, resumed from 10k) | π0.5 fine-tune, matched to SmolVLA (24 passes) | same 100 pair episodes | 50 | 40,000 × 32 | 24 | H100 | 9.9 h for steps 10k→40k (1.18 s/step); ~13.2 h of H100 in total across both attempts | ≈$41 this leg (≈$65 total incl. attempt 1; GPU-only) | 0.25 → 0.049 | full training state resumed exactly; checkpoints every 10k; the old launcher wrote this leg to a `-20260911-221316` suffixed folder (bug fixed Sept 12); R7 eval checkpoint |
| 2026-09-12 | pi05_2card_trial | π0.5 fine-tune, 2-card trial (accelerate launch, DDP) | same 100 pair episodes | 50 | 200 × 32 (16 per card) | 0.1 | 2 × H100 | 5.4 min incl. weight load; 0.66 s/step steady state | ≈$0.80 | 0.25 → 0.19 | first multi-card run: global batch confirmed (checkpoint stores num_processes 2, per-card batch 16; 32 samples/step); 1.77x faster than one H100 = 0.88 per-card scaling, now the launcher's estimate constant; output deleted |

## Comparison design (fixed 2026-09-08, before results)

- **Task pair.** Both models train on the same 100 episodes: 50 of "put the red block in the left bowl" and
  50 of "put the blue block in the right bowl" (episodes 0–49 and 100–149 of `so101_blocks`). ACT cannot read
  a task string, so a dataset where the same picture maps to two bowls would be unlearnable for it; the pair is
  a rule it can learn from color. The 50 crossed episodes (red→right, blue→left) are used only for an
  instruction-following pass on models that read language.
- **Recipe.** Each model on its library's documented default: ACT 100,000 steps × batch 8; SmolVLA 20,000 steps
  × batch 64 fine-tuned from `lerobot/smolvla_base`. Steps are not comparable across batch sizes, so the unit
  is passes over the data (steps × batch ÷ ~54k frames): ACT 15, SmolVLA 23. SmolVLA also starts from a model
  pretrained on SO-100 data, which is a head start the table must state, not hide.
- **Eval.** Identical 20 trials for every model: stickers 1–20, alternating red→left / blue→right, 30 s each,
  success plus a failure bucket by stage (never reached / reached, no grip / dropped / collision / other),
  Wilson 95% interval. Models that read an instruction get a second 20-trial pass cycling all four tasks.
- **What each result would mean.** ACT@3 passes → ACT@15 passes isolates training length. ACT@15 vs SmolVLA@23
  is the model comparison at the papers' data floor (50 demos per task). If both fail the grasp, the next lever
  is more episodes, not more steps.

Conventions: "per task" is demos of each task string the policy saw. "passes over data" = steps × batch ÷ frames.
Left/right are from the operator seat facing the arm (mirrored in the overhead camera).
