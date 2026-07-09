#!/usr/bin/env python3
"""将中文角色名解析为 danbooru 蛇形命名（本地缓存 + Bangumi API）。

默认仅查本地缓存，未命中时提示使用 --bangumi 调用 API 查询并自动写入缓存。

输出 danbooru_name（如 "hatsune_miku"），可 pipe 到 character_lib.py：
  uv run scripts/resolve_cn_character.py 初音未来 | xargs uv run scripts/character_lib.py search {} --exact --limit 1 --json

用法:
  uv run scripts/resolve_cn_character.py <中文名>
  uv run scripts/resolve_cn_character.py 初音未来 --json
  uv run scripts/resolve_cn_character.py 迷迭香 --bangumi
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

CACHE_PATH = Path(__file__).resolve().parent.parent / "tag-library" / "cn_char_map.yaml"
BANGUMI_API = "https://api.bgm.tv/v0/search/characters"
USER_AGENT = "anima-prompt/1.0"


def load_cache():
    if not CACHE_PATH.exists():
        return {}
    with open(CACHE_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_cache(cache):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        yaml.dump(cache, f, allow_unicode=True, default_flow_style=False)


def bangumi_search(keyword):
    data = json.dumps({"keyword": keyword}).encode("utf-8")
    req = urllib.request.Request(
        BANGUMI_API,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8")).get("data", [])
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        print(f"网络错误: {e}", file=sys.stderr)
        sys.exit(1)


def extract_name(infobox):
    for item in infobox:
        if item.get("key") != "别名":
            continue
        aliases = item.get("value", [])
        for priority in ("罗马字", "英文名"):
            for alias in aliases:
                if alias.get("k") == priority:
                    return priority, alias.get("v", "")
    return None, None


def to_snake(name):
    return name.lower().strip().replace(" ", "_").replace("-", "_")


def resolve(keyword):
    results = bangumi_search(keyword)
    if not results:
        return None, None, None

    for bgm_char in results:
        source, extracted = extract_name(bgm_char.get("infobox", []))
        if not extracted:
            continue
        return source, extracted, to_snake(extracted)

    return None, None, None


def main():
    parser = argparse.ArgumentParser(
        description="中文角色名 → danbooru 蛇形命名"
    )
    parser.add_argument("keyword", help="中文角色名")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument(
        "--bangumi", action="store_true",
        help="未命中缓存时调用 Bangumi API 查询并自动写入缓存",
    )
    args = parser.parse_args()

    cache = load_cache()
    keyword = args.keyword

    if keyword in cache:
        name = cache[keyword]
        if args.json:
            json.dump({"chinese_name": keyword, "danbooru_name": name}, sys.stdout, ensure_ascii=False)
            print()
        else:
            print(name, end="")
        return

    if not args.bangumi:
        print(
            f"未在本地缓存中找到: {keyword}\n"
            f"  使用 --bangumi 参数调用 Bangumi API 查询并自动缓存",
            file=sys.stderr,
        )
        sys.exit(1)

    source, extracted, danbooru_name = resolve(keyword)

    if danbooru_name:
        cache[keyword] = danbooru_name
        save_cache(cache)
        if args.json:
            json.dump({
                "chinese_name": keyword,
                "source": source,
                "extracted": extracted,
                "danbooru_name": danbooru_name,
            }, sys.stdout, ensure_ascii=False, indent=2)
            print()
        else:
            print(danbooru_name, end="")
    else:
        if source is None and extracted is None:
            print(
                f"Bangumi 找到角色但无罗马字/英文名: {keyword}\n"
                f"  可手动编辑 {CACHE_PATH} 补录映射",
                file=sys.stderr,
            )
        else:
            print(f"未在 Bangumi 找到角色: {keyword}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
