---
name: vicoo-creative-suite
description: |
  VICOO AI Creative Suite — 通过 MCP 协议调用 VICOO 平台的 AI 内容创作能力。
  支持 AI 生图、生视频、PPT 生成、工作流执行、多模态分析、Prompt 优化等能力。
  所有生成类接口异步返回 job_id，需先获取 API Key 完成鉴权。
  触发关键词：生成图片、生成视频、AI绘画、文生图、文生视频、图生视频、营销图、轮播图、
  产品图、Logo、封面、工作流、视频分析、图片分析、VICOO、ArtClaw。
compatibility:
  tools:
    - vicoo-mcp-server (all ArtClaw tools)
  dependencies:
    - VICOO MCP Server (Streamable HTTP, http://43.156.26.92:8892/mcp)
---

# VICOO AI Creative Suite

VICOO 是一站式 AI 内容创作平台，通过 MCP 协议对外提供图片生成、视频生成、多媒体分析、工作流编排等核心能力。

**MCP 服务器地址：** `http://43.156.26.92:8892/mcp`

---

## 第一步：获取 API Key

所有生成类工具需要 API Key 鉴权。每次调用工具时将 key 传入 `api_key` 参数。

> **如果用户还没有 API Key，请引导他们完成以下步骤：**

1. 打开 VICOO 官网设置页：**https://staging.vicoo.ai/#/settings**
2. 在 **API Keys** 管理区域点击「创建」
3. 输入一个名称（如 `openclaw`），确认后复制生成的 Key
4. Key 以 `vk_` 开头，**仅在创建时展示一次**，请妥善保存

> 获取 Key 后，在每次调用 MCP 工具时传入 `api_key` 参数：
> ```
> api_key = "vk_your_key_here"
> ```

---

## 第二步：配置 MCP 连接

在你的 Agent（如 OpenClaw、Claude Desktop 等）中添加以下 MCP 服务器配置：

```json
{
  "mcpServers": {
    "vicoo": {
      "url": "http://43.156.26.92:8892/mcp"
    }
  }
}
```

如果你是使用 OpenClaw，可以在 `config.json` 的 `mcpServers` 字段添加上述配置。对于其他 Agent，请参考其文档添加 MCP 服务器。
或者使用 McpPorter 进行配置。

---

## 备用方案：直接 HTTP 调用 MCP

如果你的 Agent 不支持 MCP 协议，可以通过标准 HTTP 请求直接调用 MCP 服务器。

**端点：** `POST http://43.156.26.92:8892/mcp`

### 注意事项

- 请求头必须同时接受 `application/json` 和 `text/event-stream`
- 所有请求体均为 **JSON-RPC 2.0** 格式
- **必须先调用 `initialize`** 获取 `mcp-session-id`，后续所有请求都需要在 Header 中携带此 ID

### 第一步：初始化会话

```bash
curl -X POST http://43.156.26.92:8892/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": { "name": "my-agent", "version": "1.0" }
    }
  }'
```

**返回示例：**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": { "tools": {} },
    "serverInfo": { "name": "vicoo-mcp-server", "version": "1.0" }
  }
}
```

响应头中会包含 `mcp-session-id`，后续所有请求必须携带：

```
mcp-session-id: <从响应 Header 中读取>
```

### 第二步：调用工具

以调用 `generate_image` 为例：

```bash
curl -X POST http://43.156.26.92:8892/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <your-session-id>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "generate_image",
      "arguments": {
        "prompt": "赛博朋克城市夜景",
        "aspect_ratio": "16:9",
        "api_key": "vk_your_key_here"
      }
    }
  }'
```

**返回示例：**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"job_id\": \"job_xxxxxxxx\", \"status\": \"pending\", \"message\": \"...\"}"
      }
    ]
  }
}
```

> `result.content[0].text` 是工具返回的 JSON 字符串，需要再次解析。

### 查询工具列表

```bash
curl -X POST http://43.156.26.92:8892/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <your-session-id>" \
  -d '{"jsonrpc": "2.0", "id": 3, "method": "tools/list", "params": {}}'
```


### 完整调用流程（伪代码）

#### Bash 伪代码（curl）

```bash
# 1. 初始化，获取 session_id
init_resp=$(curl -i -s -X POST "http://43.156.26.92:8892/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "agent", "version": "1.0"}}}')
# 提取 session_id
session_id=$(echo "$init_resp" | grep -i 'mcp-session-id:' | awk '{print $2}' | tr -d '\r')

# 2. 调用工具（如 generate_image）
gen_resp=$(curl -s -X POST "http://43.156.26.92:8892/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: $session_id" \
  -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "generate_image", "arguments": {"prompt": "赛博朋克城市夜景", "aspect_ratio": "16:9", "api_key": "vk_xxx"}}}')
# 提取 job_id
job_id=$(echo "$gen_resp" | jq -r '.result.content[0].text' | jq -r '.job_id')

# 3. 轮询状态
while true; do
  sleep 5
  status_resp=$(curl -s -X POST "http://43.156.26.92:8892/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "mcp-session-id: $session_id" \
    -d '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_job_status", "arguments": {"job_id": "'$job_id'", "api_key": "vk_xxx"}}}')
  status=$(echo "$status_resp" | jq -r '.result.content[0].text' | jq -r '.status')
  if [[ "$status" == "success" ]]; then
    url=$(echo "$status_resp" | jq -r '.result.content[0].text' | jq -r '.result.url')
    echo "图片URL: $url"
    break
  elif [[ "$status" == "failed" ]]; then
    echo "失败: $(echo "$status_resp" | jq -r '.result.content[0].text')"
    break
  fi
done
```

#### Python 伪代码

```python
import httpx, json

BASE = "http://43.156.26.92:8892/mcp"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}

# 1. 初始化，获取 session_id
resp = httpx.post(BASE, headers=HEADERS, json={
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "agent", "version": "1.0"}}
})
session_id = resp.headers["mcp-session-id"]
HEADERS["mcp-session-id"] = session_id

# 2. 调用工具
resp = httpx.post(BASE, headers=HEADERS, json={
    "jsonrpc": "2.0", "id": 2, "method": "tools/call",
    "params": {
        "name": "generate_image",
        "arguments": {"prompt": "赛博朋克城市夜景", "aspect_ratio": "16:9", "api_key": "vk_xxx"}
    }
})
result = json.loads(resp.json()["result"]["content"][0]["text"])
job_id = result["job_id"]

# 3. 轮询状态
import time
while True:
    time.sleep(5)
    resp = httpx.post(BASE, headers=HEADERS, json={
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": "get_job_status", "arguments": {"job_id": job_id, "api_key": "vk_xxx"}}
    })
    status_data = json.loads(resp.json()["result"]["content"][0]["text"])
    if status_data["status"] == "success":
        print("图片URL:", status_data["result"]["url"])
        break
    elif status_data["status"] == "failed":
        print("失败:", status_data)
        break
```

---

## 能力总览

| 类别 | MCP 工具 | 说明 | 是否需要 Key |
|------|----------|------|--------------|
| **生图** | `generate_image` | 文生图 / 图生图（支持参考图） | ✅ |
| **生图** | `generate_marketing_image` | 营销广告图（自动增强提示词） | ✅ |
| **生图** | `generate_product_carousel` | 产品套图（多图轮播，自动风格匹配） | ✅ |
| **生视频** | `generate_video` | 文生视频 / 图生视频（I2V） | ✅ |
| **生文/分析** | `view_image` | AI 图片理解与描述 | ✅ |
| **生文/分析** | `view_video` | AI 视频内容分析 | ✅ |
| **生文/分析** | `analyze_video_script` | 短剧剧本分析 + 互动节点设计 | ✅ |
| **生文/分析** | `analyze_character_profiles` | 从故事文本生成人物小传 | ✅ |
| **PPT** | `generate_ppt_slides` | AI PPT 幻灯片生成（多页图片） | ✅ |
| **工作流** | `list_workflows` | 列出所有可用预设工作流 | ✅ |
| **工作流** | `run_workflow` | 执行预设工作流（动画/微电影/漫画等） | ✅ |
| **任务管理** | `get_job_status` | 查询异步任务状态和进度 | ✅ |
| **任务管理** | `get_job_result` | 获取已完成任务的结果 | ✅ |
| **任务管理** | `list_jobs` | 列出历史任务 | ✅ |
| **任务管理** | `cancel_job` | 取消正在进行的任务 | ✅ |
| **Prompt 工具** | `generate_logo_prompt` | 生成 Logo 提示词（免费） | ❌ |
| **Prompt 工具** | `generate_cover_prompt` | 生成封面图提示词（免费） | ❌ |
| **Prompt 工具** | `enhance_marketing_prompt` | 增强营销图提示词（免费） | ❌ |
| **Prompt 工具** | `generate_carousel_prompts` | 生成轮播图提示词系列（免费） | ❌ |

---

## 核心模式：异步生成

**所有生成类工具**（图片/视频/PPT/工作流）均为异步模式。调用后立即返回 `job_id`，需轮询状态直到完成。

### 标准流程

```
1. 调用生成工具 → 获得 job_id
2. 立即告知用户"已提交生成任务，等待完成"
3. 刚提交的任务不会马上完成，以一定间隔（大约5s，最多不超过10s）调用 get_job_status(job_id) 检查状态。注意，任务可能非常耗时，因为可能在队列中，不要因为pending持续很久就认为出错了
4. 如果pending超过2分钟，可以安抚一下用户，告诉他们生成可能需要一些时间，并且我们会持续更新状态。之后也要间隔安抚。
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

### 返回示例

**提交后（任意生成工具）：**
```json
{
  "job_id": "job_xxxxxxxx",
  "type": "image_generation",
  "status": "pending",
  "message": "Job submitted. Use get_job_status('job_xxxxxxxx') to check progress."
}
```

**轮询完成（图片）：**
```json
{
  "job_id": "job_xxxxxxxx",
  "type": "image_generation",
  "status": "success",
  "result": {
    "url": "https://oss.vicoo.app/...",
    "content_type": "image/png",
    "width": 1920,
    "height": 1080
  }
}
```

---

## MCP 工具详细参数

### generate_image — 文生图 / 图生图

根据文本描述生成图片，支持传入参考图（图生图模式）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | **必填** | 图片描述文本 |
| `aspect_ratio` | string | `"16:9"` | 宽高比：`16:9` / `9:16` / `1:1` / `4:3` / `21:9` |
| `resolution` | string | `"1K"` | 分辨率：`1K` / `2K` / `4K` |
| `reference_paths` | list[string] | `[]` | 参考图，支持 http(s):// URL、本地路径 |
| `model` | string | 默认模型 | 指定模型 ID（可选） |
| `callback_url` | string | `""` | 任务完成后自动 POST 通知的回调地址 |
| `api_key` | string | `""` | **必填**，`vk_` 开头的 API Key |

**示例：**
```
generate_image(
  prompt="赛博朋克城市夜景，霓虹灯倒映在湿润的街道上",
  aspect_ratio="16:9",
  api_key="vk_xxx"
)
```

---

### generate_video — 文生视频 / 图生视频

根据文本描述生成视频；若传入参考图则进入图生视频（I2V）模式。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | **必填** | 视频描述 |
| `aspect_ratio` | string | `"16:9"` | `16:9` / `9:16` / `1:1` |
| `duration` | int | `5` | 时长（秒），范围 2-12 |
| `resolution` | string | `"1K"` | `480p` / `720p` / `1080p` / `1K` / `2K` |
| `reference_paths` | list[string] | `[]` | 参考图（传入后自动切换为图生视频模式） |
| `callback_url` | string | `""` | 回调地址 |
| `api_key` | string | `""` | **必填** |

**示例（文生视频）：**
```
generate_video(
  prompt="海浪拍打白色沙滩，金色傍晚阳光",
  duration=5,
  api_key="vk_xxx"
)
```

**示例（图生视频）：**
```
generate_video(
  prompt="人物缓慢回头，夕阳余晖",
  reference_paths=["https://example.com/portrait.jpg"],
  api_key="vk_xxx"
)
```

---

### generate_marketing_image — 营销广告图

根据简单描述自动增强风格，生成专业的营销类广告图片。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | **必填** | 营销图描述（如"蓝牙耳机广告"） |
| `size` | string | `"1080x1920"` | 图片尺寸，格式 `宽x高`（像素） |
| `callback_url` | string | `""` | 回调地址 |
| `api_key` | string | `""` | **必填** |

---

### generate_product_carousel — 产品套图（多图轮播）

为产品生成多张风格统一的轮播图（封面 + 内容页 + 背页），适合电商、小红书等场景。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `product_type` | string | **必填** | `skincare` / `coffee` / `tech` |
| `theme` | string | **必填** | 产品主题描述，如"春季护肤新品" |
| `product_name` | string | `""` | 产品名称，如"水光精华" |
| `style` | string | `"warm_cozy"` | `warm_cozy` / `cyberpunk` / `minimalist` / `professional` / `vibrant` / `natural` |
| `color_scheme` | string | `"warm_orange"` | `warm_orange` / `tech_cyber` / `tech_green` / `minimal_bw` / `business_blue` / `vibrant_neon` |
| `callback_url` | string | `""` | 回调地址 |
| `api_key` | string | `""` | **必填** |

---

### generate_ppt_slides — AI PPT 生成

根据内容计划和风格模板，逐页生成 PPT 幻灯片图片。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `slides_plan` | string | **必填** | JSON 格式的幻灯片内容规划 |
| `style_template` | string | **必填** | 视觉风格描述 |
| `resolution` | string | `"2K"` | `1K` / `2K` |
| `callback_url` | string | `""` | 回调地址 |
| `api_key` | string | `""` | **必填** |

---

### list_workflows — 列出可用工作流

无需参数（除 `api_key`），返回所有可用的预设工作流列表。

**内置工作流：**

| 工作流 ID | 名称 | 说明 |
|-----------|------|------|
| `2603-wf-anime-production` | AI 动画制作 | 输入故事主题，输出动画视频 |
| `2603-wf-microfilm-production` | AI 微电影制作 | 输入剧情，输出微电影 |
| `2603-wf-shadiao-comic` | 漫画生成 | 输入故事，输出漫画图片 |
| `2603-wf-ecommerce-detail-page` | 电商详情页 | 输入产品信息，输出详情页图片 |
| `2603-wf-storyboard-grid` | 九宫格分镜 | 输入剧本，输出分镜图 |

---

### run_workflow — 执行工作流

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `workflow_id` | string | **必填** | 工作流 ID（见上表） |
| `inputs` | dict | **必填** | 工作流输入变量（键: 黑板变量 ID，值: 输入内容） |
| `timeout` | int | `28800` | 超时秒数（默认 8 小时） |
| `callback_url` | string | `""` | 回调地址 |
| `api_key` | string | `""` | **必填** |

**示例：**
```
run_workflow(
  workflow_id="2603-wf-anime-production",
  inputs={"story": "一个宇航员在月球上发现了外星文明的遗迹"},
  api_key="vk_xxx"
)
```

---

### view_image — AI 图片理解

分析图片内容，回答关于图片的问题。输入图片 URL，返回文字描述/分析结果（同步返回，无需轮询）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `image_urls` | list[string] | **必填** | 图片 URL 列表（支持 1-4 张） |
| `query` | string | `"Describe this image in detail."` | 分析问题 |
| `api_key` | string | `""` | **必填** |

---

### view_video — AI 视频分析

分析视频内容，返回文字描述（同步返回，无需轮询）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `video_url` | string | **必填** | 视频 URL |
| `query` | string | `"Describe this video in detail."` | 分析问题 |
| `subtask` | string | `""` | 子任务：`"script_analysis"` 启用完整短剧分析模式 |
| `api_key` | string | `""` | **必填** |

---

### analyze_video_script — 短剧剧本分析

深度分析短剧视频，输出完整剧本文本 + 互动节点设计（分支选项/QTE）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `video_url` | string | 短剧视频 URL |
| `original_script` | string | 已有剧本（可选，用于重新设计互动节点） |
| `node_to_replace` | string | 要重新设计的特定节点（可选） |
| `api_key` | string | **必填** |

---

### analyze_character_profiles — 人物小传生成

根据故事文本，生成角色的详细人物小传（性格、背景、关系等）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `story_text` | string | 故事/剧情文本 |
| `character_names` | list[string] | 要分析的角色名列表 |
| `api_key` | string | **必填** |

---

### Prompt 增强工具（免费，无需 Key）

**`generate_logo_prompt`** — 生成专业 Logo 提示词
```
generate_logo_prompt(
  logo_type="wordmark",   # wordmark / icon / combination / badge / abstract
  brand_name="ACME",
  industry="tech"         # tech / food / fashion / finance / education / healthcare / eco / entertainment
)
```

**`generate_cover_prompt`** — 生成封面图提示词
```
generate_cover_prompt(
  subject="日落海滩",
  style="cinematic",          # cinematic / minimalist / cyberpunk / illustration / photorealistic / vintage
  composition="rule_of_thirds",  # rule_of_thirds / centered / wide / close_up / top_down / isometric
  color="warm"                # warm / cool / vibrant / muted / monochrome / high_contrast
)
```

**`enhance_marketing_prompt`** — 智能增强营销提示词（根据品类自动匹配风格）
```
enhance_marketing_prompt(simple_prompt="蓝牙耳机广告图，科技感")
```

**`generate_carousel_prompts`** — 生成整套轮播图提示词
```
generate_carousel_prompts(
  theme="2026 AI 趋势",
  style="cyberpunk",
  color_scheme="tech_cyber",  # tech_cyber / warm_orange / minimal_bw / business_blue / vibrant_neon
  title="AI 大趋势",
  count=8
)
```

---

### 任务管理工具

**`get_job_status(job_id, api_key)`** — 查询任务状态（含进度和结果）

**`get_job_result(job_id, api_key)`** — 仅当 `status=success` 时获取结果，未完成则报错

**`list_jobs(api_key, status="", type="", limit=20)`** — 列出历史任务
- `status` 过滤：`pending` / `running` / `success` / `failed` / `canceled`

**`cancel_job(job_id, api_key)`** — 取消尚未完成的任务

---

## Agent 行为规范

1. **提交任务后立即告知用户** — 不要沉默等待，说"已提交，正在生成..."
2. **按建议间隔轮询** — 图片 5s、视频 10s、工作流 15s
3. **生成完成后直接展示图片/视频 URL** — 不要只返回 job_id 给用户
4. **积分不足时引导充值** — https://staging.vicoo.ai/#/settings
5. **支持并发** — 可同时提交多个任务，用 `list_jobs` 统一跟踪

## 错误处理

| 错误 | 原因 | 处理方式 |
|------|------|----------|
| `API Key 无效或已撤销` | Key 格式错误或已删除 | 引导用户重新生成 Key |
| `积分不足` | 账户余额不足 | 引导充值：https://staging.vicoo.ai/#/settings |
| `Job not found` | job_id 不存在或已过期 | 提示任务已过期，请重新生成 |
| `未找到工作流` | workflow_id 不存在 | 先调用 `list_workflows` 确认可用 ID |
