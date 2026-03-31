---
name: artclaw-creative-suite
description: |
  ARTCLAW AI Creative Suite — 通过 CLI 或 REST API 调用 ARTCLAW 平台的 AI 内容创作能力。
  支持 AI 生图、生视频、工作流执行、多模态分析、Prompt 优化等能力。
  所有生成类接口异步返回 job_id，需先获取 API Key 完成鉴权。
  触发关键词：生成图片、生成视频、AI绘画、文生图、文生视频、图生视频、营销图、
  Logo、封面、工作流、视频分析、图片分析、ARTCLAW、ArtClaw。
compatibility:
  dependencies:
    - ARTCLAW REST API (https://artclaw.com/api/v1)
    - Python 3.8+ with requests package
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

ARTCLAW 是一站式 AI 内容创作平台，提供图片生成、视频生成、多媒体分析、工作流编排等核心能力。

**推荐使用 CLI 工具** `scripts/artclaw.py` 来调用所有能力 — 它封装了完整的 API 交互（鉴权、提交、轮询、重试），输出标准 JSON，特别适合 Agent 自动化调用。

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

## 第一步：配置 API Key

除 Prompt 工具和 Key 验证外，所有功能均需 API Key（以 `vk_` 开头）。

> **如果用户还没有 API Key，请引导他们完成以下步骤：**

1. 打开 ARTCLAW 官网设置页：**https://artclaw.com/#/settings**
2. 在 **API Keys** 管理区域点击「创建」
3. 输入一个名称（如 `my-app`），确认后复制生成的 Key
4. Key 以 `vk_` 开头，**仅在创建时展示一次**，请妥善保存

配置方式（二选一）：

```bash
# 方式 1：环境变量（推荐）
export ARTCLAW_API_KEY=vk_your_key_here

# 方式 2：写入配置文件
python3 scripts/artclaw.py config-init --api-key "vk_your_key_here"
```

验证 Key 是否有效：

```bash
python3 scripts/artclaw.py verify-key --api-key "vk_your_key_here"
# 返回：{"status": "valid", "uin": "user_id"}
```

---

## CLI 工具：artclaw.py

`scripts/artclaw.py` 是本 Skill 的核心工具，覆盖 ArtClaw 全部 API 能力。

**特性：**
- 所有输出为 JSON（stdout），进度日志走 stderr，方便管道和解析
- 生成类命令默认自动等待完成（`--wait`），也可 `--no-wait` 立即返回
- 支持 `--dry-run` 预览请求内容（不发 API 调用）
- 内置指数退避重试、类型感知轮询（图片 5s、视频 10s、工作流 30s）
- 本地历史记录（`last-job` / `history`）

### 命令总览

| 类别 | 命令 | 说明 | 需要 Key |
|------|------|------|----------|
| **生图** | `generate-image` | 文生图 / 图生图 | ✅ |
| **生图** | `generate-marketing-image` | 营销广告图 | ✅ |
| **生视频** | `generate-video` | 文生视频 / 图生视频 | ✅ |
| **工作流** | `list-workflows` | 列出可用预设工作流 | ✅ |
| **工作流** | `run-workflow` | 执行预设工作流 | ✅ |
| **分析** | `analyze-image` | AI 图片理解 | ✅ |
| **分析** | `analyze-video` | AI 视频分析 | ✅ |
| **分析** | `analyze-script` | 剧本提取 + 互动节点 | ✅ |
| **分析** | `analyze-characters` | 人物小传提取 | ✅ |
| **任务** | `job-status` | 查询任务状态 | ✅ |
| **任务** | `list-jobs` | 列出历史任务 | ✅ |
| **任务** | `cancel-job` | 取消任务 | ✅ |
| **账户** | `account-info` | 查询余额与用量 | ✅ |
| **鉴权** | `verify-key` | 验证 API Key | ❌ |
| **Prompt** | `prompt-logo` | Logo 提示词（免费） | ❌ |
| **Prompt** | `prompt-cover` | 封面提示词（免费） | ❌ |
| **Prompt** | `prompt-marketing` | 营销提示词（免费） | ❌ |
| **Prompt** | `prompt-carousel` | 轮播图提示词（免费） | ❌ |
| **配置** | `config` | 查看当前配置 | ❌ |
| **配置** | `config-init` | 初始化/更新配置 | ❌ |
| **代理** | `spawn-task` | 生成 sessions_spawn 载荷 | ✅ |
| **历史** | `last-job` | 查看最近一次任务 | ❌ |
| **历史** | `history` | 查看本地任务历史 | ❌ |

---

### 生成图片

```bash
# 基本用法 — 提交并等待完成，返回完整结果 JSON
python3 scripts/artclaw.py generate-image \
    --prompt "赛博朋克城市夜景，霓虹灯倒映在雨水中" \
    --aspect-ratio 16:9

# 指定分辨率和参考图
python3 scripts/artclaw.py generate-image \
    --prompt "同风格的山水画" \
    --resolution 2K \
    --reference-urls https://example.com/style_ref.jpg

# 不等待，立即返回 job_id
python3 scripts/artclaw.py generate-image \
    --prompt "一只猫" --no-wait

# 预览请求（不实际调用 API）
python3 scripts/artclaw.py generate-image \
    --prompt "test" --aspect-ratio 1:1 --dry-run
```

**参数：**

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--prompt` | 图片描述（必填） | 文本 |
| `--aspect-ratio` | 宽高比 | `16:9` `9:16` `1:1` `4:3` `21:9` |
| `--resolution` | 分辨率 | `1K` `2K` `4K` |
| `--reference-urls` | 参考图 URL（可多个） | URL 列表 |
| `--model` | 模型覆盖 | 模型 ID |
| `--no-wait` | 提交后立即返回 | 标志位 |
| `--callback-url` | 完成回调 Webhook | URL |
| `--dry-run` | 预览请求，不调用 API | 标志位 |

### 生成视频

```bash
python3 scripts/artclaw.py generate-video \
    --prompt "海浪拍打礁石，慢镜头" \
    --aspect-ratio 16:9 \
    --duration 5 \
    --resolution 720p

# 图生视频（I2V）
python3 scripts/artclaw.py generate-video \
    --prompt "让画面中的人物转头微笑" \
    --reference-urls https://example.com/portrait.jpg
```

**参数：**

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--prompt` | 视频描述（必填） | 文本 |
| `--aspect-ratio` | 宽高比 | `16:9` `9:16` `1:1` `4:3` `21:9` |
| `--duration` | 时长（秒） | `2` - `12` |
| `--resolution` | 分辨率 | `480p` `720p` `1080p` |
| `--reference-urls` | 参考图 URL（I2V） | URL 列表 |
| `--model` | 模型覆盖 | 模型 ID |
| `--no-wait` / `--callback-url` / `--dry-run` | 同上 | |

### 生成营销图

```bash
python3 scripts/artclaw.py generate-marketing-image \
    --prompt "夏日清凉饮品促销海报" \
    --size 1080x1920
```

### 工作流

```bash
# 列出所有可用工作流
python3 scripts/artclaw.py list-workflows

# 执行工作流
python3 scripts/artclaw.py run-workflow \
    --workflow-id "text-to-image-basic" \
    --inputs '{"prompt": "动漫风格的森林"}'
```

### 多模态分析（同步返回）

分析命令直接返回结果，无需轮询。

```bash
# 图片分析
python3 scripts/artclaw.py analyze-image \
    --reference-urls https://example.com/photo.jpg \
    --query "描述这张图片的主要内容"

# 视频分析
python3 scripts/artclaw.py analyze-video \
    --reference-urls https://example.com/clip.mp4 \
    --query "总结视频内容"

# 剧本提取
python3 scripts/artclaw.py analyze-script \
    --reference-paths https://example.com/drama.mp4

# 人物小传
python3 scripts/artclaw.py analyze-characters \
    --text "李明是一个性格内向但才华横溢的程序员..."
```

### Prompt 工具（免费，无需 API Key）

```bash
# Logo 提示词
python3 scripts/artclaw.py prompt-logo \
    --brand-name "AcmeCorp" \
    --logo-type icon \
    --industry tech

# 封面提示词
python3 scripts/artclaw.py prompt-cover \
    --subject "科技发布会" \
    --style "极简" \
    --aspect-ratio 16:9

# 营销图提示词增强
python3 scripts/artclaw.py prompt-marketing \
    --prompt "夏日冰淇淋促销"

# 轮播图提示词
python3 scripts/artclaw.py prompt-carousel \
    --theme "产品功能介绍" \
    --count 5
```

### 任务管理

```bash
# 查询任务状态
python3 scripts/artclaw.py job-status --job-id "job_xxxxxxxx"

# 列出历史任务
python3 scripts/artclaw.py list-jobs --status success --limit 10

# 取消任务
python3 scripts/artclaw.py cancel-job --job-id "job_xxxxxxxx"

# 查看账户余额
python3 scripts/artclaw.py account-info
```

### 本地历史

CLI 会自动在 `~/.openclaw/workspace/artclaw/` 保存任务记录。

```bash
# 查看最近一次任务
python3 scripts/artclaw.py last-job

# 查看历史（默认最近 20 条）
python3 scripts/artclaw.py history --limit 50
```

### Agent 异步委托（spawn-task）

用于生成 `sessions_spawn` 载荷，让另一个 Agent 异步执行生成任务并投递结果。

```bash
python3 scripts/artclaw.py spawn-task \
    --subcommand generate-video \
    --prompt "产品宣传片" \
    --aspect-ratio 16:9 \
    --duration 8 \
    --deliver-to ou_xxxxxx \
    --deliver-channel feishu
```

返回的 JSON 包含 `sessions_spawn_args`，可直接传给 OpenClaw `sessions_spawn` 工具。

---

## 核心概念

### 异步生成模式

生成类命令（`generate-image`、`generate-video`、`generate-marketing-image`、`run-workflow`）均为异步模式：

1. CLI 提交任务 → 获得 `job_id`
2. 自动按类型轮询 `job-status`（图片 5s、视频 10s、工作流 30s）
3. 状态变为 `success` 后返回完整结果

使用 `--no-wait` 可跳过自动轮询，立即返回 `job_id` 供后续手动查询。

### 任务状态

| status | 含义 |
|--------|------|
| `upload` | 上传中（极短暂） |
| `pending` | 排队等待中 |
| `running` | 生成中 |
| `success` | 已完成，结果包含 URL |
| `failed` | 失败，查看 `metadata.error_detail` |
| `canceled` | 已取消 |
| `expired` | 已过期（24 小时） |

> **注意：** 任务可能长时间处于 `pending` 状态（排队中），这不是错误。如果 pending 超过 2 分钟，应安抚用户。

### 回调通知（Webhook）

所有生成命令支持 `--callback-url`。任务到达终态时服务器自动 POST 通知：

```json
{
  "event": "job.completed",
  "job_id": "job_xxxxxxxx",
  "type": "image_generation",
  "status": "success",
  "result": { "url": "https://oss.artclaw.app/..." },
  "timestamp": "2026-03-18T10:01:05Z"
}
```

Header 含 `X-Vicoo-Signature`（HMAC-SHA256）用于校验真实性。

---

## IM 渠道投递指南

生成完成后，Agent 应使用原生消息类型投递结果，而非仅发送 URL 链接。

### 飞书（Feishu / Lark）

```bash
python3 scripts/feishu_send_video.py \
    --video /path/to/video.mp4 \
    --to ou_xxx \
    --cover-url https://oss.artclaw.app/cover.jpg \
    --duration 20875
```

**关键：** `msg_type` 必须是 `media`；`duration` 单位是**毫秒**；凭证从 `~/.openclaw/openclaw.json` → `channels.feishu` 读取。

### Telegram

```bash
TELEGRAM_BOT_TOKEN=<token> python3 scripts/telegram_send_video.py \
    --video /path/to/video.mp4 \
    --to <chat_id> \
    --cover-url https://oss.artclaw.app/cover.jpg \
    --duration 5 \
    --caption "视频已生成！"
```

**关键：** `duration` 单位是**秒**（与飞书不同）；Bot Token **必须**通过环境变量提供。

### 投递行为规范

1. **优先原生消息** — 视频用原生视频消息，图片用原生图片消息，**不要**仅发 URL
2. **自动选择渠道** — 根据当前 IM 渠道选择对应脚本
3. **先下载再发送** — 从结果 URL 下载到本地，再通过脚本上传
4. **附带封面** — 发送视频时尽量提供封面图

---

## 不同 Agent 框架的使用方式

`artclaw.py` 是通用的 CLI 工具，任何 Agent 框架都可以调用。但 **异步生成任务（图片 ~30s，视频 ~5min，工作流 ~15min）** 的处理方式因框架而异：

### OpenClaw Agent（推荐：spawn 模式）

OpenClaw 原生支持 `sessions_spawn` 工具，可以将耗时任务派生给子 Agent 异步执行，主 Agent 不阻塞。

**生成视频时：**

```bash
# 1. 主 Agent 调用 --spawn，获得 sessions_spawn_args
python3 scripts/artclaw.py generate-video \
    --prompt "产品宣传片" \
    --duration 8 \
    --spawn \
    --deliver-to ou_xxxxxx \
    --deliver-channel feishu
# → 输出 JSON 中的 sessions_spawn_args

# 2. 主 Agent 把 sessions_spawn_args 传给 sessions_spawn 工具，立即返回
# 3. 子 Agent 在后台运行，完成后自动推送结果到飞书
```

**生成图片时（时间短，也可直接运行）：**

```bash
# 直接运行（~30s，主 Agent 内同步等待也可以接受）
python3 scripts/artclaw.py generate-image --prompt "赛博朋克城市" --aspect-ratio 16:9

# 或者 spawn 模式（与视频一致的处理方式）
python3 scripts/artclaw.py generate-image --prompt "赛博朋克城市" --spawn --deliver-to ou_xxx --deliver-channel feishu
```

**工作流（时间不可控，强烈建议 spawn）：**

```bash
python3 scripts/artclaw.py run-workflow \
    --workflow-id nine_grid_storyboard \
    --inputs '{"prompt": "赛博朋克短片"}' \
    --spawn \
    --deliver-to ou_xxxxxx \
    --deliver-channel feishu
```

> **凭证前提（使用 `--deliver-channel` 前必须配置）：**
>
> `--spawn` 生成的投递指令依赖 IM 渠道凭证，由投递脚本自动读取，**不通过 artclaw.py 传递**：
>
> | 渠道 | 凭证来源 | 配置方式 |
> |------|---------|---------|
> | `feishu` | `~/.openclaw/openclaw.json` → `channels.feishu.accounts.main` | 写入 `appId` / `appSecret` |
> | `telegram` | 环境变量 `TELEGRAM_BOT_TOKEN` | `export TELEGRAM_BOT_TOKEN=xxx` |
> | `discord` | 框架自身（message 工具） | 无需额外配置 |
>
> OpenClaw 的子 Agent 与父 Agent 运行在同一台机器上，凭证自动共享。
> 若凭证未配置，子 Agent 会报错；请先在宿主机完成 IM 渠道配置再使用 spawn 投递。

---

### 通用 Agent 框架（Claude、GPT、Gemini 等）

不具备 `sessions_spawn` 机制。使用 `--no-wait` + 轮询策略处理耗时任务：

```bash
# 1. 提交任务，立即获得 job_id（不阻塞）
job_id=$(python3 scripts/artclaw.py generate-video \
    --prompt "产品宣传片" --duration 8 --no-wait | jq -r '.job_id')

# 告知用户"已提交，大约需要 3~5 分钟"

# 2. 用户询问进度时，查询状态
python3 scripts/artclaw.py job-status --job-id "$job_id"

# 3. 或直接等待（适合图片等短任务）
python3 scripts/artclaw.py generate-image --prompt "赛博朋克城市"
# 默认自动轮询，完成后返回结果
```

**建议策略：**
- 图片（~30s）：直接运行，同步等待
- 视频（~5min）：`--no-wait` 提交，提示用户等待，用户追问时再查询
- 工作流（~15min）：`--no-wait` 提交，主动告知大致时间，建议用户稍后查询


---

## Agent 行为规范

1. **提交任务后立即告知用户** — 不要沉默等待，说"已提交，正在生成..."
2. **使用 CLI 而非手动 curl** — `artclaw.py` 已封装重试、轮询、错误处理
3. **生成完成后直接展示结果 URL** — 不要只返回 job_id 给用户
4. **积分不足时引导充值** — https://artclaw.com/#/settings
5. **支持并发** — 可同时提交多个 `--no-wait` 任务，用 `job-status` 分别跟踪

## 错误处理

| 错误 | 原因 | 处理方式 |
|------|------|----------|
| `401 Unauthorized` | API Key 无效/缺失/已撤销 | 引导用户重新生成 Key |
| `402` / 积分不足 | 账户余额不足 | 引导充值：https://artclaw.com/#/settings |
| `404 Job not found` | job_id 不存在或已过期（24h） | 提示任务已过期，请重新生成 |
| `404 Workflow not found` | workflow 不存在 | 先 `list-workflows` 确认可用 ID |
| `429 Too Many Requests` | 超过频率限制（120 次/分钟） | 等待后重试 |

---

## 附录：REST API 参考

以下是 `artclaw.py` 底层调用的 REST API 端点。**通常直接使用 CLI 即可，无需手动调用。**

**基地址：** `https://artclaw.com/api/v1`

> **⚠️ 尾部斜杠：** `/jobs/` 和 `/workflows/` 列表接口需要尾部斜杠，否则 307 → 502。单条资源接口（如 `/jobs/{id}`）无需尾部斜杠。

### 鉴权

HTTP Header `X-API-KEY: vk_your_key_here`。Prompt 工具（`/prompts/*`）和 `/auth/verify` 无需 Key。

频率限制：**120 次/分钟**（按用户维度），超限返回 `429`。

### 端点列表

| 类别 | 方法 | 路径 | 说明 | CLI 命令 |
|------|------|------|------|----------|
| 生图 | POST | `/generate/image` | 文生图/图生图 | `generate-image` |
| 生图 | POST | `/generate/marketing-image` | 营销图 | `generate-marketing-image` |
| 生视频 | POST | `/generate/video` | 文生视频/图生视频 | `generate-video` |
| 分析 | POST | `/analyze/image` | 图片理解 | `analyze-image` |
| 分析 | POST | `/analyze/video` | 视频分析 | `analyze-video` |
| 分析 | POST | `/analyze/script` | 剧本提取 | `analyze-script` |
| 分析 | POST | `/analyze/characters` | 人物小传 | `analyze-characters` |
| 工作流 | GET | `/workflows/` | 列出工作流 | `list-workflows` |
| 工作流 | POST | `/workflows/{id}/run` | 执行工作流 | `run-workflow` |
| 任务 | GET | `/jobs/{job_id}` | 查询状态 | `job-status` |
| 任务 | GET | `/jobs/` | 列出任务 | `list-jobs` |
| 任务 | POST | `/jobs/{job_id}/cancel` | 取消任务 | `cancel-job` |
| 账户 | GET | `/account/info` | 余额用量 | `account-info` |
| 鉴权 | POST | `/auth/verify` | 验证 Key | `verify-key` |
| Prompt | POST | `/prompts/logo` | Logo 提示词 | `prompt-logo` |
| Prompt | POST | `/prompts/cover` | 封面提示词 | `prompt-cover` |
| Prompt | POST | `/prompts/marketing` | 营销提示词 | `prompt-marketing` |
| Prompt | POST | `/prompts/carousel` | 轮播图提示词 | `prompt-carousel` |

### 直接调用示例（curl）

```bash
API_KEY="vk_your_key_here"
BASE="https://artclaw.com/api/v1"

# 提交生成任务
gen_resp=$(curl -sL -X POST "$BASE/generate/image" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"prompt": "赛博朋克城市夜景", "aspect_ratio": "16:9"}')
job_id=$(echo "$gen_resp" | jq -r '.job_id')

# 轮询状态
while true; do
  sleep 5
  status_resp=$(curl -sL "$BASE/jobs/$job_id" -H "X-API-KEY: $API_KEY")
  status=$(echo "$status_resp" | jq -r '.status')
  if [[ "$status" == "success" ]]; then
    echo "图片URL: $(echo "$status_resp" | jq -r '.result.url')"
    break
  elif [[ "$status" == "failed" ]]; then
    echo "失败: $(echo "$status_resp" | jq -r '.metadata.error_detail')"
    break
  fi
done
```

> **建议：** 直接使用 `python3 scripts/artclaw.py generate-image --prompt "赛博朋克城市夜景"` 可一步完成上述全部流程。
