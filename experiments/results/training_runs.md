# Training runs

Every run that started a GPU, with what it saw and what it cost. Loss curves (every 100 steps) are in
`training_loss.csv`. Costs are A10G at ~$1.10/h unless noted. Dataset `so101_blocks` is private on the Hub
until the footage is reviewed.

| date (UTC) | job | policy | data | per task | steps × batch | passes over data | GPU | wall | cost | loss start → end | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-06 | act_svla_so101_pickplace_2000 | ACT from scratch | public `lerobot/svla_so101_pickplace`, 50 ep | 50 | 2,000 × 8 | 1.3 | A10G | 6.2 min | $0.18 | 1.9 → 1.15 | pipeline dry run; cameras `up`/`side`, never driven |
| 2026-09-08 | act_so101_test_r1_…_2000 | ACT from scratch | 5 test episodes (deleted) | 5 | 2,000 × 8 | 4.2 | A10G | 6.2 min | $0.19 | 10.1 → 1.17 | smoke test: trainer accepts `top`/`wrist` keys |
| 2026-09-08 | act_so101_blocks_20000_ep0-49 | ACT from scratch (ResNet-18 ImageNet backbone) | `so101_blocks` ep 0–49: red→left, blue→right | 25 | 20,000 × 8 | 5.7 | A10G | 55.3 min | ≈$1.01 | 9.9 → 0.18 (l1 0.16 at the end) | shakedown on sticker 1: reaches toward the block, jerky, no grasp, returns |
| 2026-09-08 | act_so101_blocks_20000_ep0-49_100-149 | ACT from scratch (ResNet-18 ImageNet backbone) | `so101_blocks` ep 0–49 + 100–149: red→left, blue→right | 50 | 20,000 × 8 | ~2.9 | A10G | 55.3 min | ≈$1.01 | 10.0 → 0.19 (l1 0.17 at the end) | same steps as ACT-50, so the only difference is data; R3 eval checkpoint |

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
