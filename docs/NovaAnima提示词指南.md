# Anima & Nova Anima 提示词黄金手册

通读 Nova Anima 作者 Crody 的核心设计思路，提炼 100% 还原的图像生成保姆级秘籍。

- 原作者: Crody (Team-C)
- 整理人: 家里花花
- 适配版本: Nova Anima 全系列
- 更新时间: 2026-06-03

## 0. 生图软件环境与利弊

由于 Anima 模型使用了特殊的 Qwen 文本编码器与特殊的 Qwen Image VAE 架构，不同软件表现各异：

### ComfyUI — 最强基准

- 优势：官方基准环境，复现率 100%；分段管理 Qwen 文本编码与 VAE；工作流分享与对比极度方便
- 劣势：节点式界面门槛高，日常生图繁杂

### ForgeNeo — 日常生图

- 优势：经典 WebUI 界面，上手极其丝滑；历史记录、参数直达极其便利；极低的学习与习惯迁移成本
- 劣势：出图效果与官方 Comfy 相比略微有偏；文本与 VAE 管道实现细节可能有滞后

### Diffusers-Anima — 极客专享

- 优势：显存利用率（GPU Usage）全场最佳；用 Python 原生脚本控制，极其适合批渲染；能自由整合 sd_embed 进行加权提示词嵌入
- 劣势：无原生 GUI，需自行编写部署和出错处理

#### 极速部署 Diffusers-Anima Python 脚本

```python
# 1. 依赖安装
pip install torch diffusers git+https://github.com/Faildes/sd_embed_negpip.git git+https://github.com/Faildes/diffusers-anima@from_multiple_models git+https://github.com/huggingface/transformers@1e931b8fcafa19dc82b2a482898098e4d15aca81

# 2. 管道搭建与 RF Euler 调度器加载
from diffusers_anima import AnimaPipeline
pipe = AnimaPipeline.from_single_file("/path/to/anima.safetensors", variant="bf16")
pipe.scheduler.set_sampling_config(sampler="euler_a_rf", sigma_schedule="normal")
pipe.safety_checker = None
pipe.to("cuda")
```

## 1. Nova Anima 生成参数基准

适用于 Nova Anima 2.0 及其后续所有系列的"甜点参数配方"：

| 参数 | 推荐值 |
|------|--------|
| 采样器 (Sampler) | Euler A RF（极力推荐） |
| CFG 比例 (CFG Scale) | 4.0–6.0（实测推荐 5.0） |
| 生成步数 (Steps) | 30（特殊 lighting LoRA 时按 LoRA 规定） |
| 标准画质基准像素 | 1280 x 1280（约 1.6M 总像素，单边像素必为 16 倍数） |

### 黄金像素比例换算（163.8 万总像素）

| 比例 | 尺寸 | 用途 |
|------|------|------|
| 9:16 | 960 x 1680 | 正人脸/社交短视频 |
| 3:4 | 1104 x 1472 | 标准人像 |
| 1:1 | 1280 x 1280 | 完美正方形 |
| 16:9 | 1696 x 960 | 标准宽屏风景 |
| 2.35:1 | 1952 x 832 | 电影宽荧幕 |

## 2. 结构化公式：定义"画什么"与"怎么画"

九段式卡槽结构：

| 卡槽 | 内容 |
|------|------|
| [1] | 画质分级与基础年代 (Quality / Meta / Era / Rating) |
| [2] | 人物数量与初始行为互动 (Subject Count / Interaction) |
| [3] | 角色姓名、作品出处或原创人设 (Character Name / Series / IP) |
| [4] | 五官特征、发色发型、表情与服装配饰 (Body / Hair / Face / Outfit) |
| [5] | 画面核心姿势动作 (Pose / Action) |
| [6] | 相机镜头、视距与透视构图 (Camera / Lens / Composition) |
| [7] | 背景环境、时间天气与空间道具 (Background / Atmosphere / Scene) |
| [8] | 光影渲染、空气深度与粒子特效 (Lighting / Depth / Effects) |
| [9] | （可选）复杂场景补位用的"纯自然语言"描述 |

## 3. 书写语法铁律

### 纯空格替代下划线

传统下划线多来自 Danbooru，但 Anima 理解空格和日常口语词极其优秀。

- ❌ `looking_at_viewer, fake_rabbit_ears`
- ✅ `looking at viewer, fake rabbit ears`
- 例外：固有打分标签必须带下划线，如 `score_7`

### 无条件全小写

除特殊实体外，其余一律全小写。

- ❌ `Best Quality, Long Hair, White Dress`
- ✅ `best quality, long hair, white dress`

### 克制使用提示词权重

过度加权会导致文本编码崩溃。黄金区间：初始 `1.2`，上限 `1.4`。

- 推荐：`(red eyes:1.2)`, `(black sundress:1.2)`

### 拒绝换行、严格逗号分割

输入到生图软件时绝对不能带换行符，保持一整段连续长文字，纯半角英文逗号分割。

## 4. 画质、年代与分级前缀

### 标准 Anima 画质前缀

```
masterpiece, best quality, score_9, score_8, score_7, year 2025, newest, highres, absurdres, very aesthetic, scenery
```

### 年代感指示词

- `year 2025 year 2024 newest recent mid early / old`

### 分级标签

- `safe` — 常规、健康二次元插图
- `sensitive` — 微性感、轻微露肤
- `nsfw / explicit` — 成人插画、大尺度福利

## 5. 艺术家与画风召唤术

在艺术家名字前必须带上 `@` 符号：

```
1girl, solo, @artist name, long hair, blue eyes, white dress
```

> 不要一口气叠太多艺术家 @，推荐先只写一位，最多 2 个进行混合。

## 6. 人数定义与互动纠缠

### 互动词必须紧跟在人数后

- ❌ 分开写完两个人后在末尾才写互动（易崩坏）
- ✅ `2girls, duo, holding each other's hands,` 然后分开描述

### 角色描述完全物理隔离

```
天使姐姐 descriptions... BREAK 恶魔妹妹 descriptions...
```

利用 `BREAK` 实现物理隔断。

## 7. 身体、发型与精致服装结构

### 自上而下的起步律

1. 角色名、出处 IP
2. 种族挂件（角、halo、羽翼）
3. 发色、发长、发型细节
4. 眼睛（虹膜、异色眼、瞳孔细节、眼睫毛）
5. 当前脸部表情
6. 上衣 → 下衣 → 丝袜/裤袜 → 皮鞋/靴子
7. 配饰挂件（领带、颈环、尾巴、腰间道具）

### 衣服细节升维

- ❌ `white dress`
- ✅ `white flowy maxi dress with layered chiffon skirt, delicate lace trim, softly gathered bust, embroidered hemline, light fabric folds`
- ✅ `dark blue open jacket with a cropped streetwear silhouette, glossy technical fabric, oversized lapels, zip details, seam panels, cuff accents`

## 8. 极致眼神与表情微操

把表情拆解为五个部分：眼睛、眉毛、嘴巴、脸红、汗液/眼泪。

| 表情 | 关键词组合 |
|------|-----------|
| 惊讶骇然 | wide-eyed, raised inner eyebrows, open mouth, startled expression, sweatdrop |
| 娇羞不知所措 | averting eyes, embarrassed, full-face blush, wavy mouth, sweatdrop |
| 抬眸下视（楚楚可怜） | head lowered, face angled downward, chin tucked, looking up at viewer from under her brows, upgaze |
| 侧颜倾心 | three-quarter face, slightly side-angled view, camera positioned slightly to the side |

## 9. 肢体动作、手臂分工与手指控符

### 手臂各司其职

- ✅ `left hand holding a plate with cake, right hand making a v sign beside her face, both arms clearly visible`

### 非五指/卡通手指控制符

- 4 指：`exactly four fingers on each hand, four digits on each hand, thumb and three fingers, no fifth finger`
- 3 指：`exactly three fingers on each hand, three digits on each hand, thumb and two fingers, no fourth finger, no fifth finger`
- 负面：`five fingers, five digits, extra fingers, human hands, realistic human hands`

## 10. 镜头与对角线构图

### 狂野对角线与俯冲透视

```
upper body portrait, from below, extreme dutch angle, fisheye, face focus, dynamic diagonal composition, dramatic perspective, strong foreshortening, aggressive perspective, foreground blur
```

### 俯视/上帝视角

需强制重力锚定词防止颠倒：

```
pov directly from above, directly overhead view, bird's-eye view, head near the top of the frame, feet toward the bottom of the frame, torso vertical in frame, not upside down
```

## 11. 背景空间与氛围烘托

| 场景 | 关键词组合 |
|------|-----------|
| 耀眼落日沙滩 | beach, beach waves, orange sky, clouds, sparkling sea surface, wet sand, foreground water sparkle, palm trees, sunset haze |
| 神圣溪谷森林 | sacred forest, waterfall, moss-covered rocks, reflective lake surface, floating leaves, mist, sunlight filtering through dense trees |
| 炎夏晴空烈日公园 | summer park, scorching hot sunlight, heat haze, dry grass, trees, bench, paved path, harsh midday light |
| 超新星爆缩深空 | supernova-like sky, expanding ring of light, solar flare streaks, glowing orange clouds, ember particles, luminous horizon |

## 12. 光影、折射与空气特效

放在正向提示词最末尾。

### 经典光影大礼包

```
backlighting, rim light, subsurface scattering, lens flare, depth of field, bokeh, volumetric lighting
```

### 魔法异能变身

```
glowing particles, swirling light rings, sparkling dust, transformation magic effect, afterimage silhouette, burst of light
```

### 极致水波镜折射

```
caustics, refraction, reflective liquid, water splashes, suspended droplets
```

### 赛博霓虹积水

```
neon haze, chromatic aberration, glowing outlines, holographic particles, reflective wet ground
```

## 13. 自然语言补位法

在尾部加上 1~2 句英文自然语言描述。

### 单人动作自然语言

> "A blonde woman kneels in shallow beach water while her white dress flows with the waves. The camera looks down from a dramatic angle, with golden sunlight, sparkling water, and a soft summer atmosphere."

### 双人互动自然语言

> "The red angel girl and the blue demon girl float in the night sky, holding each other's hands. Their wings spread in opposite colors under a red-to-blue gradient moon."

## 14. 负面提示词包

```
worst quality, low quality, early, old, score_1, score_2, score_3, cartoon, graphic, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured, long body, bad anatomy, bad hands, missing fingers, extra fingers, extra digits, fewer digits, cropped, very displeasing, artist name, blurry, jpeg artifacts, lowres, censor
```

## 15. Illustrious → Anima 转换规则

1. **精简画质词**：`masterpiece, best quality, score_7, highres`
2. **更改分级词**：`general, questionable` → `safe, sensitive, nsfw, explicit`
3. **剔除下划线**：`looking_at_viewer` → `looking at viewer`
4. **艺术家 @ 绑定**：画师名前加 `@`
5. **补足尾部口语**：复杂互动在末尾加英文描述

## 终极正向提示词模板

```
[quality / meta / rating], [person count], [interaction], [character name, series], [@artist name], [skin / ears / horns / halo / wings], [hair color, length, style], [eye color, eye shape, pupils], [expression], [body features], [headwear / eyewear], [neckwear], [upper clothes], [lower clothes], [legwear], [shoes], [accessories / tail / wings], [pose], [hand position], [leg position], [action], [camera distance, angle, lens, focus, composition], [background, time, weather, scene objects], [lighting, depth, effects, after details]
```

## 实战案例

### 案例一：宇宙落星·粉发神冕美少女

**参数：** Nova Anime AM v2.0 beta | 960x1680 | 30步 | CFG 5.0 | Euler A | Seed 3282307999

```
masterpiece, best quality, score_9, score_8, score_7, year 2025, newest, highres, absurdres, very aesthetic, scenery, 1girl, solo, cute, pink hair, very long hair, choppy bangs, long sidelocks, flowing hair, nebulae cosmic purple eyes, white pupils, rimlit eyes, facing side, looking at viewer, downturned eyes, light smile, red annular solar eclipse halo, red choker, detailed purple blazer with a fitted tailored cut, structured shoulders, gold piping, decorative seams, flap pockets, subtle celestial embroidery, ornate cuffs, collared white shirt with crisp pleats and a clean front placket, big red neckerchief with layered folds and wind-swept fabric, glowing stars swirling, glowing star in her outstretched hand, fingers, dramatic head tilt, torso twist, from side, from below, upper body portrait, extreme dutch angle, dynamic diagonal composition, intense perspective, strong foreshortening, wind-blown hair, fluttering neckerchief, flying fabric, sweeping motion, face focus, sharp focus, vivid foreground light streaks, blurry foreground particles, layered depth, colorful, saturated, rim light, strong backlighting, subsurface scattering, (colorful light particles:1.3), glowing star trails, energy arcs, cosmic sky, aurora, chaotic night sky, fantasy background, dreamlike atmosphere, detailed background, bokeh, depth of field, volumetric lighting, dispersion (optics), prism
```

### 案例二：红翼天使与蓝翼恶魔双子同框

**参数：** Nova Anime AM v2.0 beta | 1136x1424 | 30步 | CFG 5.0 | Euler A | Seed 2383386786

```
masterpiece, best quality, score_9, score_8, score_7, year 2025, newest, highres, absurdres, very aesthetic, scenery, 2girls, duo, black angel with white hair and white devil with black hair, floating in midair, dynamic paired pose, black angel girl, red halo, long white hair, hair between eyes, floating hair, white eyelashes, red eyes, red angel wings, rough personality, fierce expression, confident smile, parted lips, looking at viewer, turning head, slightly aggressive body language, (black sundress:1.2) with a soft draped bodice, delicate gathered bust, subtle lace inset details, thin shoulder straps, flowing layered skirt, lightweight fabric, gently flared hem, elegant summer dress silhouette, white devil girl, big white horns, long black hair, floating hair, blue eyes, blue bat demon wings, blue demon tail, calm personality, quiet expression, gentle gaze, soft smile, looking at viewer, slightly timid body language, (white sundress:1.2) with a soft draped bodice, delicate gathered bust, subtle lace inset details, thin shoulder straps, flowing layered skirt, lightweight fabric, gently flared hem, elegant summer dress silhouette, their bodies facing each other, one arm reaching across to grasp each other's hand, the free arms trailing naturally, slight back arch, torso twist, legs floating softly, elegant mirrored composition, face focus, portrait, three-quarter view, close shot, extreme dutch angle, dynamic diagonal composition, dramatic floating pose, controlled foreshortening, red angel wings spread wide, blue demon wings spread wide, hair drifting in the air, shimmering red feathers swirling around them, (night, starry sky:1.2), red-to-blue gradient full moon, ominous yet dreamy atmosphere, dappled moonlight, subtle lens flare, soft rim light, backlighting, layered depth, bokeh, depth of field, volumetric lighting
```

### 案例三：单人倚树舒缓测试

```
masterpiece, best quality, score_7, safe, newest, highres, 1girl, solo, blonde hair, low side ponytail, blue eyes, white dress with lace-trimmed collar, puffy sleeves, shoulder cutout, looking at viewer, turning head, parted lips, leaning back against a tree, one hand extended toward the viewer, upper body portrait, medium shot, dutch angle, dynamic diagonal composition, forest, flowers, white butterfly, dappled sunlight, backlighting, lens flare, depth of field, volumetric lighting
```

## 生图起手确认卡

1. 画质前缀是否在最开头？（确保带有 `score_7` 或以上）
2. 是否加上分级前缀标签（如 `safe` 或 `nsfw`）？
3. 所有下划线是否换成了空格分割？（除 score 打分词）
4. 画师/艺术家名字前是否加了 `@`？
5. 如果是多个人，互动语句是否紧跟在人数标签后？
6. 是否给双手分派了明确的行为？
7. 如果场景特别庞大，正向词末尾是否补了一句英文自然口语段？
8. 负面输入框里的词是否配对无误？
