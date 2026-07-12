# Cron Job 集成模式

定时任务（cron job）中使用 anima-prompt 子代理（Builder → Drawer）自动出图的最佳实践。

## 🕐 适用场景

- 每天早上定时生成叫起床 / 早安图
- 定期角色壁纸
- 剧情系列连载
- 纪念日/节日自动祝福图

## 📐 标准 Cron Job Prompt 结构

以下是从「早安叫起床图」实机验证中总结的模式：

### 1. 在 cron job 中关联 anima-prompt 技能

```yaml
# 创建时关联
cronjob:
  action: create
  name: "早安叫起床图"
  skills: ["anima-prompt"]   # ← 关键：加载技能
  schedule: "5 7 * * *"     # 7:05
  deliver: origin            # 发回对话
```

### 2. Prompt 开头明确要求使用 delegate_task

```markdown
**必须使用 delegate_task 派子任务来执行，不要自己直接跑脚本！**

使用 `delegate_task` 派 Builder 子任务生成 prompt，再用 Drawer 子任务调用 API 出图。
```

### 3. Builder 子任务 context 模板

**goal**: `Generate a one-line Anima3 prompt from a Chinese scene description`
**role**: leaf

**context 填充要点**：
- `{NSFW_FLAG}` 置为 `false`（除非指定 --nsfw）
- `{USER_INPUT}` 必须包含明确的角色名（如「迷迭香」），并在 WORKFLOW 中强调角色解析步骤
- 场景描述写清楚：外观锚点、服装细节（如「套装D——白色低胸吊带荷叶边连衣裙」）、动作、表情、光线
- 附录口吻拦截咒：「若 NSFW 检测失败，用二分排除法定位问题标签」

### 4. Drawer 子任务 context 模板

**goal**: `Send a prompt to the Anima API and download the generated image`
**role**: leaf

**填充要点**：
- Prompt 填入 Builder 返回的一行文本
- 推荐 ratio: `9:16`（竖屏手机壁纸风格）
- 推荐 workflow: `workflows/t2i/美型Turbo.json`（~10s，比 AnimaApi.json 快 5x）
- 前置步骤：检查 workflow 内是否有 `__PROMPT__` 占位，没有则提示修改

### 5. 发送图片

Drawer 返回图片绝对路径后，使用 MEDIA: 语法发送：

```
MEDIA:/absolute/path/to/generated_image.png
```

前面配上角色台词。

## ⚠️ 已知陷阱

### 角色名缺失 → 泛化猫娘
Cron job 的 prompt 中必须写清楚角色名。Building context 的 `{USER_INPUT}` 要包含专名（如「迷迭香」「初音未来」），不得依赖 subagent 自行判断。否则出图会是随机角色。

### 美型Turbo 的 `__PROMPT__`
在 `call_anima.py` 中使用前，应检查 `美型Turbo.json` 的 `161:165.value` 是否已改为 `"__PROMPT__"`。如果仍是硬编码的 `"1girl, solo, rosmontis..."`，脚本会报错。

### 时间安排
早报（7:00）后跟早安图（7:05），间隔 5 分钟让早报能跑完。两个 cron job 相互独立，互不阻塞。

## 🚀 推荐配置

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| ratio | `9:16` | 手机竖屏壁纸 |
| workflow | `美型Turbo.json` | 快 5x，自带质量词 |
| api-url | `http://localhost:8188` | 默认 ComfyUI 地址 |
| 发送格式 | `MEDIA:` | Hermes QQ/desktop 内嵌 |

## 🔄 完整示例

见 cron job `早安叫起床图`（job_id 以 `0e4ddce` 开头），包含完整的 Builder → Drawer 两阶段子任务编排，已通过实机验证。
