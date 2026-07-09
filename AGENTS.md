# AGENTS.md — anima-prompt

本项目是一个 **OpenCode Skill 仓库**。`SKILL.md` 是主要交付物，`scripts/` 是其下层工具。

## 运行环境

- Python 3.11 (`.python-version`)，包管理用 `uv`（非 pip/poetry）
- 首次使用：`uv venv && uv pip install pyyaml rapidfuzz`
- 所有脚本通过 `uv run scripts/<name>.py` 执行

## 关键命令

| 命令 | 用途 |
|------|------|
| `uv run scripts/query_tags.py tree <slot>` | 查看槽位分类树 |
| `uv run scripts/query_tags.py get <slot> <path>` | 读取标签列表 |
| `uv run scripts/query_tags.py search <keyword>` | 搜索标签 |
| `uv run scripts/check_prompt.py "<prompt>"` | 六项校验（人数/冲突/重复/场景/灯光/标签数） |
| `uv run scripts/warehouse.py add/search/stats` | prompt 仓库管理 |

## 注意事项

- `--json` 参数必须放在子命令之前：`query_tags.py --json list`
- 写入操作 (add/rm/rename/mv) 自动生成 `.bak` 备份
- 编辑标签库通过脚本操作，**不要直接写 YAML**
- 无测试框架，无 CI
- `SKILL.md` 是核心交付物，修改前需确认与脚本能力一致
- `docs/` 为归档目录（原始教程留存），不修改其中的文件

## 关键路径

- Skill 本体: `SKILL.md`
- 标签库: `tag-library/` (8 个 YAML)
- 参考文件: `references/` (决策树、槽位顺序、冲突表、12 个特殊主题)
- 脚本工具: `scripts/` (9 个 .py)
- prompt 仓库: `warehouse/prompts.db` (SQLite FTS5)
