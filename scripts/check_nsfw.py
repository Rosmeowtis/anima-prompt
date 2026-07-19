#!/usr/bin/env python3
"""NSFW 标签检测 —— 硬编码关键词，零外部依赖。

用法:
  uv run scripts/check_nsfw.py "<prompt>"
  uv run scripts/check_nsfw.py "<prompt>" --json

筛选原则: 只收无论如何都不可能是 SFW 的关键词。
  收: 性器官、性行为、性体液、性玩具
  不收: nipple/cleavage/spread legs/nude/ahegao/blush/sweat/tears 等存在 SFW 上下文的标签
"""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _types import CheckResult

# === 唯一数据源: 硬编码 NSFW 关键词 ===
# ponytail: ~80 个关键词，删掉原 YAML 加载。新增关键词时直接加到这里。
NSFW_KEYWORDS: set[str] = {
    # -- 性器官 --
    "penis", "huge penis", "gigantic penis", "very big penis",
    "small penis", "tiny penis", "mini penis", "veiny penis",
    "pussy", "puffy pussy", "dark pussy", "pussy gaping",
    "vagina", "vaginal opening", "vulva", "labia",
    "clitoris", "huge clitoris", "erect clitoris", "clitoral hood",
    "pierced clitoris", "clitoris rings",
    "cervix", "uterus", "ovaries", "fallopian tubes",
    "urethra", "perineum", "cleft of venus",
    "anus", "puffy anus", "dark anus",
    "testicles", "huge testicles", "long testicles",
    "foreskin", "phimosis", "erection",
    "penis and vagina", "large breasts + penis",
    "female pubic hair", "stray pubic hair",

    # -- 性行为 --
    "fellatio", "cunnilingus", "anilingus",
    "paizuri", "handjob", "footjob", "facesitting",
    "missionary", "doggystyle", "reverse doggystyle",
    "cowgirl position", "reverse cowgirl position",
    "prone bone", "mating press",
    "full nelson position", "amazon position", "anvil position",
    "standing missionary", "suspended congress",
    "piledriver", "spitroast",
    "gangbang", "group sex", "after gangbang",
    "double penetration", "triple penetration", "vaginal + anal",
    "deepthroat", "irrumatio", "face fucking",
    "skull fucking", "throat fucking",
    "rimming", "ass-to-ass",
    "sex from behind", "rough sex", "rape", "assisted rape",
    "stealth sex", "implied sex", "expressionless sex",
    "masturbation", "fingering", "clothed masturbation",
    "cervical penetration", "deep penetration",
    "imminent penetration", "just the tip",
    "orgasm", "female ejaculation", "squirting",
    "in heat", "after sex", "after fellatio",
    "trombone",

    # -- 性体液 --
    "cum", "precum", "creampie", "bukkake",
    "cum inside", "cum overflow", "cum drip", "cum string",
    "cum pool", "cum bath", "excessive cum",
    "cum on body", "cum on face", "cum on breasts",
    "cum on hair", "cum on clothes",
    "cum in mouth", "cum covered", "cum dump",
    "cum bubble", "vomiting cum", "cum silk",
    "pussy juice", "pussy juice pool",
    "pussy juice stain", "pussy juice trail",
    "ejaculation", "gokkun", "facial",

    # -- 性玩具 / 性道具 --
    "dildo", "double dildo", "vibrator", "wand vibrator",
    "anal beads", "artificial vagina",
    "ball gag", "penis gag",
    "condom", "used condom", "many used condoms",
    "glory wall",

    # -- 明确性状态 --
    "futanari",
    "fucked silly", "mind break",
    "corruption", "bimbofication",
    "woman hypnotized lewd", "instant loss",
    "cum dump",

    # -- BDSM (性向明确) --
    "shibari", "kinbaku",
    "crotch tattoo", "pubic tattoo",
}


def check(prompt: str) -> CheckResult:
    tags = [t.strip() for t in prompt.split(",") if t.strip()]
    found = [t for t in tags if t in NSFW_KEYWORDS]

    passed = len(found) == 0
    count = len(found)
    detail = f"含 {count} 个 NSFW 标签：<{', '.join(found)}>" if found else "无 NSFW 标签"
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
