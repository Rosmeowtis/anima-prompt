# 完整示例

用户说：*"帮我生成一个金发双马尾女仆在教室里的 Anima prompt"*

LLM 执行：

```bash
# 1. 读决策树 → 单人展示类 → 槽位侧重在看
# 2. 读 slot-order.md → 确认槽位顺序：count-identity → appearance → clothing → pose-action → expression → camera-shot → scene-environment → detail-mood

# 3. 自由生成标签（按槽位顺序，LLM 自行选词）
prompt = "1girl, solo, blonde hair, twin tails, maid outfit, maid headdress, standing, looking at viewer, blush, slight smile, from front, full body, classroom, school desk, afternoon, motion lines"

# 4. 校验
uv run scripts/check_prompt.py "1girl, solo, blonde hair, twin tails, maid outfit, maid headdress, standing, looking at viewer, blush, slight smile, from front, full body, classroom, school desk, afternoon, motion lines"

# → {"passed": true, ...}

# 5. 输出
1girl, solo, blonde hair, twin tails, maid outfit, maid headdress, standing, looking at viewer, blush, slight smile, from front, full body, classroom, school desk, afternoon, motion lines
```
