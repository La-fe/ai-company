#!/usr/bin/env python3
"""
tasks.jsonl CRUD utility.

Usage:
  tasks-crud.py list   <tasks_file> [--status STATUS] [--plan PLAN] [--priority P0|P1|P2] [--dimension DIM]
  tasks-crud.py today  <tasks_file>
  tasks-crud.py week   <tasks_file>
  tasks-crud.py stats  <tasks_file> [--plan PLAN]
  tasks-crud.py add    <tasks_file> --json '<json_string>'
  tasks-crud.py update <tasks_file> --id ID --field FIELD --value VALUE
  tasks-crud.py deps   <tasks_file> --id ID
  tasks-crud.py next-id <tasks_file> --goal GOAL --dimension DIMENSION

All output is human-readable for dashboard display. Use --json-out for machine-readable output.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from argparse import ArgumentParser


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


def save_tasks(path, tasks):
    with open(path, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def week_range():
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday.isoformat(), sunday.isoformat()


def cmd_list(tasks, args):
    filtered = tasks
    if args.status:
        statuses = args.status.split(",")
        filtered = [t for t in filtered if t.get("status") in statuses]
    if args.plan:
        filtered = [t for t in filtered if t.get("plan") == args.plan]
    if args.priority:
        filtered = [t for t in filtered if t.get("priority") == args.priority]
    if args.dimension:
        filtered = [t for t in filtered if t.get("dimension") == args.dimension]

    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    filtered.sort(key=lambda t: priority_order.get(t.get("priority", "P2"), 9))
    print_tasks(filtered)


def cmd_today(tasks, _args):
    today = today_str()
    filtered = [
        t for t in tasks
        if t.get("deadline", "") <= today
        and t.get("status") in ("pending", "in_progress")
    ]
    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    filtered.sort(key=lambda t: priority_order.get(t.get("priority", "P2"), 9))
    print_tasks(filtered)


def cmd_week(tasks, _args):
    mon, sun = week_range()
    filtered = [
        t for t in tasks
        if mon <= t.get("deadline", "9999-99-99") <= sun
        and t.get("status") not in ("completed", "cancelled")
    ]
    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    filtered.sort(key=lambda t: priority_order.get(t.get("priority", "P2"), 9))
    print_tasks(filtered)


def cmd_stats(tasks, args):
    filtered = tasks
    if args.plan:
        filtered = [t for t in filtered if t.get("plan") == args.plan]

    total = len(filtered)
    by_status = {}
    for t in filtered:
        s = t.get("status", "unknown")
        by_status[s] = by_status.get(s, 0) + 1

    done = by_status.get("completed", 0)
    blocked = by_status.get("blocked", 0)
    pct = f"{done/total*100:.0f}%" if total else "0%"

    print(f"Total: {total} | Done: {done} ({pct}) | Blocked: {blocked}")
    for s, c in sorted(by_status.items()):
        print(f"  {s}: {c}")


def cmd_add(tasks, args):
    new_task = json.loads(args.json)
    new_task.setdefault("created", today_str())
    new_task.setdefault("updated", today_str())
    new_task.setdefault("status", "pending")
    new_task.setdefault("dependencies", [])
    new_task.setdefault("notes", "")
    tasks.append(new_task)
    save_tasks(args.tasks_file, tasks)
    print(f"ADDED: {new_task.get('id')} — {new_task.get('title')}")


def cmd_update(tasks, args):
    found = False
    for t in tasks:
        if t.get("id") == args.id:
            t[args.field] = args.value
            t["updated"] = today_str()
            found = True
            break
    if not found:
        print(f"ERROR: task {args.id} not found")
        sys.exit(1)
    save_tasks(args.tasks_file, tasks)
    print(f"UPDATED: {args.id}.{args.field} = {args.value}")


def cmd_deps(tasks, args):
    task_map = {t["id"]: t for t in tasks}
    target = task_map.get(args.id)
    if not target:
        print(f"ERROR: task {args.id} not found")
        sys.exit(1)

    upstream = target.get("dependencies", [])
    downstream = [t["id"] for t in tasks if args.id in t.get("dependencies", [])]
    blocked_upstream = [
        uid for uid in upstream
        if task_map.get(uid, {}).get("status") not in ("completed",)
    ]

    print(f"Task: {args.id} — {target.get('title')}")
    print(f"Depends on: {upstream or 'none'}")
    print(f"  Incomplete upstream: {blocked_upstream or 'all clear'}")
    print(f"Blocks: {downstream or 'none'}")

    if target.get("status") == "completed" and downstream:
        newly_unblocked = []
        for did in downstream:
            dt = task_map.get(did, {})
            all_deps_done = all(
                task_map.get(dep, {}).get("status") == "completed"
                for dep in dt.get("dependencies", [])
            )
            if all_deps_done:
                newly_unblocked.append(did)
        if newly_unblocked:
            print(f"UNLOCKED: {newly_unblocked}")


def cmd_next_id(tasks, args):
    prefix = f"{args.goal}-{args.dimension[0].upper()}-"
    existing = [t["id"] for t in tasks if t["id"].startswith(prefix)]
    if existing:
        nums = [int(tid.split("-")[-1]) for tid in existing]
        next_num = max(nums) + 1
    else:
        next_num = 1
    print(f"{prefix}{next_num:02d}")


def print_tasks(tasks):
    if not tasks:
        print("(no tasks)")
        return
    for t in tasks:
        deps = t.get("dependencies", [])
        dep_str = f" deps:{','.join(deps)}" if deps else ""
        print(
            f"  {t.get('priority','??')}: [{t.get('id')}] {t.get('title')} "
            f"— {t.get('status')} — deadline {t.get('deadline','?')}{dep_str}"
        )


def main():
    parser = ArgumentParser(description="tasks.jsonl CRUD")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list")
    p_list.add_argument("tasks_file")
    p_list.add_argument("--status")
    p_list.add_argument("--plan")
    p_list.add_argument("--priority")
    p_list.add_argument("--dimension")

    p_today = sub.add_parser("today")
    p_today.add_argument("tasks_file")

    p_week = sub.add_parser("week")
    p_week.add_argument("tasks_file")

    p_stats = sub.add_parser("stats")
    p_stats.add_argument("tasks_file")
    p_stats.add_argument("--plan")

    p_add = sub.add_parser("add")
    p_add.add_argument("tasks_file")
    p_add.add_argument("--json", required=True)

    p_update = sub.add_parser("update")
    p_update.add_argument("tasks_file")
    p_update.add_argument("--id", required=True)
    p_update.add_argument("--field", required=True)
    p_update.add_argument("--value", required=True)

    p_deps = sub.add_parser("deps")
    p_deps.add_argument("tasks_file")
    p_deps.add_argument("--id", required=True)

    p_next = sub.add_parser("next-id")
    p_next.add_argument("tasks_file")
    p_next.add_argument("--goal", required=True)
    p_next.add_argument("--dimension", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    tasks = load_tasks(args.tasks_file)

    cmds = {
        "list": cmd_list,
        "today": cmd_today,
        "week": cmd_week,
        "stats": cmd_stats,
        "add": cmd_add,
        "update": cmd_update,
        "deps": cmd_deps,
        "next-id": cmd_next_id,
    }
    cmds[args.command](tasks, args)


if __name__ == "__main__":
    main()
