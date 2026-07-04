#!/usr/bin/env python3
"""检查人数一致性 —— 验证 count/gender 标签与实际角色数一致。

用法:
  python check_count.py <prompt>
  python check_count.py <prompt> --json
"""

import argparse
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

GENDER_COUNT_MAP = {
    "1girl":   (1, "f"),
    "2girls":  (2, "f"),
    "3girls":  (3, "f"),
    "4girls":  (4, "f"),
    "5girls":  (5, "f"),
    "1boy":    (1, "m"),
    "2boys":   (2, "m"),
    "3boys":   (3, "m"),
    "4boys":   (4, "m"),
    "5boys":   (5, "m"),
}
X_PATTERN = re.compile(r"^(\d+)(girls?|boys?)$")

CONTRADICTIONS = [
    ({"solo"}, {"hetero", "1boy", "yuri", "2girls", "2boys"}),
    ({"hetero"}, {"yuri"}),
]


def check(prompt: str) -> dict:
    tags = [t.strip() for t in prompt.split(",") if t.strip()]
    tag_set = set(tags)
    errors = []

    total_girls = 0
    total_boys = 0
    found_explicit = False

    for tag in tags:
        if tag in GENDER_COUNT_MAP:
            count, gender = GENDER_COUNT_MAP[tag]
            found_explicit = True
            if gender == "f":
                total_girls += count
            else:
                total_boys += count
        else:
            m = X_PATTERN.match(tag)
            if m:
                count = int(m.group(1))
                found_explicit = True
                if "girl" in m.group(2):
                    total_girls += count
                else:
                    total_boys += count

    if "solo" in tag_set and total_girls == 0:
        total_girls = 1

    if total_girls == 0 and total_boys == 0 and ("solo" not in tag_set):
        if found_explicit:
            errors.append("无法解析具体人数")

    for a_set, b_set in CONTRADICTIONS:
        if (a_set & tag_set) and (b_set & tag_set):
            errors.append(f"{', '.join(a_set)} 与 {', '.join(b_set)} 互斥")

    if "solo" in tag_set and total_boys > 0:
        errors.append("solo 与男性角色矛盾")

    if total_girls == 0 and total_boys == 0 and not errors:
        return {"passed": True, "detail": "无显式人数标签，跳过检查"}

    passed = len(errors) == 0
    detail = ", ".join(errors) if errors else f"角色数: 女={total_girls}, 男={total_boys}"
    return {"passed": passed, "detail": detail}


def main() -> None:
    parser = argparse.ArgumentParser(description="检查人数一致性")
    parser.add_argument("prompt", help="prompt 字符串")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = check(args.prompt)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "✓" if result["passed"] else "✗"
        print(f"{status} 人数一致性: {result['detail']}")
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
