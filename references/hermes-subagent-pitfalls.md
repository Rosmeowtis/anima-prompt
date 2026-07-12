# Hermes Subagent 实战经验

记录自 2026-07-11 实机测试（Builder → Drawer 全链路）。

## 🎭 角色名缺失 → 泛化猫娘

**故障**：Builder 生成了 `1girl, solo, white hair, green eyes, cat ears, cat tail, slim, white spaghetti strap dress...`，Drawer 出图后是"随机白发猫娘"，不是 Rosmontis。

**根因**：Builder 没有执行角色标签解析，只从 tag-library 里按外观词拼凑。没有 `rosmontis, arknights` 作为 IP 锚点，模型无法知道这是方舟角色。

**修复**：Builder 的 context 中加入 `resolve_cn_character.py` + `character_lib.py` 步骤，输出变为 `1girl, solo, rosmontis, arknights, long hair, white hair, green eyes, cat ears...`，Drawer 出图正确。

**教训**：**Builder 必须接收角色名提示**。主代理在组装 context 时，不要指望 subagent 自己猜到用户描述里的专名——直接把角色名显式填入指令里让 subagent 去查。

## 🖼️ Hermes Desktop 内嵌图片

Hermes desktop 的 delivery 机制中，以下格式可以内嵌显示：

- `MEDIA:/absolute/path/to/file.png` ✅ 内嵌渲染
- `![alt](file:///path)` ❌ 不显示
- `![alt](C:/path)` ❌ 不显示

注意路径是 Windows 绝对路径，正斜杠（`C:/Users/...`）或反斜杠（`C:\Users\...`）均可，但不支持相对路径。

## 🏗️ Builder 输出缺失 → 只输出校验结果不输出 prompt

**故障**：Builder 完成全部 7 步、校验通过后，输出的是 `All checks passed — 27 tags...` 而不是 prompt 本身。

**根因**：Subagent 将 check_prompt.py 的 stdout 当作了最终输出，压过了 prompt。OUTPUT CONSTRAINT 约束力度不够。

**修复**：在 context 的 WORKFLOW 步骤中追加硬约束：

```
## CRITICAL: YOU MUST OUTPUT THE PROMPT LINE
After validation passes, your ENTIRE response must be ONE LINE of plain text — the prompt.
NO status messages, NO "All checks passed", NO explanations. JUST THE PROMPT LINE.
```

**教训**：校验脚本的 stdout 可能被 subagent 误认为最终输出。在 context 中明确压制校验输出，或使用命令串联 + 重定向过滤掉非 prompt 行。

## 🐌 单后端限制 → 多图分批

**故障**：Anima API 后端只能一次处理一张图。并行提交多个 Drawer 会导致排队超时或卡住。

**做法**：Drawer 按顺序 one-by-one 提交。Builder 可并行（无后端瓶颈），Drawer 必须串行排队。

**教训**：多图场景下，Builder 全功率并行（max_concurrent_children=3），Drawer 逐个提交。可使用 `--output` 不同前缀避免覆盖。

## 🗺️ 可用 workflow 速查

| workflow | 模型 | LoRA | 生成速度 | 特点 |
|----------|------|------|----------|------|
| `workflows/t2i/AnimaApi.json` | `anima_baseV10` | 无 | ~50s | 原始工作流，纯 base 模型 |
| `workflows/t2i/美型Turbo.json` | `anima_baseV10` + Turbo | furrychoco, surtr, masterpiece×3 | **~10s** 🚀 | 质量词自动拼接，风格化更强 |

`美型Turbo.json` 的正面 prompt 由 `PrimitiveStringMultiline`（质量词）+ `StringConcatenate` + `__PROMPT__` （内容）拼接，使用 `call_anima.py` 时只需传内容标签，质量词自动保留。

## 🛠️ 自定义 workflow 的 `__PROMPT__` 要求

`call_anima.py` 在 workflow JSON 中递归搜索字符串 `__PROMPT__` 来确定注入位置。如果 workflow 用 `StringConcatenate` 节点拼接两段硬编码文本（如质量词 + 固定描述），则不会命中搜索，脚本报错退出。

**修复办法**：把 `StringConcatenate` 或 `PrimitiveStringMultiline` 中负责内容描述的节点的 `value` 改为 `"__PROMPT__"`。风格/质量词可保留硬编码。

## ℹ️ 命令调试环境

- 所有 Python 脚本用 `uv run scripts/xxx.py` 执行
- `call_anima.py` 默认 API 地址 `http://localhost:8188`，默认 workflow `workflows/t2i/AnimaApi.json`
- 仓库存档用 `uv run scripts/warehouse.py add "描述" "prompt" --type "类型"`
