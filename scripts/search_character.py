#!/usr/bin/env python3
"""Danbooru 角色百科搜索 —— 在 ZIP 压缩包内搜索角色信息，无需解压到文件系统。

用法:
  uv run scripts/search_character.py search <keyword>
"""

import argparse
import csv
import heapq
import json
import sys
from pathlib import Path

try:
    from rapidfuzz import fuzz
except ImportError:
    fuzz = None  # ty:ignore[invalid-assignment]

CSV_PATH = (
    Path(__file__).resolve().parent.parent / "tag-library" / "danbooru_character.csv"
)
CSV_NAME = "danbooru_character.csv"

SEARCH_FIELDS = ["character", "copyright", "trigger", "core_tags"]

_FULLWIDTH = str.maketrans(
    "０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",
    "0123456789abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz",
)


def normalize(s: str) -> str:
    return s.translate(_FULLWIDTH).lower().strip()


def open_reader():
    if not CSV_PATH.exists():
        download_name = "danbooru_character_webui.csv"
        print(
            f"缺失数据文件: {CSV_PATH}\n"
            f"请下载\n"
            f"  https://huggingface.co/datasets/Laxhar/noob-wiki/resolve/main/{download_name}\n"
            f"并保存为\n"
            f"  {CSV_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)
    text = CSV_PATH.open("r", encoding="utf-8")
    return csv.DictReader(text)


def search_rows(reader, keyword, fields, limit, threshold, use_exact):
    keyword_norm = normalize(keyword)
    heap = []
    counter = 0

    for row in reader:
        if use_exact:
            matched = any(keyword_norm in normalize(row.get(f, "")) for f in fields)
            score = 100.0 if matched else 0.0
        else:
            if fuzz is None:
                print(
                    "错误：需要 rapidfuzz 库（uv pip install rapidfuzz）",
                    file=sys.stderr,
                )
                sys.exit(1)
            score = max(
                (
                    fuzz.partial_ratio(keyword_norm, normalize(row.get(f, "")))
                    for f in fields
                ),
                default=0.0,
            )

        if score < threshold:
            continue

        row["_score"] = score
        counter += 1
        entry = (score, counter, row)
        if len(heap) < limit:
            heapq.heappush(heap, entry)
        elif score > heap[0][0]:
            heapq.heappushpop(heap, entry)

    results = sorted(heap, key=lambda x: (-x[0], x[1]))
    return [r for _, _, r in results]


def print_search_results(results, json_output):
    if json_output:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return

    if not results:
        print("无匹配结果")
        return

    for r in results:
        core = r.get("core_tags", "")[:60]
        print(f"  {r['character']:<30} {r['copyright']:<20} {r.get('_score', 0):>5.1f}")
        if core:
            print(f"  {'':>30} tags: {core}")
    print(f"\n共 {len(results)} 条结果")


def cmd_search(args):
    reader = open_reader()
    fields = (
        [f.strip() for f in args.fields.split(",")] if args.fields else SEARCH_FIELDS
    )
    results = search_rows(
        reader, args.keyword, fields, args.limit, args.threshold, args.exact
    )
    print_search_results(results, args.json)


def main():
    parser = argparse.ArgumentParser(
        description="在 danbooru_character.csv 中搜索角色信息",
    )
    sub = parser.add_subparsers(title="子命令", dest="subcommand", required=True)

    sp = sub.add_parser("search", help="模糊/精确搜索角色")
    sp.add_argument("keyword", help="搜索关键词")
    sp.add_argument(
        "--exact", action="store_true", help="精确子串匹配（默认 fuzzy partial_ratio）"
    )
    sp.add_argument(
        "--threshold", type=float, default=95.0, help="fuzzy 最低分数（默认 95）"
    )
    sp.add_argument(
        "--fields",
        default=None,
        help=f"搜索字段（逗号分隔），默认 {','.join(SEARCH_FIELDS)}",
    )
    sp.add_argument("--limit", type=int, default=10, help="返回条数（默认 10）")
    sp.add_argument("--json", action="store_true", help="JSON 输出")

    args = parser.parse_args()
    if args.subcommand == "search":
        cmd_search(args)


if __name__ == "__main__":
    main()
