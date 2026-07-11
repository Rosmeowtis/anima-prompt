# anima-prompt

将中文场景描述转写为 **Anima 模型** 的英文 prompt。

**警告**: 包含 NSFW 内容。

---

## 快速开始 / Quick Start

```bash
uv venv && uv pip install pyyaml
```

之后所有命令通过 `uv run scripts/xxx.py` 执行。All commands run via `uv run scripts/xxx.py`.

## 这是什么？/ What Is This?

anima-prompt 是一个 **OpenCode Skill** 工具仓库，专为 Anima3 二次元图像生成模型设计。它提供：

- **8 个槽位的标签库**（人数、外貌、服装、动作、表情、镜头、场景、氛围）
- **8 个 Python 脚本**：管理标签、校验 prompt、管理仓库、解析角色名
- **交互规则与互斥表**：自动检查人数/冲突/重复/场景/灯光/标签数
- **Prompt 仓库**：SQLite FTS5 全文搜索，沉淀高质量 prompt

This is an **OpenCode Skill** repository for the Anima3 anime image generation model, providing a tag library, validation tools, character name resolution, and a prompt warehouse.

## 项目结构

```
anima-prompt/
├── SKILL.md              # 核心 Skill 定义 — OpenCode 加载此文件
├── AGENTS.md             # AI 助手运行守则
├── pyproject.toml        # Python 依赖声明 (pyyaml)
├── .python-version       # Python 3.11
│
├── scripts/              # 8 个工具脚本
│   ├── manage_tags.py          # 标签库浏览(overview)+增删改移（禁止直接编辑 YAML）
│   ├── check_prompt.py        # 六项校验（人数/冲突/重复/场景/灯光/标签数）
│   ├── character_lib.py       # 角色标签搜索（danbooru ZIP）
│   ├── resolve_cn_character.py # 中文→英文角色名解析（Bangumi API）
│   ├── warehouse.py           # Prompt 仓库管理
│   ├── check_count.py / check_conflict.py / check_duplicates.py
│   ├── check_lighting.py / check_scene.py / check_tag_count.py
│   └── _types.py              # 类型定义
│
├── tag-library/           # 标签库 YAML（单文件，slot 名作顶层 key）
│   ├── tags.yaml              # 全量标签（8 槽位树结构合并）
│   ├── cn_char_map.yaml       # 中文→英文角色名缓存
│   ├── extra_characters.csv   # 额外角色数据
│   └── danbooru_character.zip # Danbooru 角色数据
│
├── references/           # 参考文档
│   ├── decision-tree.md       # 场景类型决策树
│   ├── slot-order.md          # 槽位顺序与标签数量约束
│   ├── conflict-table.md      # 互斥冲突表
│   ├── style-optimization.md  # 服装升维/表情拆解
│   ├── example.md             # 完整输出示例
│   └── special-themes/        # 12 个特殊主题配方（NTR/BDSM/隐奸…）
│
├── agents/               # OpenCode Subagent 模板
│   └── anima-engineer.md / anima-checker.md
│
├── docs/                 # 归档教程（原始文档）
├── warehouse/            # Prompt 仓库 (SQLite)
└── AI 助手配置
    ├── AGENTS.md
    └── .serena/
```

## 核心工作流

```
1. 决策树匹配场景类型
2. 查槽位顺序与标签数量约束
3. 逐槽位填充标签
4. 特殊主题交叉（如 NTR/BDSM）
5. 按槽位顺序组装为一行
6. 六项校验 → 通过
7. 输出纯文本 prompt
```

详见 `SKILL.md` 中的完整 WORKFLOW。

## 常用命令 / Common Commands

| 用途 | 命令 |
|------|------|
| 浏览目录结构 | `uv run scripts/manage_tags.py overview [--slot <name>]` |
| 添加标签 | `uv run scripts/manage_tags.py add <slot> <path> <tag>` |
| 删除标签 | `uv run scripts/manage_tags.py rm <slot> <path> <tag>` |
| 重命名标签 | `uv run scripts/manage_tags.py rename <slot> <path> <old> <new>` |
| 六项校验 | `uv run scripts/check_prompt.py "<prompt>" --scene <scene>` |
| 中文角色名解析 | `uv run scripts/resolve_cn_character.py <中文名>` |
| 角色标签查询 | `uv run scripts/character_lib.py search <name> --exact` |
| Prompt 仓库保存 | `uv run scripts/warehouse.py add <描述> <prompt> --type <场景>` |
| 仓库搜索 | `uv run scripts/warehouse.py search <keyword>` |

## 在 OpenCode 中使用

作为 Skill 加载（自动识别）：OpenCode 读取 `SKILL.md`。

可选安装 Subagent：

```bash
cp agents/anima-engineer.md .opencode/agents/
cp agents/anima-checker.md .opencode/agents/
```

之后可通过 `@anima-engineer` 端到端生成、`@anima-checker` 仅校验。

## 技术依赖 / Dependencies

- **Python** >= 3.10（推荐 3.11）
- **uv** — Python 包管理器（非 pip）
- **pyyaml** — YAML 解析
- **SQLite FTS5** — Prompt 仓库全文搜索（Python 内置）

## 许可 / License

想干嘛干嘛 / WTF