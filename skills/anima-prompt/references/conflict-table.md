## 3.1 CONFLICT TABLE

以下标签对**不可同时出现**，AI 必须在组装时检查冲突：

### 视角互斥

| 标签A | 标签B | 原因 |
|---|---|---|
| `from front` | `from behind` | 物理矛盾 |
| `from above` | `from below` | 物理矛盾 |
| `looking at viewer` | `facing away` | 视线矛盾 |
| `pov` | `full body` | POV 不可能看到自己全身 |
| `close-up` | `full body` | 景别矛盾 |

### 身份互斥

| 标签A | 标签B | 原因 |
|---|---|---|
| `solo` | `hetero` / `1boy` / `yuri` | 单人不存在互动 |
| `femdom` | `male-on-female rape` | 逻辑矛盾（主导方冲突） |
| `sleeping` / `unconscious` | `looking at viewer` | 无意识不可能直视 |
| `blindfold` | `heart-shaped pupils` / `rolling eyes` | 看不到眼睛 |

### 服装互斥

| 标签A | 标签B | 原因 |
|---|---|---|
| `completely nude` | 任何具体服装标签 | 全裸不穿衣 |
| `pantyhose` | `barefoot` | 穿了丝袜不可能光脚（除非 `torn pantyhose`） |
| `blindfold` | `glasses` | 物理冲突 |
| 内衣套装 (`cat lingerie`, `lace lingerie`, `babydoll`, `negligee`, `chemise` 等) | `no panties` / `bottomless` | 内衣套装隐含包含内裤，模型优先解析套装忽略暴露标签；需暴露时拆为单件（`cat bra` + `no panties`） |

> **不互斥**：外衣/制服（`maid outfit`、`school uniform`、`bunny suit`、`sailor uniform` 等）与 `no panties` / `bottomless` 完全兼容——穿制服不穿内裤 = 合理场景。

### 动作互斥

| 标签A | 标签B | 原因 |
|---|---|---|
| `standing sex` | `lying` / `on back` | 体位矛盾 |
| `missionary` | `doggystyle` | 不可能同时两个体位 |
| `cowgirl position` | `prone bone` | 体位矛盾 |
| `fellatio` | `cunnilingus`（同一人执行） | 嘴只有一张 |

### 细节标签过度

同一身体部位同时堆叠多个细节标签会导致模型过度渲染，产生畸形。**每部位细节标签 ≤2 个，且不能互斥。**

| 部位 | 矛盾组合 | 原因 |
|---|---|---|
| 脚趾 | `spread toes` + `toe scrunch` / `toes curling` | 舒展 vs 蜷缩，物理矛盾 |
| 脚趾 | `spread toes` + `feet together` | 分趾需要空间，合拢则压缩 |
| 手指 | `spread fingers` + `clenched fist` / `gripping` | 张开 vs 握拳 |
| 胸部 | `bouncing breasts` + `breasts squeeze together` | 弹跳 vs 挤压，动态矛盾 |
| 嘴巴 | `open mouth` + `clenched teeth` / `closed mouth` | 张嘴 vs 闭嘴 |
| 眼睛 | `rolling eyes` + `looking at viewer` | 翻白眼 vs 直视 |
| 腿部 | `spread legs` + `legs together` | 分开 vs 并拢 |
| 足部整体 | 3 个以上足部标签（如 `foot focus` + `footjob` + `toe scrunch` + `spread toes`） | 过度细化导致脚趾/脚掌畸形 |

**原则**：同一部位的状态标签可以多个，但不能互斥。`barefoot` + `feet focus` + `soles` + `toe scrunch` 四个兼容标签没问题；`spread toes` + `toe scrunch` 两个就矛盾。关键在于**状态一致性**而非数量。

**例外**：`torn pantyhose` + `barefoot`（脚部撕开）、`partially undressed` + 具体服装（半脱状态）属于合理组合。
