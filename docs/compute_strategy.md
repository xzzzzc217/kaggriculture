# Compute strategy

## Principle

Use the cheapest compute that can answer the current question. Kaggriculture is a 720-turn,
two-player simulator, so deterministic planning, rule validation, replay parsing, and league
evaluation are CPU-first. GPU time is reserved for experiments whose value is established by a
pre-registered local gate.

## Available compute

- Local deep-learning environment: PyTorch 2.6.0+cu118.
- Local GPU: NVIDIA GeForce RTX 4060 Laptop GPU, 8 GiB VRAM.
- Kaggle weekly accelerator allocation: preserve for longer reproducible training jobs after a
  local pilot passes. The exact remaining quota is checked in the Kaggle UI before each run.
- Submission runtime: 1.6 vCPU, 6.5 GiB RAM, 8 GiB disk, and a 100 MiB submission limit.

## Staged use

1. **CPU simulator first**: action-contract tests, both seats, deterministic seeds, heuristic
   search, replay analysis, and ablation leagues.
2. **Local RTX 4060 second**: compact behavior-cloning or value-model pilots, mixed precision,
   small batches, and cached trajectories. No GPU is used merely because it is available.
3. **Kaggle GPU third**: only for a frozen training recipe that already shows a robust gain in the
   local league. Each run must export configuration, seed, checkpoint hash, metrics, and runtime.
4. **TPU only with evidence**: use only if the model and input pipeline are XLA-friendly and a
   throughput check shows a real advantage.

## Promotion gates

- Every candidate plays from both seats against the current champion and a fixed opponent suite.
- Use multiple seeds and report win rate, Wilson interval, reward margin, runtime, and failures.
- Promote only if the lower confidence bound and worst-case slices improve, not just the mean.
- A leaderboard submission requires an immutable artifact, local validation, size/runtime checks,
  and an explicit user authorization. Kaggle allows five daily submissions, but only the newest
  two remain active, so daily slots are evidence checkpoints rather than a quota to exhaust.

