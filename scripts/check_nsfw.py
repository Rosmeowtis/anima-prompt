#!/usr/bin/env python3
"""NSFW 标签检测 —— 检查 prompt 中是否含 NSFW 标签。

用法:
  uv run scripts/check_nsfw.py "<prompt>"
  uv run scripts/check_nsfw.py "<prompt>" --json
"""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import yaml

from _types import CheckResult

TAGS_DIR = Path(__file__).resolve().parent.parent / "tag-library"
NSFW_PATH = TAGS_DIR / "tags_nsfw.yaml"
SFW_PATH = TAGS_DIR / "tags_sfw.yaml"


def _extract_tags(path: Path) -> set[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    tags: set[str] = set()

    def _walk(node):
        if isinstance(node, list):
            for item in node:
                if isinstance(item, str):
                    tags.add(item)
        elif isinstance(node, dict):
            for v in node.values():
                _walk(v)

    _walk(data)
    return tags


def _load_nsfw_tags() -> set[str]:
    """取 NSFW 标签集，排除也出现在 SFW 中的（避免共享标签误报）。"""
    nsfw = _extract_tags(NSFW_PATH)
    sfw = _extract_tags(SFW_PATH)
    return nsfw - sfw


_NSFW_CACHE: set[str] | None = None


def check(prompt: str) -> CheckResult:
    global _NSFW_CACHE
    if _NSFW_CACHE is None:
        _NSFW_CACHE = _load_nsfw_tags()

    tags = [t.strip() for t in prompt.split(",") if t.strip()]
    found = [t for t in tags if t in _NSFW_CACHE]

    passed = len(found) == 0
    count = len(found)
    detail = f"含 {count} 个 NSFW 标签" if found else "无 NSFW 标签"
    return CheckResult(passed=passed, detail=detail, count=count)


def main() -> None:
    parser = argparse.ArgumentParser(description="NSFW 标签检测")
    parser.add_argument("prompt", nargs="?", default="", help="prompt 字符串")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读取 prompt")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    prompt = args.prompt
    if args.stdin:
        prompt = sys.stdin.read().strip()
    if not prompt:
        print("错误: 请提供 prompt 或使用 --stdin", file=sys.stderr)
        sys.exit(1)

    result = check(prompt)
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        status = "✓" if result.passed else "✗"
        print(f"{status} NSFW: {result.detail}")
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
