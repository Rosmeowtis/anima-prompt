# 表情符号参考文档

常见的 ASCII 颜文字和 Unicode Emoji，可用于 Anima/NAI/SD 的 prompt 表情控制。

---

## 一、表情分类速查

### 1.1 开心/愉悦

| 表情 | 类型 | 含义 | 建议场景 |
|------|------|------|---------|
| `^_^` | ASCII | 开心眯眼，温柔笑 | 日常微笑、温顺 |
| `:D` | ASCII | 张嘴大笑 | 兴奋、开朗 |
| `:3` | ASCII | 猫嘴笑，小得意 | 撒娇、调皮 |
| `>w<` | ASCII | 开心到脸颊鼓起，羞萌 | 被夸奖后害羞开心 |
| `UwU` | ASCII | 可爱开心，卖萌 | 撒娇、装可爱 |
| `😁` | Unicode | 露齿笑，灿烂 | 阳光开朗 |
| `😊` | Unicode | 微笑带红晕，含蓄 | 礼貌微笑、含羞 |
| `😏` | Unicode | 单边嘴角上扬，得意 | 挑逗、自信、坏笑 |

### 1.2 惊讶/困惑

| 表情 | 类型 | 含义 | 建议场景 |
|------|------|------|---------|
| `O_O` | ASCII | 瞪大眼震惊 | 突发事件吓到，震惊 |
| `o_O` | ASCII | 困惑挑眉 | 不理解、疑惑 |
| `@_@` | ASCII | 眼花缭乱 | 信息过载、天旋地转 |
| `OwO` | ASCII | 好奇睁大眼 | 好奇、发现有趣事物 |
| `D:` | ASCII | 惊恐张嘴 | 惊吓、手足无措 |
| `😱` | Unicode | 惊恐尖叫 | 极度震惊、恐怖 |
| `😨` | Unicode | 害怕缩脖 | 畏惧、不安 |
| `😰` | Unicode | 焦虑冒汗 | 紧张、担心、冒冷汗 |

### 1.3 挫败/疲惫

| 表情 | 类型 | 含义 | 建议场景 |
|------|------|------|---------|
| `>_<` | ASCII | 抓狂、窘迫 | 被为难、不知所措 |
| `T_T` | ASCII | 哭泣、绝望 | 大哭、伤心 |
| `T~T` | ASCII | 含泪、欲哭 | 眼眶湿润、忍住不哭 |
| `;_;` | ASCII | 流泪、抽泣 | 委屈、偷偷哭 |
| `Q_Q` | ASCII | 哭泣（眼含泪花） | 可怜巴巴 |
| `-_-` | ASCII | 无语、冷漠 | 无奈、懒得理 |
| `v_v` | ASCII | 垂头丧气 | 失落、被训斥 |
| `>_>` | ASCII | 侧目、斜眼 | 怀疑、嫌弃 |
| `X_X` | ASCII | 晕死、失去意识 | 昏倒、被击倒 |
| `>: ` | ASCII | 恼怒、不爽 | 不耐烦、面色不善 |  <!-- intentionally with trailing space -->
| `>:D` | ASCII | 邪恶大笑 | 腹黑、得逞、恶作剧成功 |
| `😢` | Unicode | 含泪欲泣 | 悲伤、难过 |
| `😭` | Unicode | 嚎啕大哭 | 极度悲伤、崩溃 |
| `🥺` | Unicode | 水汪汪求饶 | 可怜请求、装可怜 |
| `😤` | Unicode | 不服气 | 气鼓鼓、不甘心 |
| `😠` | Unicode | 生气怒视 | 愤怒、不满 |
| `😡` | Unicode | 暴怒红脸 | 极度愤怒 |
| `😑` | Unicode | 面无表情 | 冷漠、生无可恋 |
| `😌` | Unicode | 松了口气 | 如释重负、欣慰 |

### 1.4 特殊状态

| 表情 | 类型 | 含义 | 建议场景 |
|------|------|------|---------|
| `😴` | Unicode | 睡觉 | 睡眠中、昏迷 |
| `😈` | Unicode | 恶魔微笑 | 腹黑、恶作剧 |
| `😅` | Unicode | 尴尬冷汗 | 尴尬、勉强 |
| `🤤` | Unicode | 流口水 | 馋、看到喜欢的人/物 |
| `😳` | Unicode | 脸红震惊 | 害羞、被说中心事 |

---

## 二、实用组合

### 单人表情链

```
^_^ → 😊 → blush → looking away    害羞中带开心的表情递进
T_T → 😢 → tears → crying          从忍泪到痛哭
O_O → 😱 → surprised → shock       从震惊到惊吓
-_- → 😑 → unimpressed → deadpan   无语冷漠延续
```

### 多人互动表情链（BREAK 结构）

```
角色A: 😏 → smirk → confident → teasing
BREAK
角色B: 😳 → blush → embarrassed → covering face
```

一方挑逗一方羞——emoticon 占位少，适合放在角色 block 开头快速定调。

---

## 三、模型兼容性

| 模型族 | ASCII 颜文字 | Unicode Emoji |
|--------|-------------|---------------|
| Stable Diffusion 1.x | ✅ 部分支持（Danbooru 标签） | ✅ 支持 |
| NovelAI | ✅ Danbooru 标签级别 | ⚠️ 视版本 |
| Anima3 | ✅ 所有 ASCII 标签 | ✅ 建议搭配文本标签使用 |
| SDXL | ✅ 支持 | ✅ 支持 |
| Pony/SD 衍生 | ✅ 部分支持 | ✅ 支持 |

> 经验法则：Unicode Emoji 在模型中的语义强度较高且单一，适合"定调"。ASCII 颜文字属于标签体系，权重受位置和上下文影响，适合精确控制。

---

## 四、标签库对照

`tag-library/tags_sfw.yaml` 中 `expression > 表情维度 > 表情符号` 分类已收录以上全部标签。使用:

```bash
uv run scripts/manage_tags.py overview --slot expression
# 或
uv run scripts/query_tags.py search "^_^"   # 搜索指定表情
```

> 标签库中仅收录了经验证在 Anima3 模型中有效且语义明确的标签。此参考文献可作选词备案，未入库的表情仍需自行测试效果。
