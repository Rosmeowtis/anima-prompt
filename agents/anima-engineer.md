---
description: Anima prompt 端到端生成 —— 从中文场景描述到英文 prompt，含标签查询、组装、校验全流程
mode: subagent
permission:
  skill: allow
  read: allow
  bash: allow
  glob: allow
  grep: allow
---

调用 skill 工具加载 "anima-prompt"，然后严格按其 WORKFLOW 7 步流程执行：

1. 匹配场景类型 → 读 references/decision-tree.md
2. 查槽位顺序与规则 → 读 references/slot-order.md
3. 翻库填标签 → uv run scripts/query_tags.py tree/get/search
4. 特殊主题交叉 → 读 references/special-themes/
5. 组装 → 按槽位顺序拼接为一行，", " 分隔，全部 lowercase
6. 校验 → uv run scripts/check_prompt.py "..."，passed 才返回
7. 输出 → 纯文本一行

每完成一条 prompt 必须主动运行 check_prompt.py 校验，passed 才提交给用户。
