# π0.5 / LIBERO 复现记录

本仓库是我的个人复现记录，**代码基线来自上游开源项目**，这里只放我自己写的配置、脚本、评测日志与结果。

> 上游：Physical-Intelligence/openpi（Apache-2.0）
> 模型：π0.5（VLA，PaliGemma 2B 骨干 + 300M action expert，flow matching）
> 基准：LIBERO（π0.5-LIBERO 变体）

## 目标

1. 搭通 openpi 的推理环境，跑通 π0.5 在 LIBERO 上的 zero-shot 评测
2. 完成 LoRA 微调（约 30k steps），记录显存、吞吐与耗时
3. 把评测结果与论文报告的数值做对齐，写清差异原因

## 环境

| 项 | 版本 |
| --- | --- |
| OS | Ubuntu 22.04 |
| GPU | RTX 4090 24G（LoRA 约 22.5GB 显存） |
| CUDA | 待填 |
| Python | 3.10 |
| 依赖管理 | uv |
| 框架 | JAX / PyTorch（二选一，见下方记录） |

## 复现步骤

命令以上游 README 为准，我这里记录**实际跑通的那一串**，与上游有出入的地方会注明原因。

1. 克隆并同步依赖：`git clone --recurse-submodules` + `GIT_LFS_SKIP_SMUDGE=1 uv sync`
2. 下载 π0.5-LIBERO 权重
3. 数据准备：LIBERO 数据集转换（转换脚本与参数见 `reproduce/`）
4. LoRA 微调：见 `reproduce/finetune.sh`
5. 评测：见 `reproduce/eval.sh`

## 仓库结构

```
pi05-libero/
├── README.md          # 本文件：目标、环境、结论
├── EXPERIMENTS.md     # 实验设计：基准对齐 / LoRA 消融 / 真机迁移
├── RESULTS.md         # 实测结果与对照表
├── NOTES.md           # 踩坑记录（编译失败、OOM、版本冲突）
├── tools/
│   └── aggregate.py   # 评测日志聚合：成功率 + Wilson 95% 置信区间
├── reproduce/
│   ├── finetune.sh    # 微调命令封装
│   ├── eval.sh        # 评测命令封装
│   └── env.md         # 环境搭建逐条记录
└── NOTICE.md          # 上游署名与许可说明
```

## 状态

- [ ] 环境搭建
- [ ] zero-shot 评测跑通
- [ ] LoRA 微调完成
- [ ] 结果与论文对齐并写入 RESULTS.md

## 参考

- π0.5 论文：*π0.5: a Vision-Language-Action Model with Open-World Generalization*（arXiv, 2025-04）
- 上游仓库：https://github.com/Physical-Intelligence/openpi
