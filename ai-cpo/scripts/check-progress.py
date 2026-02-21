#!/usr/bin/env python3
"""Check completion status of a feature-spec.md file.

Usage:
    python check-progress.py ~/context/feature-spec.md
"""

import argparse
import re
import sys


EXPECTED_STEPS = {
    1: "问题锚定",
    2: "AI 能力评估",
    3: "竞品数据模型",
    4: "数据模型",
    5: "用户旅程",
    6: "AI 系统合约",
    7: "风险评估",
    8: "Feature 清单",
}

APPENDIX_NAME = "持续校准"

# Minimum characters of meaningful content (excluding headings/separators)
MIN_CONTENT_LENGTH = 20


def parse_mode(content):
    """Extract declared mode from header."""
    match = re.search(r"> 模式:\s*(.+)", content)
    if not match:
        return "unknown"
    mode_str = match.group(1).strip()
    if "analyze" in mode_str:
        return "analyze"
    if "design" in mode_str:
        return "design"
    return mode_str


def parse_completion(content):
    """Extract declared completion from header."""
    match = re.search(r"> 完成度:\s*(.+)", content)
    return match.group(1).strip() if match else "unknown"


def section_has_content(content, start_pos, end_pos):
    """Check if a section has meaningful content beyond headings."""
    section = content[start_pos:end_pos]
    # Remove markdown headings, separators, and whitespace
    cleaned = re.sub(r"^#{1,4}\s.*$", "", section, flags=re.MULTILINE)
    cleaned = re.sub(r"^---$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\|[- |]+\|$", "", cleaned, flags=re.MULTILINE)  # empty table separators
    cleaned = cleaned.strip()
    return len(cleaned) >= MIN_CONTENT_LENGTH


def find_sections(content):
    """Find all Step and Appendix sections with their positions."""
    sections = {}

    # Find Step N: headings
    for match in re.finditer(r"^## Step (\d+):", content, re.MULTILINE):
        step_num = int(match.group(1))
        sections[f"step_{step_num}"] = match.start()

    # Find Appendix
    appendix_match = re.search(r"^## 附录:", content, re.MULTILINE)
    if appendix_match:
        sections["appendix"] = appendix_match.start()

    return sections


def main():
    parser = argparse.ArgumentParser(
        description="Check feature-spec.md completion status"
    )
    parser.add_argument("file", help="Path to feature-spec.md")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {args.file}")
        sys.exit(1)

    mode = parse_mode(content)
    declared = parse_completion(content)
    sections = find_sections(content)

    # Determine expected steps based on mode
    max_step = 4 if mode == "analyze" else 8

    print(f"File:     {args.file}")
    print(f"Mode:     {mode}")
    print(f"Declared: {declared}")
    print()

    # Get all section positions sorted for boundary detection
    all_positions = sorted(sections.values())

    completed = 0
    filled_steps = []

    for step_num in range(1, max_step + 1):
        name = EXPECTED_STEPS[step_num]
        key = f"step_{step_num}"

        if key not in sections:
            status = "missing"
            marker = "x"
        else:
            pos = sections[key]
            # Find next section boundary
            next_positions = [p for p in all_positions if p > pos]
            end_pos = next_positions[0] if next_positions else len(content)

            if section_has_content(content, pos, end_pos):
                status = "filled"
                marker = "v"
                completed += 1
                filled_steps.append(step_num)
            else:
                status = "empty"
                marker = "o"

        print(f"  [{marker}] Step {step_num}: {name}")

    # Check appendix for design mode
    if max_step == 8:
        key = "appendix"
        if key not in sections:
            print(f"  [x] Appendix: {APPENDIX_NAME}")
        else:
            pos = sections[key]
            next_positions = [p for p in all_positions if p > pos]
            end_pos = next_positions[0] if next_positions else len(content)
            if section_has_content(content, pos, end_pos):
                print(f"  [v] Appendix: {APPENDIX_NAME}")
            else:
                print(f"  [o] Appendix: {APPENDIX_NAME}")

    print()

    # Summary
    if completed == max_step:
        actual = f"Step 1-{max_step} complete"
    else:
        actual = f"{completed}/{max_step} steps filled"

    print(f"Progress: {actual}")

    # Suggest completion line
    if filled_steps:
        if filled_steps == list(range(1, max_step + 1)):
            suggested = f"Step 1-{max_step} 已完成"
        else:
            suggested = f"Step {','.join(str(s) for s in filled_steps)} 已完成"
    else:
        suggested = "未开始"

    print(f"Suggested: > 完成度: {suggested}")


if __name__ == "__main__":
    main()
