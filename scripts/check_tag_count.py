#!/usr/bin/env python3
"""检查标签数量 —— 统计标签数并按复杂度分级校验。

用法:
  python check_tag_count.py <prompt> [--scene simple|standard|complex]
  python check_tag_count.py <prompt> --json
"""

import argparse
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

RANGES = {
    "simple":   (16, 30, "单人展示/诱惑/暴露/自慰"),
    "standard": (22, 38, "双人性交/前戏"),
    "complex":  (30, 48, "多人/特殊主题/剧情主视觉"),
}


def check(prompt: str, scene: str = "") -> dict:
    tags = [t.strip() for t in prompt.split(",") if t.strip()]
    count = len(tags)

    if scene and scene in RANGES:
        lo, hi, desc = RANGES[scene]
        passed = lo <= count <= hi
        detail = f"标签数={count}, 场景={desc}, 范围={lo}-{hi}"
    else:
        passed = True
        detail = f"标签数={count}"
        # 给出宽松建议
        if count < 10:
            detail += " (偏少)"
            passed = False
        elif count > 60:
            detail += " (偏多)"
            passed = False

    return {"passed": passed, "detail": detail, "count": count}


def main() -> None:
    parser = argparse.ArgumentParser(description="检查标签数量")
    parser.add_argument("prompt", help="prompt 字符串")
    parser.add_argument("--scene", default="", choices=["simple", "standard", "complex"],
                        help="场景复杂度")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = check(args.prompt, args.scene)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "✓" if result["passed"] else "✗"
        print(f"{status} 标签数量: {result['detail']}")
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
