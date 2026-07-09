# 风格优化指南

AI 填充标签时，本章补充常规槽位清单之外的"密度升维"技巧：如何让服装描写更有质感、表情神态更传神。

---

## 1. 人物描述自上而下律

描述人物最稳的顺序是按照重力的"自顶向下"。用于 `appearance` 和 `clothing/state` 槽位内部的标签排序：

1. 角色名、出处 IP（填充到 count/gender 或 character/series）
2. 种族挂件（角、halo、羽翼）— appearance
3. 发色、发长、发型细节 — appearance
4. 眼睛（虹膜、异色眼、瞳孔细节、眼睫毛）— appearance
5. 当前脸部表情 — expression
6. 上衣 → 下衣 → 丝袜/裤袜 → 皮鞋/靴子 — clothing/state
7. 配饰挂件（领带、颈环、尾巴、腰间道具）— clothing/state

> ⚡ **与槽位系统的关系**：自上而下律是对单个槽位内部标签粒度的补充指导，不改变 `slot-order.md` 的跨槽位顺序。"种族挂件"仍属于 appearance，"配饰"仍属于 clothing/state。

---

## 2. 服装细节升维公式

别只写单薄的名词服装标签。用"品类 + 剪裁 + 材质 + 装饰细节"四层公式增加画面密度：

### 通用范例

| 层级 | ❌ 单薄 | ✅ 升维 |
|------|---------|---------|
| 连衣裙 | `white dress` | `white flowy maxi dress with layered chiffon skirt, delicate lace trim, softly gathered bust, embroidered hemline, light fabric folds` |
| 外套 | `jacket` | `dark blue open jacket with a cropped streetwear silhouette, glossy technical fabric, oversized lapels, zip details, seam panels, cuff accents` |
| 上衣 | `sweater` | `cream cable-knit sweater with ribbed cuffs, relaxed fit, soft wool texture, slightly oversized` |
| 裙装 | `skirt` | `black pleated miniskirt with a high waist, sharp knife pleats, smooth fabric, slight flare at hem` |

### NSFW 专项范例

半脱/湿透/撕裂等状态需要同时给出"服装"和"穿着状态"两个维度：

| 状态 | 标签写法（服装 + 状态） |
|------|------------------------|
| 半脱 | `white button-up shirt, unbuttoned, open front, pulled off one shoulder, loose hanging, exposing bra` |
| 湿透 | `sheer white blouse, wet, clinging to skin, translucent fabric, water-soaked, visible bra underneath` |
| 撕裂 | `black fishnet stockings, torn, ripped holes, laddered, exposing bare skin underneath` |
| 半穿半脱 | `school uniform, unzipped skirt, sliding down hips, bunched at waist, inner thigh visible` |
| 绳索/捆绑 | `rope harness, wrapped around torso, crossed between breasts, tied behind back, taut lines pressing into skin` |
| 液体沾染 | `white dress, wet stains, translucent at chest, fabric clinging, darkened soaked patches, dripping hem` |

> **组合原则**：一件服装最多叠加 2 种状态（如 `wet, clinging`），不要超过 3 层，否则标签过长且模型容易困惑。

---

## 3. 表情五维拆解法

不要只写一个维度词（如 `sad`）。把表情拆解为 **眼睛·眉毛·嘴巴·脸红·汗泪** 五个独立维度组合：

### 五维对照表

| 维度 | 关键词示例 |
|------|-----------|
| 眼睛 | `wide-eyed, half-closed eyes, narrowed eyes, looking away, averted gaze, teary eyes, blank eyes` |
| 眉毛 | `raised eyebrows, knitted brows, furrowed brow, downturned eyebrows` |
| 嘴巴 | `open mouth, parted lips, bit lip, wavy mouth, pout, slight smile, tongue out, drooling` |
| 脸红 | `blush, full-face blush, red cheeks, flushed chest` |
| 汗泪 | `sweatdrop, sweat on face, tears, streaming tears, tear tracks, wet eyelashes` |

### 经典表情组合

| 表情 | 五维组合 |
|------|---------|
| 惊讶骇然 | `wide-eyed, raised inner eyebrows, open mouth, startled expression, sweatdrop` |
| 娇羞不知所措 | `averting eyes, embarrassed, full-face blush, wavy mouth, sweatdrop` |
| 楚楚可怜抬眸 | `head lowered, face angled downward, chin tucked, looking up at viewer from under her brows, upgaze` |
| 意乱情迷 | `half-closed eyes, heavy-lidded, flushed cheeks, parted lips, bit lip, dazed expression` |
| 屈辱强忍 | `furrowed brows, clenched jaw, tears welling, tight-lipped, trembling lip, suppressed sob` |
| 愉悦陶醉 | `upturned eyes, glazed pupils, slack jaw, tongue slightly out, deep flush, sweat on face` |

> ⚡ **与 expression.yaml 的关系**：本章提供了完整的"从零构造"方法。如果 expression.yaml 已有预设组合标签，优先使用脚本查询到的标签；需要进行微调或找不到合适组合时，用本章五维法手动构造。

---

## 5. 手臂分工原则

多手多脚畸形通常源于没有给双手分派明确职责。描写的核心原则：**明确双臂分工，互不重叠。**

### 通用写法

```
left hand holding a plate with cake, right hand making a v sign beside her face, both arms clearly visible
```

### NSFW 专项范例

| 场景 | 标签写法 |
|------|---------|
| 触手/凌辱 | `left hand gripping sheets tightly, right hand pinned against the wall, arms spread apart, restrained, struggling slightly` |
| 调整衣物 | `left hand unbuttoning her shirt slowly, right hand pulling down her bra strap, both arms reaching back, clothing adjustment` |
| 挑逗/自慰 | `left hand pressed against her own chest, fingers splayed, right hand sliding down her stomach, fingertips disappearing beneath waistband` |
| 强制 POV | `left hand gripping her own thigh, fingers digging into flesh, right hand making a v sign near her mouth, tongue out, deliberate pose` |

> **原则**：不要出现对称动作写两遍——`left hand doing X, right hand doing X` 是浪费标签容量。双手永远做不同的事，且尽量形成空间上的对角线（一高一低、一前一后）。

---

## 6. 动态构图方法论

拒绝呆板的正脸大头照。将相机视距、角度、焦段和构图结构化输入，画面张力立刻提升。

### 狂野对角线与俯冲透视

适用于需要动态感、速度感和空间交错的画面：

```
upper body portrait, from below, extreme dutch angle, face focus, dynamic diagonal composition, dramatic perspective, strong foreshortening, aggressive perspective, foreground blur
```

### 俯视/上帝视角

使用俯视角时模型容易把人物画得头下脚上。必须锚定重力方向：

```
pov directly from above, directly overhead view, bird's-eye view, head near the top of the frame, feet toward the bottom of the frame, torso vertical in frame, not upside down
```

### NSFW 视角专项

| 场景 | 推荐镜头组合 |
|------|-------------|
| 口交正戏（蹲踞位） | `from above, pov directly from above, looking down at partner, extreme dutch angle, face focus, dynamic composition` |
| 背后位/后入 | `from behind, over-the-shoulder, waist-level view, POV, thrust dynamics, body focus, sweat on back` |
| 压床正面 | `bird's-eye view, directly overhead, head near top of frame, face flushed, body sprawled, arms pinned` |
| 制服/调教站立 | `cowboy shot, from slightly below, subject looking down at viewer, power imbalance contrast, slight fisheye distortion` |

> ⚡ **与 camera/shot 槽位的关系**：本章补充的是现有 `camera-shot.yaml` 中未覆盖的"动态构图组合"与"视角特殊锚定词"。优先从脚本查询到的标签开始选，需要更激进的构图时用本章词包补位。

---

## 7. 背景空间升维公式

优秀的背景绝非一个单调的名词（如 `beach`）。按"**地点 + 时间/天气 + 前景动效 + 空间进深**"四层公式构建，场景才够立体。

### 通用场景范例

| 场景 | 标签组合 |
|------|---------|
| 耀眼落日沙滩 | `beach, beach waves, orange sky, clouds, sparkling sea surface, wet sand, foreground water sparkle, palm trees, sunset haze` |
| 神圣溪谷森林 | `sacred forest, waterfall, moss-covered rocks, reflective lake surface, floating leaves, mist, sunlight filtering through dense trees` |
| 炎夏晴空烈日公园 | `summer park, scorching hot sunlight, heat haze, dry grass, trees, bench, paved path, harsh midday light` |
| 超新星爆缩深空 | `supernova-like sky, expanding ring of light, solar flare streaks, glowing orange clouds, ember particles, luminous horizon` |

### NSFW 场景专项

| 场景 | 标签组合 |
|------|---------|
| 情人旅馆镜前 | `love hotel, large wall mirror reflecting bed, dim warm lighting, rumpled sheets, champagne glass on nightstand, soft focus, atmospheric haze` |
| 深夜空教室 | `classroom at night, moonlight through window, desks pushed together, scattered papers, dim fluorescent hum, dust particles in air, silent atmosphere` |
| 天台黄昏 | `school rooftop, sunset sky, orange glow, chain-link fence, water tank silhouette, wind-blown hair, city skyline, golden hour, elongated shadows` |
| 废弃公厕 | `public restroom, dirty tiles, flickering fluorescent light, graffiti on walls, wet floor reflections, cramped stall, cramped space, seedy atmosphere` |

> **公式用法**：选定核心地点 → 加上 1 个时间/天气锚点 → 加上 2-3 个周围物件 → 加上 1 个气氛收尾词。不要堆超过 7 个场景词，超出后模型注意力分散。

> ⚡ **与 scene 槽位的关系**：本章提供完整的"自组场景词包"。优先从 `scene-environment.yaml` 查询现有标签，需要自定义新场景或高级氛围描述时参考本章的四层公式。

---

## 8. 光影标签使用指南

光影标签现已允许使用。应按结构化方式放置：推荐置于 prompt 末尾倒数第二段（`scene` 之后、`natural language` 之前），与 `detail/mood` 槽位配合。

### 经典光影大礼包

适用于大多数场景的通用光影组合，涵盖了轮廓光、透射、景深和大气效果：

```
backlighting, rim light, subsurface scattering, lens flare, depth of field, bokeh, volumetric lighting
```

### 场景专项光影

| 场景类型 | 推荐光影组合 |
|---------|-------------|
| 魔法/异能变身 | `glowing particles, swirling light rings, sparkling dust, transformation magic effect, afterimage silhouette, burst of light` |
| 水边/水下 | `caustics, refraction, reflective liquid, water splashes, suspended droplets` |
| 赛博/都市夜 | `neon haze, chromatic aberration, glowing outlines, holographic particles, reflective wet ground` |
| 奇幻/星空 | `star trails, aurora, dispersion (optics), prism, colorful light particles` |

### 光影使用原则

- **不超过 1 组**：选用一个方向（经典 / 魔法 / 水波 / 赛博）的一组组合，不要混合多组（如 `backlighting` + `neon haze` 语义冲突）
- **不超过 5 个标签**：光影组内标签数控制在 3-5 个，超出后模型注意力分散
- **不叠加重力词**：`backlighting` 和 `rim light` 是二选一的关系，同时出现会让模型混乱
- **与场景一致**：`caustics, refraction` 配水边/水下场景；`neon haze` 配赛博都市夜

> ⚡ **与 detail/mood 槽位的关系**：`tag-library/detail-mood.yaml` 的 `光影标签清单` 节提供完整的单标签库，本章提供的是经过验证的组合推荐。优先从 YAML 单标签中选，直接组装时参考本章组合。

---

## 9. 与现有槽位系统的对应

| NovaAnima 概念 | 对应 SKILL.md 槽位 | 说明 |
|---------------|-------------------|------|
| 自上而下律 | appearance → clothing/state | 槽位内部标签排序指导 |
| 服装升维公式 | clothing/state | 常规服装用"品类+剪裁+材质+装饰"，NSFW 加"状态"维度 |
| 表情五维拆解 | expression | 当脚本预设组合不够用时，手动五维构造 |
| 手臂分工原则 | pose/action | 双臂各司其职，避免对称重复 |
| 动态构图方法论 | camera/shot | 补充脚本未覆盖的动态构图组合与视角锚定词 |
| 背景空间升维公式 | scene/environment | 四层公式自定义新场景，脚本覆盖不到时使用 |
