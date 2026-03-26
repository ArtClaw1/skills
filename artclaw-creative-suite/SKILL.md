---
name: artclaw-creative-suite
description: |
  ARTCLAW AI Creative Suite — 通过 REST API 调用 ARTCLAW 平台的 AI 内容创作能力。
  支持 AI 生图、生视频、工作流执行、多模态分析、Prompt 优化等能力。
  所有生成类接口异步返回 job_id，需先获取 API Key 完成鉴权。
  触发关键词：生成图片、生成视频、AI绘画、文生图、文生视频、图生视频、营销图、
  Logo、封面、工作流、视频分析、图片分析、ARTCLAW、ArtClaw。
compatibility:
  dependencies:
    - ARTCLAW REST API (https://artclaw.com/api/v1)
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires":
          {
            "env": ["ARTCLAW_API_KEY"]
          },
        "primaryEnv": "ARTCLAW_API_KEY"
      }
  }
---

# ARTCLAW AI Creative Suite

ARTCLAW 是一站式 AI 内容创作平台，通过 REST API 对外提供图片生成、视频生成、多媒体分析、工作流编排等核心能力。

**API 基地址：** `https://artclaw.com/api/v1`

>
> **⚠️ 尾部斜杠：** `/jobs` 和 `/workflows` 列表接口需要添加尾部斜杠（`/jobs/`、`/workflows/`），否则会产生指向内部地址的 307 重定向，导致 502 错误。单条资源接口（如 `/jobs/{id}`、`/workflows/{id}/run`）无需尾部斜杠。

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

🎬 AI 生视频
  • 文生视频 / 图生视频 — 让静态画面动起来

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

除 Prompt 工具（`/prompts/*`）和 Key 验证（`/auth/verify`）外，所有接口均需通过 HTTP Header `X-API-KEY` 传递 API Key 鉴权。未携带或无效 Key 将返回 `401 Unauthorized`。

> **如果用户还没有 API Key，请引导他们完成以下步骤：**

1. 打开 ARTCLAW 官网设置页：**https://artclaw.com/#/settings**
2. 在 **API Keys** 管理区域点击「创建」
3. 输入一个名称（如 `my-app`），确认后复制生成的 Key
4. Key 以 `vk_` 开头，**仅在创建时展示一次**，请妥善保存

> 获取 Key 后，在每次 HTTP 请求中通过 Header 传入：
> ```
> X-API-KEY: vk_your_key_here
> ```

可以调用验证接口确认 Key 有效：

```bash
curl -L -X POST https://artclaw.com/api/v1/auth/verify \
  -H "Content-Type: application/json" \
  -d '{"api_key": "vk_your_key_here"}'
```

返回：
```json
{"status": "valid", "uin": "user_id"}
```

错误返回：
- Key 无效 → `401`：`{"detail": "API Key is invalid or revoked"}`
- 格式错误（缺少 `vk_` 前缀）→ `400`：`{"detail": "Invalid API Key format. Expected vk_ prefix."}`

---

## 能力总览

| 类别 | 接口 | 方法 | 说明 | 需要 Key |
|------|------|------|------|----------|
| **生图** | `/api/v1/generate/image` | POST | 文生图 / 图生图（支持参考图） | ✅ |
| **生图** | `/api/v1/generate/marketing-image` | POST | 营销广告图（自动增强提示词） | ✅ |
| **生视频** | `/api/v1/generate/video` | POST | 文生视频 / 图生视频（I2V） | ✅ |
| **分析** | `/api/v1/analyze/image` | POST | AI 图片理解与描述 | ✅ |
| **分析** | `/api/v1/analyze/video` | POST | AI 视频内容分析 | ✅ |
| **分析** | `/api/v1/analyze/script` | POST | 从视频提取剧本 + 互动节点设计 | ✅ |
| **分析** | `/api/v1/analyze/characters` | POST | 从故事文本生成人物小传 | ✅ |
| **工作流** | `/api/v1/workflows/` | GET | 列出所有可用预设工作流 | ✅ |
| **工作流** | `/api/v1/workflows/{id}/run` | POST | 执行预设工作流 | ✅ |
| **任务管理** | `/api/v1/jobs/{job_id}` | GET | 查询任务状态和结果 | ✅ |
| **任务管理** | `/api/v1/jobs/` | GET | 列出历史任务 | ✅ |
| **任务管理** | `/api/v1/jobs/{job_id}/cancel` | POST | 取消正在进行的任务 | ✅ |
| **账户** | `/api/v1/account/info` | GET | 查询账户余额与用量 | ✅ |
| **鉴权** | `/api/v1/auth/verify` | POST | 验证 API Key 有效性 | ❌ |
| **Prompt** | `/api/v1/prompts/logo` | POST | 生成 Logo 提示词（免费） | ❌ |
| **Prompt** | `/api/v1/prompts/cover` | POST | 生成封面图提示词（免费） | ❌ |
| **Prompt** | `/api/v1/prompts/marketing` | POST | 增强营销图提示词（免费） | ❌ |
| **Prompt** | `/api/v1/prompts/carousel` | POST | 生成轮播图提示词（免费） | ❌ |

---

## 频率限制

所有接口统一限制 **120 次/分钟**（按用户维度），超限返回 `429 Too Many Requests`。

---

## 核心模式：异步生成

**生成类接口**（图片/视频/工作流）均为异步模式。调用后返回 `job_id`，需要由 client 轮询状态直到完成。

> **注意：** 分析类接口（`/analyze/*`）是**同步**的，直接返回 `result` 字段，不返回 `job_id`。



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
| `upload` | 上传中，预期很短很短 | 
| `pending` | 排队等待中 |
| `running` | 生成中 |
| `success` | 已完成，`result` 字段包含结果 URL |
| `failed` | 失败，检查 `metadata.error_detail` |
| `canceled` | 已取消 |
| `expired` | 已过期（24小时） |

### 轮询间隔建议

| 任务类型 | 轮询间隔 | 超时上限 |
|----------|----------|----------|
| 图片 | 5s | 5 min |
| 视频 | 10s | 10 min |
| 工作流 | 30-60s | 30min |

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

## 调用流程示例

```bash
API_KEY="vk_your_key_here"
BASE="https://artclaw.com/api/v1"

# 1. 提交生成任务
gen_resp=$(curl -sL -X POST "$BASE/generate/image" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"prompt": "赛博朋克城市夜景", "aspect_ratio": "16:9"}')
job_id=$(echo "$gen_resp" | jq -r '.job_id')

# 2. 轮询状态
while true; do
  sleep 5
  status_resp=$(curl -sL "$BASE/jobs/$job_id" -H "X-API-KEY: $API_KEY")
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

---

## IM 渠道投递指南

生成完成后，Agent 应使用原生消息类型投递结果，而非仅发送 URL 链接。通过 `scripts/` 下的脚本执行实际投递。

### 飞书（Feishu / Lark）

```bash
python3 scripts/feishu_send_video.py \
    --video /path/to/video.mp4 \
    --to ou_xxx \
    --cover-url https://oss.artclaw.app/cover.jpg \
    --duration 20875
```

**关键注意事项：** `msg_type` 必须是 `media`（不是 `video`/`file`）；`duration` 单位是**毫秒**；凭证从 `~/.openclaw/openclaw.json` 的 `channels.feishu` 读取。

### Telegram

```bash
TELEGRAM_BOT_TOKEN=<token> python3 scripts/telegram_send_video.py \
    --video /path/to/video.mp4 \
    --to <chat_id> \
    --cover-url https://oss.artclaw.app/cover.jpg \
    --duration 5 \
    --caption "视频已生成！"
```

**关键注意事项：** `duration` 单位是**秒**（与飞书不同）；Bot Token **必须**通过环境变量提供，不可通过 CLI 参数传递。

### Agent 行为规范

1. **优先原生消息** — 视频用原生视频消息，图片用原生图片消息，**不要**仅发 URL
2. **自动选择渠道** — 根据当前 IM 渠道选择对应脚本
3. **先下载再发送** — 从生成结果 URL 下载到本地，再通过脚本上传
4. **附带封面** — 发送视频时尽量提供封面图，提升用户体验

---

## Agent 行为规范

1. **提交任务后立即告知用户** — 不要沉默等待，说"已提交，正在生成..."
2. **按建议间隔轮询** — 图片 5s、视频 10s、工作流 30s
3. **生成完成后直接展示图片/视频 URL** — 不要只返回 job_id 给用户
4. **积分不足时引导充值** — https://artclaw.com/#/settings
5. **支持并发** — 可同时提交多个任务，用 `GET /api/v1/jobs/` 统一跟踪

## 错误处理

| HTTP 状态码 | 错误 | 原因 | 处理方式 |
|-------------|------|------|----------|
| `401` | `Unauthorized` | API Key 无效、缺失或已撤销 | 引导用户重新生成 Key |
| `402` / 业务错误 | 积分不足 | 账户余额不足 | 引导充值：https://artclaw.com/#/settings |
| `404` | `Job not found` | job_id 不存在或已过期（24h） | 提示任务已过期，请重新生成 |
| `404` | `Workflow not found` | workflow 不存在 | 先调用 `GET /api/v1/workflows/` 确认可用 ID |
| `429` | `Too Many Requests` | 超过频率限制 | 等待后重试，参见频率限制章节 |
