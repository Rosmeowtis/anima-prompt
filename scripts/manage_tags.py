#!/usr/bin/env python3
"""标签管理工具 —— 概览浏览 + 增删改移标签和分类。

浏览: uv run scripts/manage_tags.py overview [--slot <name>]
写入: uv run scripts/manage_tags.py add|rm|rename|mv|add-cat|rm-cat ...

禁止 Agent 直接编辑 YAML，所有写入操作必须通过此脚本。
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

TAGS_PATH = Path(__file__).resolve().parent.parent / "tag-library" / "tags.yaml"

SLOT_KEYS = [
    "count-identity",
    "appearance",
    "clothing",
    "pose-action",
    "expression",
    "camera-shot",
    "scene-environment",
    "detail-mood",
]


def _load() -> dict[str, Any]:
    with open(TAGS_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _save(data: dict[str, Any]) -> None:
    def _str_representer(dumper, value):
        if '\n' in value:
            return dumper.represent_scalar('tag:yaml.org,2002:str', value, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', value)

    yaml.add_representer(str, _str_representer, Dumper=yaml.SafeDumper)

    with open(TAGS_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=True)


def _resolve(data: dict, path_str: str) -> Any:
    if not path_str:
        return data
    parts = [p.strip() for p in path_str.split("/") if p.strip()]
    current = data
    for p in parts:
        if isinstance(current, dict) and p in current:
            current = current[p]
        else:
            print(f"错误: 路径 '{path_str}' 在节点 '{p}' 处不存在", file=sys.stderr)
            sys.exit(1)
    return current


def _get_slot_data(data: dict, slot: str) -> dict:
    if slot not in SLOT_KEYS:
        print(f"错误: 未知槽位 '{slot}'，可用: {', '.join(SLOT_KEYS)}", file=sys.stderr)
        sys.exit(1)
    return data.setdefault(slot, {})


def cmd_add(args: argparse.Namespace) -> None:
    data = _load()
    slot_data = _get_slot_data(data, args.slot)
    value = _resolve(slot_data, args.path)
    if not isinstance(value, list):
        print(f"错误: 路径 '{args.path}' 的值不是列表", file=sys.stderr)
        sys.exit(1)
    if args.tag in value:
        print(f"警告: 标签 '{args.tag}' 已存在，跳过", file=sys.stderr)
        return
    value.append(args.tag)
    _save(data)
    print(f"已添加: [{args.slot}] {args.path} → {args.tag}")


def cmd_rm(args: argparse.Namespace) -> None:
    data = _load()
    slot_data = _get_slot_data(data, args.slot)
    value = _resolve(slot_data, args.path)
    if not isinstance(value, list):
        print(f"错误: 路径 '{args.path}' 的值不是列表", file=sys.stderr)
        sys.exit(1)
    if args.tag not in value:
        print(f"错误: 标签 '{args.tag}' 不存在", file=sys.stderr)
        sys.exit(1)
    value.remove(args.tag)
    _save(data)
    print(f"已删除: [{args.slot}] {args.path} → {args.tag}")


def cmd_rename(args: argparse.Namespace) -> None:
    data = _load()
    slot_data = _get_slot_data(data, args.slot)
    value = _resolve(slot_data, args.path)
    if not isinstance(value, list):
        print(f"错误: 路径 '{args.path}' 的值不是列表", file=sys.stderr)
        sys.exit(1)
    if args.old not in value:
        print(f"错误: 标签 '{args.old}' 不存在", file=sys.stderr)
        sys.exit(1)
    if args.new in value:
        print(f"错误: 新标签 '{args.new}' 已存在", file=sys.stderr)
        sys.exit(1)
    idx = value.index(args.old)
    value[idx] = args.new
    _save(data)
    print(f"已重命名: [{args.slot}] {args.path} → {args.old} → {args.new}")


def cmd_mv(args: argparse.Namespace) -> None:
    cmd_rm(argparse.Namespace(slot=args.slot, path=args.old_path, tag=args.tag))
    cmd_add(argparse.Namespace(slot=args.slot, path=args.new_path, tag=args.tag))


def cmd_add_cat(args: argparse.Namespace) -> None:
    data = _load()
    slot_data = _get_slot_data(data, args.slot)
    parts = [p.strip() for p in args.path.split("/") if p.strip()]
    if not parts:
        print("错误: 路径不能为空", file=sys.stderr)
        sys.exit(1)
    parent_path = "/".join(parts[:-1])
    new_cat = parts[-1]
    parent = _resolve(slot_data, parent_path) if parent_path else slot_data
    if not isinstance(parent, dict):
        print(f"错误: 父路径 '{parent_path}' 不是字典", file=sys.stderr)
        sys.exit(1)
    if new_cat in parent:
        print(f"警告: 分类 '{new_cat}' 已存在，跳过", file=sys.stderr)
        return
    parent[new_cat] = []
    _save(data)
    print(f"已添加分类: [{args.slot}] {args.path}")


def cmd_rm_cat(args: argparse.Namespace) -> None:
    data = _load()
    slot_data = _get_slot_data(data, args.slot)
    value = _resolve(slot_data, args.path)
    if not isinstance(value, dict) and not isinstance(value, list):
        print(f"错误: 路径 '{args.path}' 不是分类", file=sys.stderr)
        sys.exit(1)
    if isinstance(value, list) and value:
        print(f"错误: 分类 '{args.path}' 非空（含 {len(value)} 个标签），请先删除标签", file=sys.stderr)
        sys.exit(1)
    if isinstance(value, dict) and value:
        print(f"错误: 分类 '{args.path}' 非空（含子分类），请先删除子分类", file=sys.stderr)
        sys.exit(1)

    parts = [p.strip() for p in args.path.split("/") if p.strip()]
    parent_path = "/".join(parts[:-1])
    cat_name = parts[-1]
    parent = _resolve(slot_data, parent_path) if parent_path else slot_data
    if isinstance(parent, dict) and cat_name in parent:
        del parent[cat_name]
    _save(data)
    print(f"已删除分类: [{args.slot}] {args.path}")


def cmd_overview(args: argparse.Namespace) -> None:
    """列出 1~3 级标题（slot → L1 → L2）及对应行号。"""
    with open(TAGS_PATH, encoding="utf-8") as f:
        lines = f.readlines()

    current_slot = None
    for i, line in enumerate(lines, 1):
        raw = line.rstrip("\n\r")
        if not raw:
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent > 4:
            continue
        content = raw[indent:]
        if content.startswith("- ") or content.startswith("#"):
            continue
        colon_pos = content.find(":")
        if colon_pos <= 0:
            continue
        key = content[:colon_pos]
        if key.startswith(("'", '"')):
            continue

        if indent == 0:
            if not args.slot or args.slot == key:
                current_slot = key
                print(f"\n[{key}]")
            else:
                current_slot = None
        elif indent == 2 and current_slot:
            print(f"  {i:4d}  {key}")
        elif indent == 4 and current_slot:
            print(f"    {i:4d}  {key}")


def main() -> None:
    parser = argparse.ArgumentParser(description="标签管理工具")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="增加标签")
    p_add.add_argument("slot")
    p_add.add_argument("path")
    p_add.add_argument("tag")

    p_rm = sub.add_parser("rm", help="删除标签")
    p_rm.add_argument("slot")
    p_rm.add_argument("path")
    p_rm.add_argument("tag")

    p_rename = sub.add_parser("rename", help="重命名标签")
    p_rename.add_argument("slot")
    p_rename.add_argument("path")
    p_rename.add_argument("old")
    p_rename.add_argument("new")

    p_mv = sub.add_parser("mv", help="移动标签到另一分类")
    p_mv.add_argument("slot")
    p_mv.add_argument("old_path")
    p_mv.add_argument("tag")
    p_mv.add_argument("new_path")

    p_add_cat = sub.add_parser("add-cat", help="新增分类")
    p_add_cat.add_argument("slot")
    p_add_cat.add_argument("path")

    p_rm_cat = sub.add_parser("rm-cat", help="删除空分类")
    p_rm_cat.add_argument("slot")
    p_rm_cat.add_argument("path")

    p_overview = sub.add_parser("overview", help="列出 1~3 级标题及行号")
    p_overview.add_argument("--slot", default="", help="只显示指定槽位")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "add": cmd_add,
        "rm": cmd_rm,
        "rename": cmd_rename,
        "mv": cmd_mv,
        "add-cat": cmd_add_cat,
        "rm-cat": cmd_rm_cat,
        "overview": cmd_overview,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
