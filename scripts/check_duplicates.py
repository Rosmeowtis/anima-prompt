#!/usr/bin/env python3
"""检查重复标签。

用法:
  python check_duplicates.py <prompt>
  python check_duplicates.py <prompt> --json
"""

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict

from _types import CheckResult


def check(prompt: str) -> CheckResult:
    tags = [t.strip() for t in prompt.split(",") if t.strip()]
    counter = Counter(tags)
    dups = [tag for tag, count in counter.items() if count > 1]
    passed = len(dups) == 0
    detail = f"重复标签: {', '.join(dups)}" if dups else "无重复"
    return CheckResult(passed=passed, detail=detail)


def main() -> None:
    parser = argparse.ArgumentParser(description="检查重复标签")
    parser.add_argument("prompt", help="prompt 字符串")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = check(args.prompt)
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        status = "✓" if result.passed else "✗"
        print(f"{status} 重复检查: {result.detail}")
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
