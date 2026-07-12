# 详细参考（跨模式）

本文件含槽位顺序、冲突表、风格优化的详细规则。SKILL.md 内联了核心规则，本文件是深度补充。
Agent 在常规场景无需读取本文件，遇到复杂情况时可查阅。

---

## 槽位详细规则

### 风格一致性强调

跨槽位风格一致性铁律：clothing、scene、detail/mood 不能出现逻辑矛盾。基本原则——古风配古风（如 `hanfu` + `ancient shrine` + 水墨空灵），赛博配赛博（如 `latex bodysuit` + `cyberpunk city` + 数字故障），日常配日常（如 `school uniform` + `classroom` + 自然质感）。
不要出现 `hanfu` 站在 `cyberpunk city` 里这类跨世界观的矛盾组合。同一世界观内不同场景的混搭（如 `kimono` + `love hotel`）属于合理。

### 自然语言使用场景及具体写法

**核心原则**：tag 为主，自然语言仅在 tag 无法准确表达时使用。自然语言短句统一放在 prompt 末尾，所有 tag 之后。

**必须使用自然语言的场景**：

| 场景 | 原因 | 示例（放在末尾） |
|------|------|-----------------|
| 角色间动作关系 | 标签无法描述"谁对谁做什么" | `one reaches toward the viewer while the other watches in silence` |
| 复杂构图/空间关系 | 标签无法描述"谁在哪、面向谁" | `girl sitting on boy's lap facing him` |
| 特殊姿势组合 | 多个动作标签堆叠时主次不清 | `girl pinning wolf boy down while riding him` |
| 分镜/对比关系 | 标签无法表达时间或状态对比 | `left panel: dressed, right panel: nude` |

**格式规则**：自然语言短句统一放在 prompt 末尾（所有 tag 之后），与 tag 用逗号分隔。保持简洁，一个短句解决一个歧义。

### 观众关系（叙事性互动）

当场景具有剧情性时，除了视线方向，**必须**用自然语言（放末尾）描述角色与观众的叙事关系：

| 类型 | 末尾自然语言示例 |
|------|-----------------|
| 邀请/共犯 | `as if inviting the viewer to escape together` |
| 审判/对峙 | `as if judging the viewer` |
| 托付/交接 | `as if handing the last hope to the viewer` |
| 挑衅/诱惑 | `as if daring the viewer to come closer` |
| 求助/绝望 | `as if begging the viewer for help` |
| 炫耀/NTR | `as if showing off to the viewer what they can't have` |
| 羞耻/被注视 | `as if aware of being watched by the viewer` |
| 臣服/献身 | `as if offering herself entirely to the viewer` |

### 多人场景角色规则

**极重要**：多人场景中，只写角色名而不补外观会导致模型混淆，**必须为每个角色补充完整的外观和动作描述**。推荐用 `BREAK` 物理分隔角色 block，避免属性跨角色串味。

**结构**：
```
人数 → 共享互动词（体位/对望/拥抱等涉及两人的标签）→
角色 A（appearance → clothing → solo-action → expression）BREAK
角色 B（appearance → clothing → solo-action → expression）→
共享标签（camera → scene → detail/mood）→
自然语言（放末尾）
```

- **共享互动词**：描述两人关系的标签，如 `yuri, holding hands, missionary, fellatio`。紧跟在人数标签之后。
- **角色 block**：每个角色包含完整的外观、服装、独有动作和表情。block 内保持子槽位顺序一致。
- **BREAK**：作为逗号分隔序列中的一个分隔元素，物理隔断前后角色 block。
- **独有动作**：不涉及另一角色的自身动作（如 `one hand making a v sign`），放入对应角色 block。
- **自然语言**：关系/剧情等 tag 无法表达的内容，统一放在 prompt 末尾。

**示例**：
- 错误：`raiden shogun, long purple hair, playful, yae miko, pink hair, embarrassed, skirt lift`（模型无法判断属性归属）
- 正确：`2girls, skirt lift, raiden shogun with long purple hair and purple eyes, naval outfit, smiling mischievously, BREAK, yae miko with long pink hair and fox ears, shrine maiden outfit, blushing, looking away, from above, full body, shrine, one playfully lifting the other's skirt with a mischievous smirk while the other looks shy and embarrassed`

---

## 冲突详细规则

### 服装互斥

| 标签A | 标签B | 原因 |
|-------|-------|------|
| `completely nude` | 任何具体服装标签 | 全裸不穿衣 |
| `pantyhose` | `barefoot` | 穿了丝袜不可能光脚（除非 `torn pantyhose`） |
| `blindfold` | `glasses` | 物理冲突 |
| 内衣套装（`cat lingerie`, `lace lingerie`, `babydoll` 等） | `no panties` / `bottomless` | 内衣套装隐含包含内裤，模型优先解析套装忽略暴露标签；需暴露时拆为单件（`cat bra` + `no panties`） |

> **不互斥**：外衣/制服（`maid outfit`、`school uniform`、`bunny suit`、`sailor uniform` 等）与 `no panties` / `bottomless` 完全兼容——穿制服不穿内裤合理。

### 细节标签过度

同一身体部位同时堆叠多个细节标签会导致模型过度渲染，产生畸形。**每部位细节标签 ≤2 个，且不能互斥。**

| 部位 | 矛盾组合 | 原因 |
|------|---------|------|
| 脚趾 | `spread toes` + `toe scrunch` / `toes curling` | 舒展 vs 蜷缩 |
| 脚趾 | `spread toes` + `feet together` | 分趾 vs 合拢 |
| 手指 | `spread fingers` + `clenched fist` / `gripping` | 张开 vs 握拳 |
| 胸部 | `bouncing breasts` + `breasts squeeze together` | 弹跳 vs 挤压 |
| 嘴巴 | `open mouth` + `clenched teeth` / `closed mouth` | 张嘴 vs 闭嘴 |
| 眼睛 | `rolling eyes` + `looking at viewer` | 翻白眼 vs 直视 |
| 腿部 | `spread legs` + `legs together` | 分开 vs 并拢 |
| 足部整体 | 3 个以上足部标签 （如 `foot focus` + `footjob` + `toe scrunch` + `spread toes`） | 过度细化导致畸形 |

**原则**：同一部位的状态标签可以多个，但不能互斥。`barefoot` + `feet focus` + `soles` + `toe scrunch` 四个兼容标签没问题；`spread toes` + `toe scrunch` 两个就矛盾。关键在于**状态一致性**而非数量。

**例外**：`torn pantyhose` + `barefoot`（脚部撕开）、`partially undressed` + 具体服装（半脱状态）属于合理组合。

---

## 风格优化通用部分

### 1. 人物描述自上而下律

描述人物最稳的顺序是按照重力的"自顶向下"。用于 `appearance` 和 `clothing/state` 槽位内部的标签排序：

1. 角色名、出处 IP（填充到 count/gender 或 character/series）
2. 种族挂件（角、halo、羽翼）— appearance
3. 发色、发长、发型细节 — appearance
4. 眼睛（虹膜、异色眼、瞳孔细节、眼睫毛）— appearance
5. 当前脸部表情 — expression
6. 上衣 → 下衣 → 丝袜/裤袜 → 皮鞋/靴子 — clothing/state
7. 配饰挂件（领带、颈环、尾巴、腰间道具）— clothing/state

> 自上而下律是对单个槽位内部标签粒度的补充指导，不改变跨槽位顺序。

### 2. 服装细节升维公式（通用）

用"品类 + 剪裁 + 材质 + 装饰细节"四层公式增加画面密度：

| 层级 | 单薄 | 升维 |
|------|------|------|
| 连衣裙 | `white dress` | `white flowy maxi dress with layered chiffon skirt, delicate lace trim, softly gathered bust, embroidered hemline, light fabric folds` |
| 外套 | `jacket` | `dark blue open jacket with a cropped streetwear silhouette, glossy technical fabric, oversized lapels, zip details, seam panels, cuff accents` |
| 上衣 | `sweater` | `cream cable-knit sweater with ribbed cuffs, relaxed fit, soft wool texture, slightly oversized` |
| 裙装 | `skirt` | `black pleated miniskirt with a high waist, sharp knife pleats, smooth fabric, slight flare at hem` |

### 3. 表情五维拆解法

把表情拆解为 **眼睛·眉毛·嘴巴·脸红·汗泪** 五个独立维度组合：

| 维度 | 关键词示例 |
|------|-----------|
| 眼睛 | `wide-eyed, half-closed eyes, narrowed eyes, looking away, averted gaze, teary eyes, blank eyes` |
| 眉毛 | `raised eyebrows, knitted brows, furrowed brow, downturned eyebrows` |
| 嘴巴 | `open mouth, parted lips, bit lip, wavy mouth, pout, slight smile, tongue out, drooling` |
| 脸红 | `blush, full-face blush, red cheeks, flushed chest` |
| 汗泪 | `sweatdrop, sweat on face, tears, streaming tears, tear tracks, wet eyelashes` |

**经典组合**：惊讶骇然 `wide-eyed, raised inner eyebrows, open mouth, startled expression, sweatdrop`；娇羞不知所措 `averting eyes, embarrassed, full-face blush, wavy mouth, sweatdrop`；意乱情迷 `half-closed eyes, heavy-lidded, flushed cheeks, parted lips, bit lip, dazed expression`；愉悦陶醉 `upturned eyes, glazed pupils, slack jaw, tongue slightly out, deep flush, sweat on face`。

> 优先使用脚本查到的 expression.yaml 标签；需微调或找不到合适组合时，用本五维法手动构造。

### 5. 手臂分工原则（通用）

多手多脚畸形源于没有给双手分派明确职责。**明确双臂分工，互不重叠。**

**通用写法**：`left hand holding a plate with cake, right hand making a v sign beside her face, both arms clearly visible`

**原则**：不要出现对称动作写两遍。双手永远做不同的事，且尽量形成空间上的对角线（一高一低、一前一后）。

### 6. 动态构图方法论（通用）

**狂野对角线与俯冲透视**（适用于需要动态感的画面）：
```
upper body portrait, from below, extreme dutch angle, face focus, dynamic diagonal composition, dramatic perspective, strong foreshortening
```

**俯视/上帝视角**（需锚定重力方向）：
```
pov directly from above, directly overhead view, bird's-eye view, head near the top of the frame, feet toward the bottom of the frame, torso vertical in frame
```

### 7. 背景空间升维公式（通用）

按"**地点 + 时间/天气 + 前景动效 + 空间进深**"四层公式构建：

| 场景 | 标签组合 |
|------|---------|
| 耀眼落日沙滩 | `beach, beach waves, orange sky, clouds, sparkling sea surface, wet sand, foreground water sparkle, palm trees, sunset haze` |
| 神圣溪谷森林 | `sacred forest, waterfall, moss-covered rocks, reflective lake surface, floating leaves, mist, sunlight filtering through dense trees` |
| 炎夏晴空烈日公园 | `summer park, scorching hot sunlight, heat haze, dry grass, trees, bench, paved path, harsh midday light` |
| 超新星爆缩深空 | `supernova-like sky, expanding ring of light, solar flare streaks, glowing orange clouds, ember particles, luminous horizon` |

> 选定核心地点 → 加 1 个时间/天气锚点 → 加 2-3 个周围物件 → 加 1 个气氛收尾词。不要堆超过 7 个场景词。

### 8. 光影标签使用指南

光影标签现已允许使用。推荐置于 prompt 末尾倒数第二段（`scene` 之后、`natural language` 之前），与 `detail/mood` 槽位配合。

**经典光影大礼包**（适用于大多数场景）：
```
backlighting, rim light, subsurface scattering, lens flare, depth of field, bokeh, volumetric lighting
```

**场景专项光影**：

| 场景类型 | 推荐光影组合 |
|---------|-------------|
| 魔法/异能变身 | `glowing particles, swirling light rings, sparkling dust, transformation magic effect, afterimage silhouette, burst of light` |
| 水边/水下 | `caustics, refraction, reflective liquid, water splashes, suspended droplets` |
| 赛博/都市夜 | `neon haze, chromatic aberration, glowing outlines, holographic particles, reflective wet ground` |
| 奇幻/星空 | `star trails, aurora, dispersion (optics), prism, colorful light particles` |

**使用原则**：选用一个方向的一组组合（不超过 5 个标签），不混合多组；`backlighting` 和 `rim light` 二选一；光影与场景一致。

### 9. 与现有槽位系统的对应

| 概念 | 对应槽位 | 说明 |
|------|---------|------|
| 自上而下律 | appearance → clothing/state | 槽位内部标签排序指导 |
| 服装升维公式 | clothing/state | 常规服装用"品类+剪裁+材质+装饰" |
| 表情五维拆解 | expression | 脚本预设组合不够时手动构造 |
| 手臂分工原则 | pose/action | 双臂各司其职，避免对称重复 |
| 动态构图方法论 | camera/shot | 补充脚本未覆盖的动态构图组合 |
| 背景空间升维公式 | scene/environment | 四层公式自定义新场景 |
