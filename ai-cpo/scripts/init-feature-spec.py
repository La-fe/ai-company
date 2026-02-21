#!/usr/bin/env python3
"""Generate a feature-spec.md skeleton with correct headers and Step structure.

Usage:
    python init-feature-spec.py "MyProject" --mode analyze -o ~/context/feature-spec.md
    python init-feature-spec.py "MyProject" --mode design
"""

import argparse
import datetime
import sys


STEPS_ANALYZE = [
    ("Step 1", "问题锚定", ["宏观 JTBD", "概念拆解", "不做清单"]),
    ("Step 2", "AI 能力评估", ["能力清单", "硬边界", "能力→JTBD 映射"]),
    ("Step 3", "竞品数据模型", ["竞品实体对比", "定价/留存/Onboarding 对比"]),
    ("Step 4", "数据模型", ["核心实体", "限界上下文", "领域事件目录"]),
]

STEPS_DESIGN_ONLY = [
    ("Step 5", "用户旅程 + HITL", ["端到端旅程", "渐进自主路径", "失败路径", "关键时刻"]),
    ("Step 6", "AI 系统合约", ["合约清单", "成本汇总"]),
    ("Step 7", "风险评估", []),
    ("Step 8", "Feature 清单", ["Cupcake (V1.0)", "V1.1", "V1.2", "兔子洞清单"]),
]

APPENDIX = ("附录", "持续校准", ["评估节奏", "反馈回流机制", "涨标追踪"])


def generate(product_name, mode):
    today = datetime.date.today().strftime("%Y-%m-%d")

    if mode == "analyze":
        mode_label = "analyze (Phase A: Step 1-4)"
        completion = "Step 1-4 待完成"
    else:
        mode_label = "design (Full: Step 1-8 + 附录)"
        completion = "Step 1-8 待完成"

    lines = [
        f"# Feature Spec — {product_name}",
        "",
        f"> 版本: v0.1",
        f"> 更新: {today}",
        f"> 状态: draft",
        f"> 模式: {mode_label}",
        f"> 方法论: 8-Step Concept-to-Feature (AI Product)",
        f"> 完成度: {completion}",
        "",
        "---",
        "",
    ]

    steps = list(STEPS_ANALYZE)
    if mode == "design":
        steps.extend(STEPS_DESIGN_ONLY)

    for step_id, step_name, subsections in steps:
        lines.append(f"## {step_id}: {step_name}")
        lines.append("")
        for sub in subsections:
            lines.append(f"### {sub}")
            lines.append("")
        lines.append("---")
        lines.append("")

    if mode == "design":
        lines.append(f"## {APPENDIX[0]}: {APPENDIX[1]}")
        lines.append("")
        for sub in APPENDIX[2]:
            lines.append(f"### {sub}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate feature-spec.md skeleton"
    )
    parser.add_argument("product_name", help="Product name for the header")
    parser.add_argument(
        "--mode",
        choices=["analyze", "design"],
        default="design",
        help="Mode: analyze (Step 1-4) or design (Step 1-8)",
    )
    parser.add_argument(
        "--output", "-o",
        default="feature-spec.md",
        help="Output file path (default: feature-spec.md)",
    )
    args = parser.parse_args()

    content = generate(args.product_name, args.mode)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)

    step_count = 4 if args.mode == "analyze" else 8
    extra = " + appendix" if args.mode == "design" else ""
    print(f"Created {args.output} ({args.mode} mode, {step_count} steps{extra})")


if __name__ == "__main__":
    main()
