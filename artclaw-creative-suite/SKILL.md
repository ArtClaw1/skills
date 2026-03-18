---
name: artclaw-creative-suite
description: |
  ARTCLAW AI Creative Suite — 通过 REST API 调用 ARTCLAW 平台的 AI 内容创作能力。
  支持 AI 生图、生视频、PPT 生成、工作流执行、多模态分析、Prompt 优化等能力。
  所有生成类接口异步返回 job_id，需先获取 API Key 完成鉴权。
  触发关键词：生成图片、生成视频、AI绘画、文生图、文生视频、图生视频、营销图、轮播图、
  产品图、Logo、封面、工作流、视频分析、图片分析、ARTCLAW、ArtClaw。
compatibility:
  dependencies:
    - ARTCLAW REST API (http://43.156.26.92:8892/api/v1)
---

# ARTCLAW AI Creative Suite

ARTCLAW 是一站式 AI 内容创作平台，通过 REST API 对外提供图片生成、视频生成、多媒体分析、工作流编排等核心能力。

**API 基地址：** `http://43.156.26.92:8892/api/v1`

---

## 开场白（Skill 激活时默认展示）

当用户首次激活本 Skill 或对话开始时，**必须立即输出以下开场白**（不需要用户主动提问），让用户快速了解可用能力：

```
🎨 ARTCLAW AI Creative Suite 已就绪！

我是你的 AI 创意助手，已接入 ARTCLAW 全套内容创作能力。以下是我能为你做的事：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🖼️ AI 生图
  • 文生图 / 图生图 — 描述画面即可生成
  • 营销广告图 — 自动优化风格与构图
  • 产品套图 — 电商轮播图一键生成

🎬 AI 生视频
  • 文生视频 / 图生视频 — 让静态画面动起来

📊 AI PPT
  • 输入主题，自动生成多页演示幻灯片

🔍 多模态分析
  • 图片理解 — 看图说话，精准描述
  • 视频分析 — 自动解析视频内容
  • 剧本分析 — 短剧剧本深度拆解 + 互动节点
  • 人物小传 — 从故事文本提炼角色档案

⚡ 工作流
  • 一键执行预设流程（动画 / 微电影 / 漫画 / 电商详情页…）

✏️ Prompt 工具（免费，无需 API Key）
  • Logo 提示词 · 封面提示词 · 营销图提示词 · 轮播图提示词

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 快速开始：
  1. 直接告诉我你想生成什么，例如："帮我画一张赛博朋克风格的猫咪"
  2. 如果还没有 API Key，我会引导你免费获取
  3. 免费的 Prompt 工具可以直接使用，无需任何配置

有什么想创作的？告诉我吧 ✨
```

> **注意：** 开场白在以下场景触发：
> - 用户首次激活 Skill 时
> - 新对话开始且 Skill 已加载时
>
> 如果用户在首条消息中已明确提出具体任务（如"帮我生成一张图片"），则跳过开场白，直接执行任务。

---

## 第一步：获取 API Key

所有生成类接口需要 API Key 鉴权，通过 HTTP Header `X-API-KEY` 传递。

> **如果用户还没有 API Key，请引导他们完成以下步骤：**

1. 打开 ARTCLAW 官网设置页：**https://staging.artclaw.com/#/settings**
2. 在 **API Keys** 管理区域点击「创建」
3. 输入一个名称（如 `my-app`），确认后复制生成的 Key
4. Key 以 `vk_` 开头，**仅在创建时展示一次**，请妥善保存

> 获取 Key 后，在每次 HTTP 请求中通过 Header 传入：
> ```
> X-API-KEY: vk_your_key_here
> ```

可以调用验证接口确认 Key 有效：

```bash
curl -X POST http://43.156.26.92:8892/api/v1/auth/verify \
  -H "Content-Type: application/json" \
  -d '{"api_key": "vk_your_key_here"}'
```

返回：
```json
{"status": "valid", "uin": "user_id"}
```

---

## 能力总览

| 类别 | 接口 | 方法 | 说明 | 需要 Key |
|------|------|------|------|----------|
| **生图** | `/api/v1/generate/image` | POST | 文生图 / 图生图（支持参考图） | ✅ |
| **生图** | `/api/v1/generate/marketing-image` | POST | 营销广告图（自动增强提示词） | ✅ |
| **生图** | `/api/v1/generate/product-carousel` | POST | 产品套图（多图轮播，自动风格匹配） | ✅ |
| **生视频** | `/api/v1/generate/video` | POST | 文生视频 / 图生视频（I2V） | ✅ |
| **PPT** | `/api/v1/generate/ppt` | POST | AI PPT 幻灯片生成（多页图片） | ✅ |
| **分析** | `/api/v1/analyze/image` | POST | AI 图片理解与描述 | ✅ |
| **分析** | `/api/v1/analyze/video` | POST | AI 视频内容分析 | ✅ |
| **分析** | `/api/v1/analyze/script` | POST | 短剧剧本分析 + 互动节点设计 | ✅ |
| **分析** | `/api/v1/analyze/characters` | POST | 从故事文本生成人物小传 | ✅ |
| **工作流** | `/api/v1/workflows` | GET | 列出所有可用预设工作流 | ✅ |
| **工作流** | `/api/v1/workflows/{id}/run` | POST | 执行预设工作流 | ✅ |
| **任务管理** | `/api/v1/jobs/{job_id}` | GET | 查询任务状态和结果 | ✅ |
| **任务管理** | `/api/v1/jobs` | GET | 列出历史任务 | ✅ |
| **任务管理** | `/api/v1/jobs/{job_id}/cancel` | POST | 取消正在进行的任务 | ✅ |
| **账户** | `/api/v1/account/info` | GET | 查询账户余额与用量 | ✅ |
| **鉴权** | `/api/v1/auth/verify` | POST | 验证 API Key 有效性 | ❌ |
| **Prompt** | `/api/v1/prompts/logo` | POST | 生成 Logo 提示词（免费） | ❌ |
| **Prompt** | `/api/v1/prompts/cover` | POST | 生成封面图提示词（免费） | ❌ |
| **Prompt** | `/api/v1/prompts/marketing` | POST | 增强营销图提示词（免费） | ❌ |
| **Prompt** | `/api/v1/prompts/carousel` | POST | 生成轮播图提示词系列（免费） | ❌ |

---

## 鉴权方式

除 Prompt 工具（`/api/v1/prompts/*`）和 Key 验证（`/api/v1/auth/verify`）外，所有接口均需在 HTTP Header 中传入 API Key：

```
X-API-KEY: vk_your_key_here
```

未携带或无效 Key 将返回 `401 Unauthorized`。

---

## 频率限制

| 分类 | 路径 | 限制 |
|------|------|------|
| 生成类 | `/api/v1/generate/*`、`/api/v1/workflows/*`、`/api/v1/analyze/*` | 10 次/分钟 |
| 查询类 | `/api/v1/jobs/*`、`/api/v1/account/*` | 60 次/分钟 |
| 公开类 | `/api/v1/prompts/*` | 30 次/分钟 |

超限返回 `429 Too Many Requests`。

---

## 核心模式：异步生成

**所有生成类接口**（图片/视频/PPT/工作流）均为异步模式。调用后立即返回 `job_id`，需轮询状态直到完成。

### 标准流程

```
1. POST 生成接口 → 获得 job_id
2. 立即告知用户"已提交生成任务，等待完成"
3. 以一定间隔 GET /api/v1/jobs/{job_id} 检查状态。任务可能在队列中排队，不要因为 pending 持续很久就认为出错
4. 如果 pending 超过 2 分钟，安抚用户，告知生成可能需要一些时间，之后也要间隔安抚
5. 状态变为 "success" 后返回 result.url 给用户
```

### 任务状态说明

| status | 含义 |
|--------|------|
| `pending` | 排队等待中 |
| `running` | 生成中 |
| `success` | 已完成，`result` 字段包含结果 URL |
| `failed` | 失败，检查 `metadata.error_detail` |
| `canceled` | 已取消 |
| `expired` | 已过期（24小时） |

### 轮询间隔建议

| 任务类型 | 轮询间隔 | 超时上限 |
|----------|----------|----------|
| 图片 | 5s | 2min |
| 视频 | 10s | 5min |
| PPT | 10s | 10min |
| 工作流 | 15s | 30min |

### 回调通知（Webhook）

所有生成接口均支持 `callback_url` 参数。任务到达终态时，服务器会自动 POST 通知：

```json
{
  "event": "job.completed",
  "job_id": "job_xxxxxxxx",
  "type": "image_generation",
  "status": "success",
  "metadata": {},
  "result": { "url": "https://oss.artclaw.app/..." },
  "timestamp": "2026-03-18T10:01:05Z"
}
```

Header 中包含 `X-Vicoo-Signature`（HMAC-SHA256 签名）可用于校验请求真实性。失败会重试 3 次（间隔 10s/30s/60s）。

---

## 完整调用流程示例

### Bash（curl）

```bash
API_KEY="vk_your_key_here"
BASE="http://43.156.26.92:8892/api/v1"

# 1. 提交生成任务
gen_resp=$(curl -s -X POST "$BASE/generate/image" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"prompt": "赛博朋克城市夜景", "aspect_ratio": "16:9"}')
job_id=$(echo "$gen_resp" | jq -r '.job_id')

# 2. 轮询状态
while true; do
  sleep 5
  status_resp=$(curl -s "$BASE/jobs/$job_id" -H "X-API-KEY: $API_KEY")
  status=$(echo "$status_resp" | jq -r '.status')
  if [[ "$status" == "success" ]]; then
    url=$(echo "$status_resp" | jq -r '.result.url')
    echo "图片URL: $url"
    break
  elif [[ "$status" == "failed" ]]; then
    echo "失败: $(echo "$status_resp" | jq -r '.metadata.error_detail')"
    break
  fi
done
```

### Python

```python
import httpx, time

API_KEY = "vk_your_key_here"
BASE = "http://43.156.26.92:8892/api/v1"
HEADERS = {"Content-Type": "application/json", "X-API-KEY": API_KEY}

# 1. 提交生成任务
resp = httpx.post(f"{BASE}/generate/image", headers=HEADERS, json={
    "prompt": "赛博朋克城市夜景",
    "aspect_ratio": "16:9"
})
job_id = resp.json()["job_id"]

# 2. 轮询状态
while True:
    time.sleep(5)
    resp = httpx.get(f"{BASE}/jobs/{job_id}", headers=HEADERS)
    data = resp.json()
    if data["status"] == "success":
        print("图片URL:", data["result"]["url"])
        break
    elif data["status"] == "failed":
        print("失败:", data["metadata"].get("error_detail"))
        break
```

---

## REST API 详细参数

### POST `/api/v1/generate/image` — 文生图 / 图生图

根据文本描述生成图片，支持传入参考图（图生图模式）。

**请求体：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | **必填** | 图片描述文本 |
| `aspect_ratio` | string | `"16:9"` | 宽高比：`16:9` / `9:16` / `1:1` / `4:3` / `21:9` |
| `resolution` | string | `"1K"` | 分辨率：`1K` / `2K` / `4K` |
| `reference_urls` | list[string] | `[]` | 参考图 URL 列表（传入后进入图生图模式） |
| `model` | string | 默认模型 | 指定模型 ID（可选） |
| `callback_url` | string | `""` | 回调地址 |

**示例：**

```bash
curl -X POST http://43.156.26.92:8892/api/v1/generate/image \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: vk_xxx" \
  -d '{
    "prompt": "赛博朋克城市夜景，霓虹灯倒映在湿润的街道上",
    "aspect_ratio": "16:9"
  }'
```

**返回：**

```json
{
  "job_id": "job_xxxxxxxx",
  "type": "image_generation",
  "status": "pending",
  "created_at": "2026-03-18T10:00:00Z",
  "message": "Job submitted. Use get_job_status('job_xxxxxxxx') to check progress."
}
```

---

### POST `/api/v1/generate/video` — 文生视频 / 图生视频

根据文本描述生成视频；若传入参考图则进入图生视频（I2V）模式。

**请求体：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | **必填** | 视频描述 |
| `aspect_ratio` | string | `"16:9"` | `16:9` / `9:16` / `1:1` |
| `duration` | int | `5` | 时长（秒），范围 2-12 |
| `resolution` | string | `"1K"` | `480p` / `720p` / `1080p` / `1K` / `2K` |
| `reference_url` | string | `""` | 参考图 URL（传入后自动切换为图生视频模式） |
| `model` | string | 默认模型 | 指定模型 ID（可选） |
| `callback_url` | string | `""` | 回调地址 |

**示例（文生视频）：**

```bash
curl -X POST http://43.156.26.92:8892/api/v1/generate/video \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: vk_xxx" \
  -d '{"prompt": "海浪拍打白色沙滩，金色傍晚阳光", "duration": 5}'
```

**示例（图生视频）：**

```bash
curl -X POST http://43.156.26.92:8892/api/v1/generate/video \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: vk_xxx" \
  -d '{
    "prompt": "人物缓慢回头，夕阳余晖",
    "reference_url": "https://example.com/portrait.jpg"
  }'
```

---

### POST `/api/v1/generate/marketing-image` — 营销广告图

根据简单描述自动增强风格，生成专业的营销类广告图片。

**请求体：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | **必填** | 营销图描述（如"蓝牙耳机广告"） |
| `size` | string | `"1080x1920"` | 图片尺寸，格式 `宽x高`（像素） |
| `callback_url` | string | `""` | 回调地址 |

---

### POST `/api/v1/generate/product-carousel` — 产品套图

为产品生成多张风格统一的轮播图（封面 + 内容页 + 背页），适合电商、小红书等场景。

**请求体：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `product_type` | string | **必填** | `skincare` / `coffee` / `tech` |
| `theme` | string | **必填** | 产品主题描述，如"春季护肤新品" |
| `product_name` | string | `""` | 产品名称，如"水光精华" |
| `style` | string | `"warm_cozy"` | `warm_cozy` / `cyberpunk` / `minimalist` / `professional` / `vibrant` / `natural` |
| `color_scheme` | string | `"warm_orange"` | `warm_orange` / `tech_cyber` / `tech_green` / `minimal_bw` / `business_blue` / `vibrant_neon` |
| `callback_url` | string | `""` | 回调地址 |

---

### POST `/api/v1/generate/ppt` — AI PPT 生成

根据内容计划和风格模板，逐页生成 PPT 幻灯片图片。

**请求体：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `slides_plan` | string | **必填** | JSON 格式的幻灯片内容规划 |
| `style_template` | string | **必填** | 视觉风格描述 |
| `resolution` | string | `"2K"` | `1K` / `2K` |
| `callback_url` | string | `""` | 回调地址 |

---

### GET `/api/v1/workflows` — 列出可用工作流

无需请求体，返回所有可用的预设工作流列表。

**返回：**

```json
{
  "workflows": [
    {"id": "2603-wf-anime-production", "name": "AI 动画番剧生成", "description": "..."},
    {"id": "2603-wf-microfilm-production", "name": "AI 微电影生成", "description": "..."},
    {"id": "2603-wf-shadiao-comic", "name": "沙雕漫画生成", "description": "..."},
    {"id": "2603-wf-ecommerce-detail-page", "name": "电商套图生成", "description": "..."},
    {"id": "2603-wf-storyboard-grid", "name": "九宫格分镜生成", "description": "..."}
  ],
  "total": 5
}
```

---

### POST `/api/v1/workflows/{workflow_id}/run` — 执行工作流

**请求体：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `inputs` | dict | **必填** | 工作流输入变量（键: 黑板变量 ID，值: 输入内容） |
| `timeout` | int | `28800` | 超时秒数（默认 8 小时） |
| `callback_url` | string | `""` | 回调地址 |

**示例：**

```bash
curl -X POST http://43.156.26.92:8892/api/v1/workflows/2603-wf-anime-production/run \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: vk_xxx" \
  -d '{"inputs": {"story": "一个宇航员在月球上发现了外星文明的遗迹"}}'
```

---

### POST `/api/v1/analyze/image` — AI 图片理解

分析图片内容，回答关于图片的问题（**同步返回**，无需轮询）。

**请求体：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `image_urls` | list[string] | **必填** | 图片 URL 列表（支持 1-4 张） |
| `query` | string | `"Describe this image in detail."` | 分析问题 |

**返回：**

```json
{"result": "The image shows..."}
```

---

### POST `/api/v1/analyze/video` — AI 视频分析

分析视频内容，返回文字描述（**同步返回**，无需轮询）。

**请求体：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `video_url` | string | **必填** | 视频 URL |
| `query` | string | `"Describe this video in detail."` | 分析问题 |
| `subtask` | string | `""` | 子任务：`"script_analysis"` 启用完整短剧分析模式 |

---

### POST `/api/v1/analyze/script` — 短剧剧本分析

深度分析短剧视频，输出完整剧本文本 + 互动节点设计（分支选项/QTE）。

**请求体：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `video_url` | string | 短剧视频 URL |
| `original_script` | string | 已有剧本（可选，传入后进入重新设计互动节点模式） |
| `node_to_replace` | string | 要重新设计的特定节点 JSON（可选） |

---

### POST `/api/v1/analyze/characters` — 人物小传生成

根据故事文本，生成角色的详细人物小传（性格、背景、关系等）。

**请求体：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `story_text` | string | 故事/剧情文本 |
| `character_names` | list[string] | 要分析的角色名列表（可选，不传则自动提取所有角色） |

---

### 任务管理接口

**GET `/api/v1/jobs/{job_id}`** — 查询任务状态（含进度和结果）

返回：
```json
{
  "job_id": "job_xxxxxxxx",
  "type": "image_generation",
  "status": "success",
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-18T10:00:32Z",
  "metadata": {
    "points_consumed": 12,
    "model": "gemini-3.1-flash-image-preview"
  },
  "result": {
    "url": "https://oss.artclaw.app/...",
    "content_type": "image/png",
    "width": 1920,
    "height": 1080
  }
}
```

`metadata` 中的进度字段（按任务类型不同）：
- 工作流：`steps_completed`、`steps_total`、`current_step_name`
- 轮播图：`carousel_completed`、`carousel_total`
- PPT：`ppt_completed`、`ppt_total`
- 失败：`error_detail`

---

**GET `/api/v1/jobs`** — 列出历史任务

| 查询参数 | 类型 | 默认值 | 说明 |
|----------|------|--------|------|
| `status` | string | `""` | 过滤状态：`pending` / `running` / `success` / `failed` / `canceled` |
| `type` | string | `""` | 过滤类型：`image_generation` / `video_generation` / `marketing_image` / `product_carousel` / `ppt_generation` / `workflow` |
| `limit` | int | `20` | 返回条数（最大 100） |

---

**POST `/api/v1/jobs/{job_id}/cancel`** — 取消尚未完成的任务

---

**GET `/api/v1/account/info`** — 查询账户余额与用量

---

### Prompt 增强接口（免费，无需 API Key）

**POST `/api/v1/prompts/logo`** — 生成专业 Logo 提示词

```json
{
  "logo_type": "combination",
  "brand_name": "ACME",
  "industry": "tech",
  "style_options": "{}"
}
```

`logo_type` 可选：`wordmark` / `icon` / `combination` / `badge` / `abstract`
`industry` 可选：`tech` / `food` / `fashion` / `finance` / `education` / `healthcare` / `eco` / `entertainment`

返回：`{"prompt": "..."}`

---

**POST `/api/v1/prompts/cover`** — 生成封面图提示词

```json
{
  "subject": "日落海滩",
  "style": "cinematic",
  "composition": "rule_of_thirds",
  "color": "warm",
  "text_space": "top",
  "aspect_ratio": "16:9"
}
```

`style` 可选：`cinematic` / `minimalist` / `cyberpunk` / `illustration` / `photorealistic` / `abstract` / `vintage` / `flat`
`composition` 可选：`rule_of_thirds` / `centered` / `wide` / `close_up` / `top_down` / `isometric`
`color` 可选：`warm` / `cool` / `vibrant` / `muted` / `monochrome` / `high_contrast`

---

**POST `/api/v1/prompts/marketing`** — 智能增强营销提示词

```json
{"prompt": "蓝牙耳机广告图，科技感"}
```

返回：`{"prompt": "专业产品营销图片：蓝牙耳机广告图，科技感。视觉风格：现代科技风格..."}`

---

**POST `/api/v1/prompts/carousel`** — 生成整套轮播图提示词

```json
{
  "theme": "2026 AI 趋势",
  "style": "cyberpunk",
  "color_scheme": "tech_cyber",
  "title": "AI 大趋势",
  "count": 8
}
```

`color_scheme` 可选：`tech_cyber` / `warm_orange` / `minimal_bw` / `business_blue` / `vibrant_neon`

返回：
```json
{
  "theme": "2026 AI 趋势",
  "style": "cyberpunk",
  "color_scheme": "科技感 - 赛博蓝紫",
  "total_pages": 8,
  "prompts": [
    {"type": "cover", "page": 1, "title": "AI 大趋势", "prompt": "..."},
    {"type": "content", "page": 2, "prompt": "..."}
  ]
}
```

---

## 更新 Skill

本 Skill 托管在 GitHub 公开仓库，无需认证即可下载最新版本。

**一键更新（下载 tarball 覆盖）：**

```bash
curl -sL https://github.com/ArtClaw1/skills/archive/refs/heads/main.tar.gz \
  | tar xz --strip-components=1 -C /path/to/skills
```

**检查远程最新版本号：**

```bash
curl -sL https://raw.githubusercontent.com/ArtClaw1/skills/main/artclaw-creative-suite/manifest.json \
  | grep '"version"'
```

与本地 `manifest.json` 中的 `version` 字段对比，决定是否需要更新。

---

## Agent 行为规范

1. **提交任务后立即告知用户** — 不要沉默等待，说"已提交，正在生成..."
2. **按建议间隔轮询** — 图片 5s、视频 10s、工作流 15s
3. **生成完成后直接展示图片/视频 URL** — 不要只返回 job_id 给用户
4. **积分不足时引导充值** — https://staging.artclaw.com/#/settings
5. **支持并发** — 可同时提交多个任务，用 `GET /api/v1/jobs` 统一跟踪

## 错误处理

| HTTP 状态码 | 错误 | 原因 | 处理方式 |
|-------------|------|------|----------|
| `401` | `Unauthorized` | API Key 无效、缺失或已撤销 | 引导用户重新生成 Key |
| `402` / 业务错误 | 积分不足 | 账户余额不足 | 引导充值：https://staging.artclaw.com/#/settings |
| `404` | `Job not found` | job_id 不存在或已过期（24h） | 提示任务已过期，请重新生成 |
| `404` | `Workflow not found` | workflow_id 不存在 | 先调用 `GET /api/v1/workflows` 确认可用 ID |
| `429` | `Too Many Requests` | 超过频率限制 | 等待后重试，参见频率限制章节 |
