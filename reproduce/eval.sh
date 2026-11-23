#!/usr/bin/env bash
# π0.5 在 LIBERO 上的评测封装
set -euo pipefail

CKPT="${CKPT:-gs://openpi-assets/checkpoints/pi05_libero}"
NUM_TRIALS="${NUM_TRIALS:-50}"

# TODO: 与上游 examples/libero 下的评测入口对齐
uv run examples/libero/main.py \
  --policy-config="${CKPT}" \
  --num-trials="${NUM_TRIALS}"

# 评测输出（每个任务的成功率）保存到 logs/eval_$(date +%Y%m%d_%H%M).json
# 汇总后写入 RESULTS.md，注明 episode 数与随机种子
