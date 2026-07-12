#!/usr/bin/env python3
"""检查互斥冲突 —— 对照互斥表检查标签是否矛盾。

用法:
  python check_conflict.py <prompt>
  python check_conflict.py <prompt> --json
"""

import argparse
import json
import sys
from dataclasses import asdict

from _types import CheckResult

CONFLICT_PAIRS = [
    ("from front", "from behind", "视角矛盾"),
    ("from above", "from below", "视角矛盾"),
    ("looking at viewer", "facing away", "视线矛盾"),
    ("pov", "full body", "POV 不可能看到全身"),
    ("close-up", "full body", "景别矛盾"),
    ("solo", "hetero", "单人不存在互动"),
    ("solo", "yuri", "单人不存在百合互动"),
    ("femdom", "male-on-female rape", "主导方冲突"),
    ("sleeping", "looking at viewer", "无意识不可能直视"),
    ("unconscious", "looking at viewer", "无意识不可能直视"),
    ("blindfold", "heart-shaped pupils", "看不到眼睛"),
    ("blindfold", "rolling eyes", "看不到眼睛"),
    ("blindfold", "glasses", "物理冲突"),
    ("pantyhose", "barefoot", "穿丝袜不可能是光脚"),
    ("standing sex", "lying", "体位矛盾"),
    ("standing sex", "on back", "体位矛盾"),
    ("missionary", "doggystyle", "不可能同时两个体位"),
    ("cowgirl position", "prone bone", "体位矛盾"),
    ("fellatio", "cunnilingus", "嘴只有一张（单人执行）"),
    ("spread toes", "toe scrunch", "舒展 vs 蜷缩"),
    ("spread toes", "toes curling", "舒展 vs 蜷缩"),
    ("spread toes", "feet together", "分趾 vs 合拢"),
    ("spread fingers", "clenched fist", "张开 vs 握拳"),
    ("spread fingers", "gripping", "张开 vs 握抓"),
    ("bouncing breasts", "breasts squeeze together", "弹跳 vs 挤压"),
    ("open mouth", "clenched teeth", "张嘴 vs 闭嘴"),
    ("open mouth", "closed mouth", "张嘴 vs 闭嘴"),
    ("rolling eyes", "looking at viewer", "翻白眼 vs 直视"),
    ("spread legs", "legs together", "分开 vs 并拢"),
]


def check(prompt: str) -> CheckResult:
    tags = [t.strip() for t in prompt.split(",") if t.strip()]
    tag_set = set(tags)
    conflicts = []
    for a, b, reason in CONFLICT_PAIRS:
        if a in tag_set and b in tag_set:
            conflicts.append(f"{a} ❌ {b} ({reason})")

    passed = len(conflicts) == 0
    detail = "; ".join(conflicts) if conflicts else "无互斥冲突"
    return CheckResult(passed=passed, detail=detail)


def main() -> None:
    parser = argparse.ArgumentParser(description="检查标签互斥冲突")
    parser.add_argument("prompt", help="prompt 字符串")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = check(args.prompt)
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        status = "✓" if result.passed else "✗"
        print(f"{status} 互斥冲突: {result.detail}")
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
