#!/usr/bin/env python3
"""
向远程 Anima API (ComfyUI) 发送 workflow 并接收生成图像。

功能：
  - 加载 workflow JSON，自动发现 __PROMPT__ 占位符和 EmptyLatentImage 节点
  - 注入 prompt、width、height 三个参数
  - 自动随机化 KSampler/KSamplerAdvanced 的 seed（避免连续相同参数导致后端不返回图像）
  - 提交任务 → 轮询结果 → 下载图像
  - 输出目录图片数量限制（超出自动清理旧文件）
"""

import argparse
import json
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RATIO_MAP = {
    "1:1": (1536, 1536),
    "16:9": (2048, 1152),
    "9:16": (1152, 2048),
    "4:3": (1792, 1344),
    "3:4": (1344, 1792),
    "3:2": (1920, 1280),
    "2:3": (1280, 1920),
    "5:4": (1728, 1376),
    "4:5": (1376, 1728),
}

POLL_INTERVAL = 10
MAX_POLLS = 30
REQUEST_TIMEOUT = 120
MAX_IMAGES = 50
SEED_MAX = 2**53 - 1


def _nested_set(obj, keys, value):
    for k in keys[:-1]:
        obj = obj[k]
    obj[keys[-1]] = value


def _prune_dir(output_dir, max_count):
    if not output_dir.exists():
        return
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    images = sorted(
        [p for p in output_dir.iterdir() if p.suffix.lower() in exts],
        key=lambda p: p.stat().st_mtime,
    )
    for p in images[:-max_count]:
        p.unlink()


def _find_str_containing(d, target):
    """递归搜索 dict d 中所有字符串值，返回第一个包含 target 的路径和值。"""
    for k, v in d.items():
        if isinstance(v, str) and target in v:
            return [k], v
        if isinstance(v, dict):
            result = _find_str_containing(v, target)
            if result:
                inner_path, inner_val = result
                return [k] + inner_path, inner_val
    return None


def _find_prompt_path(wf):
    for node_id, node in wf.items():
        if not isinstance(node, dict) or "inputs" not in node:
            continue
        result = _find_str_containing(node["inputs"], "__PROMPT__")
        if result:
            key_path, _ = result
            return [node_id, "inputs"] + key_path
    print("错误: workflow 中未找到 __PROMPT__ 占位符", file=sys.stderr)
    sys.exit(1)


def _find_latent_path(wf):
    matches = [
        node_id
        for node_id, node in wf.items()
        if isinstance(node, dict) and node.get("class_type") == "EmptyLatentImage"
    ]
    if len(matches) != 1:
        print(
            f"错误: 需要 1 个 EmptyLatentImage 节点，实际找到 {len(matches)} 个",
            file=sys.stderr,
        )
        sys.exit(1)
    return [matches[0], "inputs"]


def _find_seed_paths(wf):
    paths = []
    for node_id, node in wf.items():
        if not isinstance(node, dict) or "inputs" not in node:
            continue
        ct = node.get("class_type", "")
        if ct not in ("KSampler", "KSamplerAdvanced"):
            continue
        if "seed" in node["inputs"] and isinstance(node["inputs"]["seed"], int):
            paths.append([node_id, "inputs", "seed"])
    if not paths:
        print(
            "警告: workflow 中未找到 KSampler/KSamplerAdvanced 节点，seed 未随机化",
            file=sys.stderr,
        )
    return paths


def prepare_workflow(workflow_path, prompt, width, height):
    path = Path(workflow_path)
    if not path.exists():
        print(f"workflow 文件不存在: {path}", file=sys.stderr)
        sys.exit(1)
    wf = json.loads(path.read_text(encoding="utf-8"))

    p_path = _find_prompt_path(wf)
    l_path = _find_latent_path(wf)
    seeds = _find_seed_paths(wf)

    _nested_set(wf, p_path, prompt)
    _nested_set(wf, l_path + ["width"], width)
    _nested_set(wf, l_path + ["height"], height)
    for sp in seeds:
        _nested_set(wf, sp, random.randint(0, SEED_MAX))
    return wf


def _json_req(url, data=None):
    """发送 JSON 请求并解析 JSON 响应。"""
    body = json.dumps(data).encode("utf-8") if data else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"API 错误 ({e.code}): {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"连接失败: {e.reason}", file=sys.stderr)
        sys.exit(1)


def _bin_req(url):
    """发送 GET 并返回二进制内容。"""
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        print(f"下载失败 ({e.code}): {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"下载连接失败: {e.reason}", file=sys.stderr)
        sys.exit(1)


def parse_args():
    p = argparse.ArgumentParser(description="向远程 Anima API 发送 workflow 并接收图像")
    p.add_argument("-p", "--prompt", required=True, help="替换 __PROMPT__ 的文本")
    p.add_argument(
        "-r",
        "--ratio",
        default="1:1",
        choices=sorted(RATIO_MAP.keys()),
        help="画面比例（默认 1:1）",
    )
    p.add_argument("--api-url", default="http://localhost:8188", help="Anima API 地址")
    p.add_argument(
        "-w",
        "--workflow",
        default="workflows/t2i/AnimaApi.json",
        help="workfow JSON 路径",
    )
    p.add_argument("-o", "--output", default="./outputs", help="图像保存目录")
    return p.parse_args()


def post_prompt(api_url, workflow):
    resp = _json_req(f"{api_url}/prompt", {"prompt": workflow})
    rid = resp.get("prompt_id")
    if not rid:
        print(f"响应缺少 prompt_id: {resp}", file=sys.stderr)
        sys.exit(1)
    print(f"任务已提交，prompt_id: {rid}")
    return rid


def poll_history(api_url, prompt_id):
    url = f"{api_url}/history/{prompt_id}"
    for i in range(MAX_POLLS):
        time.sleep(POLL_INTERVAL)
        data = _json_req(url)
        history = data.get(prompt_id)
        if not history:
            continue
        status = history.get("status", {})
        if status.get("completed") or status.get("status_str") == "success":
            print(f"生成完成（耗时约 {(i + 1) * POLL_INTERVAL}s）")
            return history
        if history.get("errors"):
            print(f"生成出错: {history['errors']}", file=sys.stderr)
            sys.exit(1)
    print("超时: 生成未在预期时间内完成", file=sys.stderr)
    sys.exit(1)


def download_images(api_url, history, output_dir, prompt):
    outputs = history.get("outputs", {})
    count = 0
    for node_out in outputs.values():
        for img in node_out.get("images", []):
            filename = img["filename"]
            params = f"filename={filename}&type={img.get('type', 'output')}"
            if img.get("subfolder"):
                params += f"&subfolder={img['subfolder']}"
            data = _bin_req(f"{api_url}/view?{params}")
            out_path = output_dir / filename
            out_path.write_bytes(data)
            print(f"已保存：{out_path.resolve()}")
            print("提示词：")
            print(prompt)
            _prune_dir(output_dir, MAX_IMAGES)
            count += 1
    return count


def main():
    args = parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    w, h = RATIO_MAP[args.ratio]
    wf = prepare_workflow(args.workflow, args.prompt, w, h)

    api_url = args.api_url.rstrip("/")
    rid = post_prompt(api_url, wf)
    history = poll_history(api_url, rid)
    n = download_images(api_url, history, output_dir, args.prompt)
    if n == 0:
        print("警告: 未下载到任何图像", file=sys.stderr)


if __name__ == "__main__":
    main()
