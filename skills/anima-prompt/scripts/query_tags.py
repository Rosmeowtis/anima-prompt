#!/usr/bin/env python3
"""标签库查询工具 —— 标签库 CRUD + 搜索。

用法:
  python query_tags.py list
  python query_tags.py tree <slot> [--path <path>]
  python query_tags.py get <slot> <path> [--leaves]
  python query_tags.py search <keyword> [--slot <slot>] [--fuzzy] [--threshold <n>]
  python query_tags.py add <slot> <path> <tag>
  python query_tags.py rm <slot> <path> <tag>
  python query_tags.py rename <slot> <path> <old> <new>
  python query_tags.py mv <slot> <old_path> <tag> <new_path>
  python query_tags.py add-cat <slot> <path>
  python query_tags.py rm-cat <slot> <path>

全局参数:
  --json  以 JSON 格式输出
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import yaml

try:
    from rapidfuzz import fuzz, process
    HAS_RAPIDFUZZ = True
except ImportError:
    HAS_RAPIDFUZZ = False

TAG_LIBRARY_DIR = Path(__file__).resolve().parent.parent / "tag-library"

SLOT_FILES = {
    "count-identity":    "count-identity.yaml",
    "appearance":        "appearance.yaml",
    "clothing":          "clothing.yaml",
    "pose-action":       "pose-action.yaml",
    "expression":        "expression.yaml",
    "camera-shot":       "camera-shot.yaml",
    "scene-environment": "scene-environment.yaml",
    "detail-mood":       "detail-mood.yaml",
}


def _load(slot: str) -> dict:
    fname = SLOT_FILES.get(slot)
    if fname is None:
        print(f"错误: 未知槽位 '{slot}'，可用: {', '.join(SLOT_FILES)}", file=sys.stderr)
        sys.exit(1)
    path = TAG_LIBRARY_DIR / fname
    if not path.exists():
        print(f"错误: 文件不存在 {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _save(slot: str, data: dict) -> None:
    fname = SLOT_FILES[slot]
    path = TAG_LIBRARY_DIR / fname
    bak = path.with_suffix(".yaml.bak")
    if path.exists():
        bak.write_bytes(path.read_bytes())
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def _resolve(data: dict, path_str: str) -> Any:
    """按 / 分割路径递归访问嵌套字典。"""
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


def _set_value(data: dict, path_str: str, value: Any) -> dict:
    parts = [p.strip() for p in path_str.split("/") if p.strip()]
    if not parts:
        return data
    current = data
    for p in parts[:-1]:
        if p not in current:
            current[p] = {}
        current = current[p]
    current[parts[-1]] = value
    return data


def _delete_key(data: dict, path_str: str) -> dict:
    parts = [p.strip() for p in path_str.split("/") if p.strip()]
    if not parts:
        return data
    current = data
    for p in parts[:-1]:
        if p not in current:
            return data
        current = current[p]
    if parts[-1] in current:
        del current[parts[-1]]
    return data


def _tree(data: dict, prefix: str = "", is_json: bool = False, max_depth: int = 3, current_depth: int = 0) -> str | list:
    if current_depth >= max_depth:
        return "" if not is_json else []
    lines: list[str] = []
    items: list[dict] = []
    for key, value in data.items():
        if isinstance(value, dict):
            if is_json:
                children = _tree(value, prefix + "  ", is_json, max_depth, current_depth + 1)
                items.append({"name": key, "type": "category", "children": children if isinstance(children, list) else []})
            else:
                lines.append(f"{prefix}{key}/")
                lines.append(_tree(value, prefix + "  ", is_json, max_depth, current_depth + 1))
        elif isinstance(value, list):
            item_count = len(value)
            if is_json:
                items.append({"name": key, "type": "leaf", "count": item_count})
            else:
                lines.append(f"{prefix}{key}  ({item_count} tags)")
        else:
            if is_json:
                items.append({"name": key, "type": "value"})
            else:
                lines.append(f"{prefix}{key}")
    if is_json:
        return items
    return "\n".join(lines)


def _flatten_tags(data: dict, slot: str, prefix: str = "") -> list[tuple[str, str, str]]:
    """返回 [(slot, path, tag), ...]"""
    result: list[tuple[str, str, str]] = []
    for key, value in data.items():
        current_path = f"{prefix}/{key}" if prefix else key
        if isinstance(value, list):
            for tag in value:
                if isinstance(tag, str):
                    result.append((slot, current_path, tag))
        elif isinstance(value, dict):
            result.extend(_flatten_tags(value, slot, current_path))
        elif isinstance(value, str):
            result.append((slot, current_path, value))
    return result


def cmd_list(args: argparse.Namespace) -> None:
    slots = list(SLOT_FILES.keys())
    if args.json:
        print(json.dumps({"slots": slots}, ensure_ascii=False, indent=2))
    else:
        for s in slots:
            fname = SLOT_FILES[s]
            path = TAG_LIBRARY_DIR / fname
            exists = "✓" if path.exists() else "✗"
            print(f"  {exists} {s}  ({fname})")


def cmd_tree(args: argparse.Namespace) -> None:
    data = _load(args.slot)
    if args.path:
        data = _resolve(data, args.path)
    output = _tree(data, is_json=args.json)
    if args.json:
        print(json.dumps({"slot": args.slot, "path": args.path or "", "tree": output}, ensure_ascii=False, indent=2))
    else:
        print(output)


def cmd_get(args: argparse.Namespace) -> None:
    data = _load(args.slot)
    value = _resolve(data, args.path)
    if args.leaves:
        if isinstance(value, list):
            result = [x for x in value if isinstance(x, str)]
        elif isinstance(value, str):
            result = [value]
        else:
            result = [tag for _, _, tag in _flatten_tags(value, args.slot)]
    else:
        result = value
    if args.json:
        print(json.dumps({"slot": args.slot, "path": args.path, "data": result}, ensure_ascii=False, indent=2))
    elif isinstance(result, list):
        for item in result:
            print(item)
    elif isinstance(result, dict):
        print(yaml.dump(result, allow_unicode=True, default_flow_style=False, sort_keys=False))
    else:
        print(result)


def cmd_search(args: argparse.Namespace) -> None:
    keyword: str = args.keyword
    threshold: int = args.threshold if args.threshold else 70
    slots_to_search = [args.slot] if args.slot else list(SLOT_FILES.keys())

    all_tags: list[tuple[str, str, str]] = []
    for slot in slots_to_search:
        try:
            data = _load(slot)
        except SystemExit:
            continue
        all_tags.extend(_flatten_tags(data, slot))

    if args.fuzzy:
        if not HAS_RAPIDFUZZ:
            print("错误: --fuzzy 需要 rapidfuzz 库，请执行 pip install rapidfuzz", file=sys.stderr)
            sys.exit(1)
        tag_texts = [tag for _, _, tag in all_tags]
        matches = process.extract(
            keyword,
            tag_texts,
            scorer=fuzz.partial_ratio,
            limit=20,
            score_cutoff=threshold,
        )
        results: list[tuple[str, str, str, float]] = []
        seen: set[int] = set()
        for tag_text, score, idx in matches:
            if idx not in seen:
                seen.add(idx)
                slot, path, _ = all_tags[idx]
                results.append((slot, path, tag_text, score))
        results.sort(key=lambda x: -x[3])
    else:
        results = []
        keyword_lower = keyword.lower()
        for slot, path, tag in all_tags:
            if keyword_lower in tag.lower():
                results.append((slot, path, tag, 100))
            elif keyword_lower in path.lower():
                results.append((slot, path, tag, 50))

    if args.json:
        output = [{"slot": s, "path": p, "tag": t, "score": sc} for s, p, t, sc in results]
        print(json.dumps({"keyword": keyword, "fuzzy": args.fuzzy, "results": output}, ensure_ascii=False, indent=2))
    else:
        if not results:
            print(f"未找到匹配 '{keyword}' 的标签")
            return
        current_slot = ""
        current_path = ""
        for slot, path, tag, score in results:
            if slot != current_slot:
                print(f"\n[{slot}]")
                current_slot = slot
                current_path = ""
            if path != current_path:
                print(f"  {path}")
                current_path = path
            score_str = f" (score: {score})" if args.fuzzy and score < 100 else ""
            print(f"    {tag}{score_str}")


def cmd_add(args: argparse.Namespace) -> None:
    data = _load(args.slot)
    value = _resolve(data, args.path)
    if not isinstance(value, list):
        print(f"错误: 路径 '{args.path}' 的值不是列表，无法添加标签", file=sys.stderr)
        sys.exit(1)
    if args.tag in value:
        print(f"警告: 标签 '{args.tag}' 已存在，跳过", file=sys.stderr)
        return
    value.append(args.tag)
    _save(args.slot, data)
    print(f"已添加: [{args.slot}] {args.path} → {args.tag}")


def cmd_rm(args: argparse.Namespace) -> None:
    data = _load(args.slot)
    value = _resolve(data, args.path)
    if not isinstance(value, list):
        print(f"错误: 路径 '{args.path}' 的值不是列表", file=sys.stderr)
        sys.exit(1)
    if args.tag not in value:
        print(f"错误: 标签 '{args.tag}' 不存在", file=sys.stderr)
        sys.exit(1)
    value.remove(args.tag)
    _save(args.slot, data)
    print(f"已删除: [{args.slot}] {args.path} → {args.tag}")


def cmd_rename(args: argparse.Namespace) -> None:
    data = _load(args.slot)
    value = _resolve(data, args.path)
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
    _save(args.slot, data)
    print(f"已重命名: [{args.slot}] {args.path} → {args.old} → {args.new}")


def cmd_mv(args: argparse.Namespace) -> None:
    cmd_rm(args)
    cmd_add(args)


def cmd_add_cat(args: argparse.Namespace) -> None:
    data = _load(args.slot)
    parts = [p.strip() for p in args.path.split("/") if p.strip()]
    if not parts:
        print("错误: 路径不能为空", file=sys.stderr)
        sys.exit(1)
    parent_path = "/".join(parts[:-1])
    new_cat = parts[-1]
    parent = _resolve(data, parent_path) if parent_path else data
    if not isinstance(parent, dict):
        print(f"错误: 父路径 '{parent_path}' 不是字典", file=sys.stderr)
        sys.exit(1)
    if new_cat in parent:
        print(f"警告: 分类 '{new_cat}' 已存在，跳过", file=sys.stderr)
        return
    parent[new_cat] = []
    _save(args.slot, data)
    print(f"已添加分类: [{args.slot}] {args.path}")


def cmd_rm_cat(args: argparse.Namespace) -> None:
    data = _load(args.slot)
    value = _resolve(data, args.path)
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
    parent = _resolve(data, parent_path) if parent_path else data
    if isinstance(parent, dict) and cat_name in parent:
        del parent[cat_name]
    _save(args.slot, data)
    print(f"已删除分类: [{args.slot}] {args.path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Anima 标签库查询工具")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="列出所有槽位")

    p_tree = sub.add_parser("tree", help="查看分类树")
    p_tree.add_argument("slot", help="槽位名")
    p_tree.add_argument("--path", default="", help="子路径")

    p_get = sub.add_parser("get", help="读取标签")
    p_get.add_argument("slot", help="槽位名")
    p_get.add_argument("path", help="分类路径，如 头发/颜色")
    p_get.add_argument("--leaves", action="store_true", help="仅返回标签文本")

    p_search = sub.add_parser("search", help="搜索标签")
    p_search.add_argument("keyword", help="搜索关键词")
    p_search.add_argument("--slot", default="", help="限制槽位")
    p_search.add_argument("--fuzzy", action="store_true", help="启用 rapidfuzz 模糊匹配")
    p_search.add_argument("--threshold", type=int, default=70, help="模糊匹配阈值 (默认 70)")

    p_add = sub.add_parser("add", help="增加标签")
    p_add.add_argument("slot", help="槽位名")
    p_add.add_argument("path", help="分类路径")
    p_add.add_argument("tag", help="标签文本")

    p_rm = sub.add_parser("rm", help="删除标签")
    p_rm.add_argument("slot", help="槽位名")
    p_rm.add_argument("path", help="分类路径")
    p_rm.add_argument("tag", help="标签文本")

    p_rename = sub.add_parser("rename", help="重命名标签")
    p_rename.add_argument("slot", help="槽位名")
    p_rename.add_argument("path", help="分类路径")
    p_rename.add_argument("old", help="旧标签")
    p_rename.add_argument("new", help="新标签")

    p_mv = sub.add_parser("mv", help="移动标签到另一分类")
    p_mv.add_argument("slot", help="槽位名")
    p_mv.add_argument("old_path", help="原路径")
    p_mv.add_argument("tag", help="标签文本")
    p_mv.add_argument("new_path", help="新路径")

    p_add_cat = sub.add_parser("add-cat", help="新增分类")
    p_add_cat.add_argument("slot", help="槽位名")
    p_add_cat.add_argument("path", help="分类路径")

    p_rm_cat = sub.add_parser("rm-cat", help="删除空分类")
    p_rm_cat.add_argument("slot", help="槽位名")
    p_rm_cat.add_argument("path", help="分类路径")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "list":    cmd_list,
        "tree":    cmd_tree,
        "get":     cmd_get,
        "search":  cmd_search,
        "add":     cmd_add,
        "rm":      cmd_rm,
        "rename":  cmd_rename,
        "mv":      cmd_mv,
        "add-cat": cmd_add_cat,
        "rm-cat":  cmd_rm_cat,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
