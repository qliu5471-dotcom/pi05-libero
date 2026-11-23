#!/usr/bin/env python3
"""把评测日志聚合成可写进 RESULTS.md 的表格。

用法：
    python tools/aggregate.py logs/eval_*.json --suite libero_long

输入 json 结构（每个文件一组实验）：
    {
      "model": "pi05_libero_lora_r32_30k",
      "suite": "libero_long",
      "seed": 0,
      "tasks": {"task_1": {"trials": 20, "success": 13}, ...}
    }

输出：逐任务成功率、suite 总体成功率、Wilson 95% 置信区间。
"""
from __future__ import annotations

import argparse
import glob
import json
import math
from collections import defaultdict


def wilson(success: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval，比正态近似更适合小样本成功率。"""
    if trials == 0:
        return (0.0, 0.0)
    p = success / trials
    denom = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denom
    half = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def load(paths: list[str]) -> list[dict]:
    records = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as fh:
            records.append(json.load(fh))
    return records


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="评测 json，支持通配符")
    ap.add_argument("--suite", default=None, help="只统计某个 suite")
    ap.add_argument("--markdown", action="store_true", help="直接输出 markdown 表格")
    args = ap.parse_args()

    expanded: list[str] = []
    for pattern in args.paths:
        expanded.extend(glob.glob(pattern))
    records = [r for r in load(expanded) if args.suite is None or r.get("suite") == args.suite]
    if not records:
        raise SystemExit("没有匹配到评测记录")

    by_model: dict[str, dict[str, dict[str, int]]] = defaultdict(dict)
    for rec in records:
        model = rec["model"]
        for task, stat in rec["tasks"].items():
            agg = by_model[model].setdefault(task, {"trials": 0, "success": 0})
            agg["trials"] += int(stat["trials"])
            agg["success"] += int(stat["success"])

    rows = []
    for model, tasks in by_model.items():
        t = sum(v["trials"] for v in tasks.values())
        s = sum(v["success"] for v in tasks.values())
        lo, hi = wilson(s, t)
        rows.append((model, len(tasks), s, t, s / t, lo, hi))

    header = ("model", "tasks", "success", "trials", "rate", "ci_low", "ci_high")
    if args.markdown:
        print("| " + " | ".join(header) + " |")
        print("| " + " | ".join(["---"] * len(header)) + " |")
        for r in rows:
            print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]:.1%} | {r[5]:.1%} | {r[6]:.1%} |")
    else:
        for r in rows:
            print(f"{r[0]}: {r[2]}/{r[3]} = {r[4]:.1%}  [95% CI {r[5]:.1%}, {r[6]:.1%}]")


if __name__ == "__main__":
    main()
