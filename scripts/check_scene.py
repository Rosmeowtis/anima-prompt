#!/usr/bin/env python3
"""检查场景合理性 —— 场景标签与动作标签物理兼容。

用法:
  python check_scene.py <prompt>
  python check_scene.py <prompt> --json
"""

import argparse
import json
import sys

INCOMPATIBLE = [
    ({"underwater"}, {"cigarette"}, "水下不能抽烟"),
    ({"underwater"}, {"candle"}, "水下不能点蜡烛"),
    ({"underwater"}, {"fire"}, "水下不能有火"),
    ({"sleeping"}, {"standing"}, "睡眠中不能站立"),
    ({"sleeping"}, {"walking"}, "睡眠中不能行走"),
    ({"sleeping"}, {"running"}, "睡眠中不能跑步"),
    ({"sleeping"}, {"jumping"}, "睡眠中不能跳"),
    ({"swimming"}, {"lying"}, "游泳中不能躺着"),
    ({"outdoors"}, {"indoor"}, "室内外矛盾"),
    ({"day"}, {"night"}, "白天黑夜矛盾"),
    ({"sunlight"}, {"moonlight"}, "日光月光矛盾"),
    ({"rain"}, {"sunlight"}, "雨天烈日矛盾（排除太阳雨场景）"),
    ({"shower"}, {"completely dressed"}, "淋浴时不可能穿戴整齐"),
    ({"bath"}, {"shoes"}, "泡澡时不穿鞋"),
]


def check(prompt: str) -> dict:
    tags = [t.strip() for t in prompt.split(",") if t.strip()]
    tag_set = set(tags)
    issues = []
    for group_a, group_b, reason in INCOMPATIBLE:
        if (group_a & tag_set) and (group_b & tag_set):
            found_a = group_a & tag_set
            found_b = group_b & tag_set
            issues.append(f"{', '.join(found_a)} + {', '.join(found_b)} ({reason})")

    passed = len(issues) == 0
    detail = "; ".join(issues) if issues else "场景合理"
    return {"passed": passed, "detail": detail}


def main() -> None:
    parser = argparse.ArgumentParser(description="检查场景合理性")
    parser.add_argument("prompt", help="prompt 字符串")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = check(args.prompt)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "✓" if result["passed"] else "✗"
        print(f"{status} 场景合理性: {result['detail']}")
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
