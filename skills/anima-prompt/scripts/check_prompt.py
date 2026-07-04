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
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPTS_DIR = Path(__file__).resolve().parent

CHECKS = [
    ("count",     "check_count.py"),
    ("conflict",  "check_conflict.py"),
    ("duplicates","check_duplicates.py"),
    ("scene",     "check_scene.py"),
    ("lighting",  "check_lighting.py"),
    ("tag_count", "check_tag_count.py"),
]


def run_check(script: str, prompt: str, scene: str = "") -> dict:
    path = SCRIPTS_DIR / script
    cmd = [sys.executable, str(path), "--json", prompt]
    if scene and script == "check_tag_count.py":
        cmd.extend(["--scene", scene])
    try:
        result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", timeout=30)
        stdout = result.stdout.strip()
        if stdout:
            try:
                parsed = json.loads(stdout)
                return parsed
            except json.JSONDecodeError:
                pass
        return {"passed": False, "detail": result.stderr.strip() or stdout or f"{script} 无输出"}
    except subprocess.TimeoutExpired:
        return {"passed": False, "detail": f"{script} 执行超时"}
    except json.JSONDecodeError:
        return {"passed": False, "detail": f"{script}: {result.stdout[:200]}"}


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
    report = {"passed": True, "prompt": prompt, "tag_count": tag_count, "checks": {}}
    for check_name, script in CHECKS:
        result = run_check(script, prompt, args.scene)
        report["checks"][check_name] = result
        if not result.get("passed", False):
            report["passed"] = False

    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
