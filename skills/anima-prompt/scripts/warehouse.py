#!/usr/bin/env python3
"""Prompt 仓库管理 —— SQLite + FTS5 全文搜索。

用法:
  python warehouse.py add <description> <prompt> --type <scene> [--theme <theme>]
  python warehouse.py search <keyword> [--limit 10] [--tag <tag>] [--type <scene>]
  python warehouse.py stats
  python warehouse.py export [--format json|csv] [--output <file>]
  python warehouse.py rm <id>
  python warehouse.py init
"""

import argparse
import json
import sqlite3
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

DB_PATH = Path(__file__).resolve().parent.parent / "warehouse" / "prompts.db"

SCHEMA = textwrap.dedent("""
    CREATE TABLE IF NOT EXISTS prompts (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        description   TEXT NOT NULL,
        prompt        TEXT NOT NULL,
        scene_type    TEXT,
        special_theme TEXT,
        tags          TEXT,
        tag_count     INTEGER DEFAULT 0,
        rating        INTEGER DEFAULT 0,
        created_at    TEXT DEFAULT (datetime('now')),
        notes         TEXT
    );
    CREATE VIRTUAL TABLE IF NOT EXISTS prompts_fts
        USING fts5(description, prompt, tags, content=prompts, content_rowid=id);
    CREATE TRIGGER IF NOT EXISTS prompts_ai AFTER INSERT ON prompts BEGIN
        INSERT INTO prompts_fts(rowid, description, prompt, tags)
        VALUES (new.id, new.description, new.prompt, new.tags);
    END;
    CREATE TRIGGER IF NOT EXISTS prompts_ad AFTER DELETE ON prompts BEGIN
        INSERT INTO prompts_fts(prompts_fts, rowid, description, prompt, tags)
        VALUES ('delete', old.id, old.description, old.prompt, old.tags);
    END;
    CREATE TRIGGER IF NOT EXISTS prompts_au AFTER UPDATE ON prompts BEGIN
        INSERT INTO prompts_fts(prompts_fts, rowid, description, prompt, tags)
        VALUES ('delete', old.id, old.description, old.prompt, old.tags);
        INSERT INTO prompts_fts(rowid, description, prompt, tags)
        VALUES (new.id, new.description, new.prompt, new.tags);
    END;
""")


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def cmd_init(args: argparse.Namespace) -> None:
    conn = get_db()
    conn.close()
    print(f"仓库已初始化: {DB_PATH}")


def cmd_add(args: argparse.Namespace) -> None:
    conn = get_db()
    tags_str = ", ".join(t.strip().lower() for t in args.prompt.split(",") if t.strip())
    tag_count = len([t for t in args.prompt.split(",") if t.strip()])
    conn.execute(
        "INSERT INTO prompts (description, prompt, scene_type, special_theme, tags, tag_count, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (args.description, args.prompt, args.type, args.theme, tags_str, tag_count,
         datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    print(f"已保存 #{row_id}: {args.description[:60]}")


def cmd_search(args: argparse.Namespace) -> None:
    conn = get_db()
    conditions = []
    params: list = []

    if args.tag:
        conditions.append("tags LIKE ?")
        params.append(f"%{args.tag}%")
    if args.type:
        conditions.append("scene_type = ?")
        params.append(args.type)

    if args.keyword:
        fts_cond = "prompts_fts MATCH ?"
        if conditions:
            where = "WHERE id IN (SELECT rowid FROM prompts_fts WHERE " + fts_cond + ") AND " + " AND ".join(conditions)
            params.insert(0, args.keyword)
        else:
            where = "WHERE id IN (SELECT rowid FROM prompts_fts WHERE " + fts_cond + ")"
            params.insert(0, args.keyword)
        query = f"SELECT * FROM prompts {where} ORDER BY created_at DESC LIMIT ?"
    else:
        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        query = f"SELECT * FROM prompts {where} ORDER BY created_at DESC LIMIT ?"

    params.append(args.limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()

    if not rows:
        print("无匹配结果")
        return

    for row in rows:
        print(f"#{row['id']} [{row['scene_type'] or '?'}] {row['description'][:80]}")
        print(f"    {row['prompt'][:120]}{'...' if len(row['prompt']) > 120 else ''}")
        if row.get("tags"):
            print(f"    tags: {row['tags'][:100]}")
        print()


def cmd_stats(args: argparse.Namespace) -> None:
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM prompts").fetchone()[0]
    print(f"总 prompt 数: {total}")

    print("\n场景类型分布:")
    rows = conn.execute(
        "SELECT scene_type, COUNT(*) as cnt FROM prompts GROUP BY scene_type ORDER BY cnt DESC"
    ).fetchall()
    for row in rows:
        print(f"  {row['scene_type'] or '(未分类)'}: {row['cnt']}")

    print("\n最近 10 条:")
    rows = conn.execute("SELECT id, description, created_at FROM prompts ORDER BY created_at DESC LIMIT 10").fetchall()
    for row in rows:
        print(f"  #{row['id']} {row['created_at'][:10]} {row['description'][:60]}")

    if total > 0:
        print("\n最常用标签 Top 15:")
        all_tags: list[str] = []
        for row in conn.execute("SELECT tags FROM prompts WHERE tags IS NOT NULL").fetchall():
            all_tags.extend(t.strip() for t in row["tags"].split(",") if t.strip())
        from collections import Counter
        for tag, cnt in Counter(all_tags).most_common(15):
            print(f"  {tag}: {cnt}")

    conn.close()


def cmd_export(args: argparse.Namespace) -> None:
    conn = get_db()
    rows = conn.execute("SELECT * FROM prompts ORDER BY created_at").fetchall()
    conn.close()

    data = [dict(row) for row in rows]

    if args.format == "csv":
        import csv
        import io
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        content = output.getvalue()
    else:
        content = json.dumps(data, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"已导出 {len(data)} 条到 {args.output}")
    else:
        print(content)


def cmd_rm(args: argparse.Namespace) -> None:
    conn = get_db()
    row = conn.execute("SELECT id, description FROM prompts WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"错误: 未找到 #{args.id}", file=sys.stderr)
        conn.close()
        sys.exit(1)
    conn.execute("DELETE FROM prompts WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"已删除 #{args.id}: {row['description'][:60]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Anima Prompt 仓库管理")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="初始化数据库")

    p_add = sub.add_parser("add", help="保存 prompt")
    p_add.add_argument("description", help="中文场景描述")
    p_add.add_argument("prompt", help="英文 prompt")
    p_add.add_argument("--type", default="", help="场景类型 (单人展示/双人正戏/...)")
    p_add.add_argument("--theme", default="", help="特殊主题 (NTR/BDSM/...)")

    p_search = sub.add_parser("search", help="搜索 prompt")
    p_search.add_argument("keyword", nargs="?", default="", help="搜索关键词")
    p_search.add_argument("--limit", type=int, default=10, help="返回数量")
    p_search.add_argument("--tag", default="", help="按标签筛选")
    p_search.add_argument("--type", default="", help="按场景类型筛选")

    p_stats = sub.add_parser("stats", help="统计概览")

    p_export = sub.add_parser("export", help="导出数据")
    p_export.add_argument("--format", default="json", choices=["json", "csv"])
    p_export.add_argument("--output", default="", help="输出文件路径")

    p_rm = sub.add_parser("rm", help="删除 prompt")
    p_rm.add_argument("id", type=int, help="prompt ID")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "init":   cmd_init,
        "add":    cmd_add,
        "search": cmd_search,
        "stats":  cmd_stats,
        "export": cmd_export,
        "rm":     cmd_rm,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
