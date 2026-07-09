#!/usr/bin/env python3
"""检查灯光禁令 —— 确保无光线/光影/色调标签。

用法:
  python check_lighting.py <prompt>
  python check_lighting.py <prompt> --json
"""

import argparse
import json
import sys
from dataclasses import asdict

from _types import CheckResult

BANNED_PATTERNS = [
    "sunlight",
    "moonlight",
    "dim light",
    "candlelight",
    "neon light",
    "neon lights",
    "streetlight",
    "streetlights",
    "backlighting",
    "backlight",
    "rim light",
    "warm lighting",
    "cool lighting",
    "golden hour glow",
    "soft lighting",
    "warm tone",
    "cool tone",
    "sepia",
    "blue tone",
    "amber tone",
    "god rays",
    "light rays",
    "light particles",
    "volumetric light",
    "tyndall effect",
    "glowing",
    "illuminated",
    "lit",
    "spotlight",
    "flash photography",
    "ray tracing",
    "cinematic lighting",
    "ambient occlusion",
    "global illumination",
    "bloom",
]

ALLOWED_CARRYOVER = [
    "rain", "snow", "fog", "steam", "storm", "stormy",
    "dust particles", "underwater", "day", "night", "sunset", "twilight",
    "afternoon", "morning", "dark room", "dim lighting", "ambient light",
]


def check(prompt: str) -> CheckResult:
    tags = [t.strip() for t in prompt.split(",") if t.strip()]
    violations = []
    for tag in tags:
        for pattern in BANNED_PATTERNS:
            if pattern == tag.lower():
                violations.append(tag)
                break

    passed = len(violations) == 0
    detail = f"违禁标签: {', '.join(violations)}" if violations else "无违禁标签"
    return CheckResult(passed=passed, detail=detail)


def main() -> None:
    parser = argparse.ArgumentParser(description="检查灯光禁令")
    parser.add_argument("prompt", help="prompt 字符串")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = check(args.prompt)
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        status = "✓" if result.passed else "✗"
        print(f"{status} 灯光禁令: {result.detail}")
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
