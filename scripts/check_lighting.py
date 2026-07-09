#!/usr/bin/env python3
"""校验光影标签 —— 识别并统计 prompt 中的光影标签。

光影标签现在已经允许使用。本脚本仅做统计报告，不拦截。
用法:
  python check_lighting.py <prompt>
  python check_lighting.py <prompt> --json
"""

import argparse
import json
import sys
from dataclasses import asdict

from _types import CheckResult

LIGHTING_TAGS = [
    "sunlight", "moonlight", "dim light", "candlelight",
    "neon light", "neon lights", "streetlight", "streetlights",
    "backlighting", "backlight", "rim light",
    "warm lighting", "cool lighting", "golden hour glow", "soft lighting",
    "warm tone", "cool tone", "sepia", "blue tone", "amber tone",
    "god rays", "light rays", "light particles",
    "volumetric light", "volumetric lighting", "tyndall effect",
    "glowing", "illuminated", "lit", "backlit", "spotlight",
    "flash photography", "ray tracing",
    "cinematic lighting", "ambient occlusion",
    "global illumination", "bloom",
    "lens flare",
    "depth of field",
    "bokeh",
    "subsurface scattering",
    "prism",
    "caustics", "refraction",
    "chromatic aberration",
    "glowing outlines", "holographic particles",
    "reflective wet ground",
    "neon haze",
    "transformation magic effect",
    "afterimage silhouette",
    "burst of light",
    "swirling light rings",
    "sparkling dust",
    "soft focus",
    "vignette",
]


def check(prompt: str) -> CheckResult:
    tags = [t.strip() for t in prompt.split(",") if t.strip()]
    found = []
    for tag in tags:
        if tag.lower() in LIGHTING_TAGS:
            found.append(tag)

    passed = True
    detail = f"光影标签 ({len(found)} 个): {', '.join(found)}" if found else "无光影标签"
    return CheckResult(passed=passed, detail=detail)


def main() -> None:
    parser = argparse.ArgumentParser(description="校验光影标签（仅统计，不拦截）")
    parser.add_argument("prompt", help="prompt 字符串")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = check(args.prompt)
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(f"✓ 光影校验: {result.detail}")
    sys.exit(0)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
