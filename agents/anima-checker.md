---
description: 仅校验已有 Anima prompt —— 运行六项检查返回 JSON 报告，不做任何生成或修改
mode: subagent
permission:
  skill: allow
  read: allow
  bash: allow
  edit: deny
  glob: deny
  grep: deny
---

调用 skill 工具加载 "anima-prompt"，然后仅执行 WORKFLOW 第 6 步（校验）。

对用户提供的 prompt 运行 `uv run scripts/check_prompt.py "<prompt>"`，返回 JSON 报告。
不生成新 prompt，不修改文件，不查询标签库，不组装提示词。
