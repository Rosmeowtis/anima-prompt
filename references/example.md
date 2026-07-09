# 完整示例

用户说：*"帮我生成一个金发双马尾女仆在教室里的 Anima prompt"*

LLM 执行：

```bash
# 1. 读决策树 → 单人展示类 → 槽位侧重在看
# 2. 翻库
uv run scripts/query_tags.py get count-identity "人数与性别/一女"
# → 1girl, solo

uv run scripts/query_tags.py get appearance "头发/颜色"
# → 选: blonde hair

uv run scripts/query_tags.py get appearance "头发/扎发编发"
# → 选: twin tails

uv run scripts/query_tags.py get clothing "服装类型/职业制服"
# → 选: maid outfit, maid headdress

uv run scripts/query_tags.py get scene-environment "半公开空间/教室"
# → 选: classroom, school desk

# 3. 组装
prompt = "1girl, solo, blonde hair, twin tails, maid outfit, maid headdress, standing, looking at viewer, from front, full body, classroom, school desk, afternoon"
# (12 标签 → 偏少，需要补表情+服装细节)

# 4. 补全
# 表情: blush, slight smile || 服装: white apron, frilled socks, mary janes || 细节: motion lines
prompt = "1girl, solo, blonde hair, twin tails, maid outfit, maid headdress, white apron, frilled socks, mary janes, standing, looking at viewer, blush, slight smile, from front, full body, classroom, school desk, afternoon, motion lines"
# (19 标签 → 在 16-30 范围内 ✅)

# 5. 校验
uv run scripts/check_prompt.py "1girl, solo, blonde hair, twin tails, maid outfit, maid headdress, white apron, frilled socks, mary janes, standing, looking at viewer, blush, slight smile, from front, full body, classroom, school desk, afternoon, motion lines" --scene simple

# 6. 输出
1girl, solo, blonde hair, twin tails, maid outfit, maid headdress, white apron, frilled socks, mary janes, standing, looking at viewer, blush, slight smile, from front, full body, classroom, school desk, afternoon, motion lines
```
