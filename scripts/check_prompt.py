#!/usr/bin/env python3
"""Prompt 总检查入口 —— 依次执行全部检查并输出 JSON 报告。

用法:
  python check_prompt.py "<prompt>"
  echo "<prompt>" | python check_prompt.py --stdin

依赖: check_nsfw.py, check_count.py, check_conflict.py,
      check_duplicates.py, check_scene.py, check_lighting.py
"""

import argparse
import json
import sys
from dataclasses import asdict

from _types import CheckResult, Report
from check_count import check as check_count
from check_conflict import check as check_conflict
from check_duplicates import check as check_duplicates
from check_nsfw import check as check_nsfw
from check_scene import check as check_scene
from check_lighting import check as check_lighting


sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

CHECKS = [
    ("nsfw",       check_nsfw),
    ("count",      check_count),
    ("conflict",   check_conflict),
    ("duplicates", check_duplicates),
    ("scene",      check_scene),
    ("lighting",   check_lighting),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Anima Prompt 综合校验")
    parser.add_argument("prompt", nargs="?", default="", help="prompt 字符串")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读取 prompt")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--nsfw", action="store_true", help="NSFW 模式：允许 NSFW 标签")
    args = parser.parse_args()

    prompt = args.prompt
    if args.stdin:
        prompt = sys.stdin.read().strip()
    if not prompt:
        print("错误: 请提供 prompt 或使用 --stdin", file=sys.stderr)
        sys.exit(1)

    tag_count = len([t.strip() for t in prompt.split(",") if t.strip()])
    report = Report(passed=True, prompt=prompt, tag_count=tag_count, checks={})
    for check_name, check_fn in CHECKS:
        try:
            if check_name == "nsfw" and args.nsfw:
                # NSFW mode: run check but never fail — just count for info
                raw = check_nsfw(prompt)
                result = CheckResult(passed=True, detail=f"NSFW 模式: {raw.detail}", count=raw.count)
            else:
                result = check_fn(prompt)
        except Exception as e:
            result = CheckResult(passed=False, detail=f"执行异常: {e}")
        report.checks[check_name] = result
        if not result.passed:
            report.passed = False

    print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
