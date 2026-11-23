#!/usr/bin/env bash
# π0.5-LIBERO LoRA 微调封装
# 具体参数以上游 openpi 的 README 与 config 为准，跑通后把实际值固定到这里
set -euo pipefail

EXP_NAME="${EXP_NAME:-pi05_libero_lora_$(date +%Y%m%d)}"

# TODO: 确认当前上游提供的 config 名，常见形如 pi05_libero
CONFIG="pi05_libero"

uv run scripts/train.py "${CONFIG}" \
  --exp-name="${EXP_NAME}" \
  --overwrite

# 训练完成后记录：
#   wandb / 本地 log 路径
#   显存峰值、单步耗时、总步数
# 把数字同步到 RESULTS.md
