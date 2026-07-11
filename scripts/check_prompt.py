#!/usr/bin/env python3
"""Prompt 总检查入口 —— 依次执行全部检查并输出 JSON 报告。

用法:
  python check_prompt.py "<prompt>"
  python check_prompt.py "<prompt>" --scene simple|standard|complex
  echo "<prompt>" | python check_prompt.py --stdin

依赖: check_count.py, check_conflict.py, check_duplicates.py,
      check_scene.py, check_lighting.py, check_tag_count.py
"""

import argparse
import json
import sys
from dataclasses import asdict

from _types import CheckResult, Report
from check_count import check as check_count
from check_conflict import check as check_conflict
from check_duplicates import check as check_duplicates
from check_scene import check as check_scene
from check_lighting import check as check_lighting
from check_tag_count import check as check_tag_count

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

CHECKS = [
    ("count",      check_count),
    ("conflict",   check_conflict),
    ("duplicates", check_duplicates),
    ("scene",      check_scene),
    ("lighting",   check_lighting),
    ("tag_count",  check_tag_count),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Anima Prompt 综合校验")
    parser.add_argument("prompt", nargs="?", default="", help="prompt 字符串")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读取 prompt")
    parser.add_argument("--scene", default="", choices=["simple", "standard", "complex"],
                        help="场景复杂度: simple=单人, standard=双人, complex=复杂")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
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
            if check_name == "tag_count":
                result = check_fn(prompt, args.scene)  # ty:ignore[too-many-positional-arguments]
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
