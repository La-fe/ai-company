#!/usr/bin/env python3
"""
Renders the company operations dashboard.

Usage:
  dashboard.py <company_dir>

Reads tasks.jsonl and git state, outputs a formatted dashboard.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta


def load_tasks(path):
    tasks = []
    if not os.path.exists(path):
        return tasks
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks


def git_info(company_dir):
    info = {"commit_count": 0, "latest_tag": "none"}
    try:
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=company_dir, capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            info["commit_count"] = int(result.stdout.strip())
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=company_dir, capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            info["latest_tag"] = result.stdout.strip()
    except Exception:
        pass

    return info


def week_range():
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday.isoformat(), sunday.isoformat()


WEEKDAYS_ZH = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def main():
    if len(sys.argv) < 2:
        print("Usage: dashboard.py <company_dir>")
        sys.exit(1)

    company_dir = sys.argv[1]
    tasks_file = os.path.join(company_dir, "tasks.jsonl")
    company_md = os.path.join(company_dir, "context", "company.md")

    company_name = os.path.basename(company_dir.rstrip("/"))
    if os.path.exists(company_md):
        with open(company_md, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line.startswith("# "):
                company_name = first_line[2:].strip()

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    weekday = WEEKDAYS_ZH[today.weekday()]

    gi = git_info(company_dir)
    tasks = load_tasks(tasks_file)

    print(f"{company_name} | {today_str} {weekday} | git: {gi['commit_count']} commits, tag: {gi['latest_tag']}")
    print()

    today_tasks = [
        t for t in tasks
        if t.get("deadline", "") <= today_str
        and t.get("status") in ("pending", "in_progress")
    ]
    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    today_tasks.sort(key=lambda t: priority_order.get(t.get("priority", "P2"), 9))

    if today_tasks:
        print("今日任务:")
        for t in today_tasks:
            deps = t.get("dependencies", [])
            dep_str = ""
            if deps:
                dep_str = f"\n      依赖: {', '.join(deps)}"
            print(
                f"  {t.get('priority','??')}: [{t.get('id')}] {t.get('title')} "
                f"— {t.get('status')} — deadline {t.get('deadline','?')}{dep_str}"
            )
    else:
        print("今日任务: 暂无到期任务")

    print()

    mon, sun = week_range()
    week_tasks = [
        t for t in tasks
        if mon <= t.get("deadline", "9999-99-99") <= sun
    ]
    done = sum(1 for t in week_tasks if t.get("status") == "completed")
    blocked = sum(1 for t in week_tasks if t.get("status") == "blocked")
    total = len(week_tasks)
    pct = f"{done/total*100:.0f}%" if total else "0%"
    print(f"本周进度: {done}/{total} done ({pct}) | {blocked} blocked")
    print()

    print("操作:")
    print("  A. 更新任务      B. 添加任务/想法    C. 调整优先级/目标")
    print("  D. 新建规划      E. 继续/调整已有规划")
    print("  F. 周复盘        G. 月度复盘")


if __name__ == "__main__":
    main()
