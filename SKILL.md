---
name: artclaw-creative-suite
description: |
  ARTCLAW AI Creative Suite — invoke ARTCLAW platform's AI content creation capabilities via CLI.
  Supports AI image generation, video generation, workflow execution, multimodal analysis, and more.
  All generation commands must be executed asynchronously (spawn or background). Requires an API Key (prefixed with vk_) for authentication.
  Trigger keywords: generate image, generate video, AI painting, text-to-image, text-to-video, image-to-video, marketing image,
  Logo, cover, workflow, video analysis, image analysis, ARTCLAW, ArtClaw.
compatibility:
  dependencies:
    - ARTCLAW REST API (https://artclaw.com/api/v1)
    - Python 3.8+ with requests package
metadata:
  {
    'openclaw':
      {
        'emoji': '🎨',
        'requires': { 'env': ['ARTCLAW_API_KEY'] },
        'primaryEnv': 'ARTCLAW_API_KEY',
      },
  }
---

# ARTCLAW AI Creative Suite

ARTCLAW is an all-in-one AI content creation platform. The CLI tool `scripts/artclaw.py` wraps the complete API interaction (authentication, submission, polling, retry) and outputs standard JSON.

> **⚠️ Mandatory Rule: All generation commands (generate-image / generate-video / generate-marketing-image / run-workflow) must be executed asynchronously. Blocking the main Agent is prohibited.**
>
> | Your Framework                                                             | Execution Method                                                                 |
> | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
> | Has `sessions_spawn` tool (e.g., OpenClaw)                                 | Add `--spawn`, pass the output `sessions_spawn_args` to `sessions_spawn`         |
> | No `sessions_spawn` but has background task capability (e.g., Claude Code) | **Do not** add `--spawn`, use the framework's own background execution mechanism |

---

## 0. Pre-Flight Check (Execute at the start of every conversation)

```bash
python3 scripts/artclaw.py verify-key
```

- Returns `{"status": "valid"}` → proceed normally
- Returns error or Key missing → **stop**, guide user to configure:
  1. Go to https://artclaw.com/settings → API Keys section → click "Create"
  2. Copy the generated Key (prefixed with `vk_`, shown only once)
  3. Configure: `python3 scripts/artclaw.py config-init --api-key "vk_xxx"`

---

## 1. Generate Image

```bash
python3 scripts/artclaw.py generate-image \
    --prompt "Cyberpunk cityscape at night, neon lights reflected in rainwater" \
    --aspect-ratio 16:9 \
    --spawn \
    --deliver-to ou_xxxxxx \
    --deliver-channel feishu
```

With reference image (image-to-image):

```bash
python3 scripts/artclaw.py generate-image \
    --prompt "Landscape painting in the same style" \
    --reference-urls https://example.com/style_ref.jpg \
    --spawn \
    --deliver-to ou_xxxxxx \
    --deliver-channel feishu
```

| Parameter          | Description                             | Values                           |
| ------------------ | --------------------------------------- | -------------------------------- |
| `--prompt`         | Image description (required)            | Text                             |
| `--aspect-ratio`   | Aspect ratio                            | `16:9` `9:16` `1:1` `4:3` `21:9` |
| `--resolution`     | Resolution                              | `1K` `2K` `4K`                   |
| `--reference-urls` | Reference image URLs (multiple allowed) | URL list or base64 data URI |
| `--reference-files` | Reference image files (local paths, auto-converted to base64) | File path list |
| `--model`          | Model override                          | Model ID                         |

## 2. Generate Video

```bash
python3 scripts/artclaw.py generate-video \
    --prompt "Waves crashing on rocks, slow motion" \
    --aspect-ratio 16:9 \
    --duration 5 \
    --resolution 720p \
    --spawn \
    --deliver-to ou_xxxxxx \
    --deliver-channel feishu
```

Image-to-video (I2V):

```bash
python3 scripts/artclaw.py generate-video \
    --prompt "Make the person in the frame turn their head and smile" \
    --reference-urls https://example.com/portrait.jpg \
    --spawn \
    --deliver-to ou_xxxxxx \
    --deliver-channel feishu
```

| Parameter          | Description                  | Values                           |
| ------------------ | ---------------------------- | -------------------------------- |
| `--prompt`         | Video description (required) | Text                             |
| `--aspect-ratio`   | Aspect ratio                 | `16:9` `9:16` `1:1` `4:3` `21:9` |
| `--duration`       | Duration (seconds)           | `2` - `12`                       |
| `--resolution`     | Resolution                   | `480p` `720p` `1080p`            |
| `--reference-urls` | Reference image URLs (I2V)   | URL list or base64 data URI |
| `--reference-files` | Reference image files (I2V, local paths auto-converted) | File path list |
| `--model`          | Model override               | Model ID                         |

## 3. Generate Marketing Image

```bash
python3 scripts/artclaw.py generate-marketing-image \
    --prompt "Summer cool drinks promotional poster" \
    --size 1080x1920 \
    --spawn \
    --deliver-to ou_xxxxxx \
    --deliver-channel feishu
```

## 4. Execute Workflow

```bash
# List available workflows
python3 scripts/artclaw.py list-workflows

# Execute a workflow
python3 scripts/artclaw.py run-workflow \
    --workflow-id "text-to-image-basic" \
    --inputs '{"prompt": "Anime-style forest"}' \
    --spawn \
    --deliver-to ou_xxxxxx \
    --deliver-channel feishu
```

## 5. Multimodal Analysis (Synchronous, no spawn needed)

Analysis commands return results directly without `--spawn`.

```bash
# Image analysis
python3 scripts/artclaw.py analyze-image \
    --reference-urls https://example.com/photo.jpg \
    --query "Describe the main content of this image"

# Video analysis
python3 scripts/artclaw.py analyze-video \
    --reference-urls https://example.com/clip.mp4 \
    --query "Summarize the video content"

# Script extraction
python3 scripts/artclaw.py analyze-script \
    --reference-paths https://example.com/drama.mp4

# Character profiles
python3 scripts/artclaw.py analyze-characters \
    --text "Li Ming is an introverted but brilliant programmer..."
```

---

## 6. Delivery Target (`--deliver-to`)

`--spawn` must be paired with `--deliver-to` and `--deliver-channel` to specify where to deliver the generated results. Background execution mode (Method B) does not need these two parameters.

| Scenario              | `--deliver-channel` | `--deliver-to` Value | Source                                                                        |
| --------------------- | ------------------- | -------------------- | ----------------------------------------------------------------------------- |
| Feishu group chat     | `feishu`            | `oc_xxx` (chat_id)   | `conversation_label` or `chat_id` from inbound metadata, strip `chat:` prefix |
| Feishu direct message | `feishu`            | `ou_xxx` (open_id)   | `sender_id` from inbound metadata, strip `user:` prefix                       |
| Telegram              | `telegram`          | `chat_id`            | inbound message context                                                       |
| Discord               | `discord`           | `channel_id`         | inbound message context                                                       |

**Feishu group chat vs. direct message:** Check `is_group_chat` in inbound metadata. `true` → use `oc_` (chat*id), `false` → use `ou*` (open_id).

### Method A: Spawn Execution Flow (when `sessions_spawn` is available)

1. Main Agent runs `artclaw.py generate-xxx --spawn ...` → output JSON contains `sessions_spawn_args`
2. Main Agent passes `sessions_spawn_args` to the `sessions_spawn` tool → returns immediately
3. **Immediately notify the user**: "Submitted, generating..." (do not wait silently)
4. Sub-Agent executes generation in the background + automatically delivers results to the specified channel

### Method B: Background Execution (without `sessions_spawn`, e.g., Claude Code)

1. Use the framework's background execution capability to run the command (e.g., `Bash(run_in_background: true)`), **without** `--spawn`
2. **Immediately notify the user**: "Submitted, generating..."
3. After the command completes, extract the result URL from the output JSON and display it to the user

### Credential Prerequisites

The delivery scripts for spawn sub-Agents require IM channel credentials (shared automatically on the same machine as the parent Agent):

| Channel    | Credential Source                                             | Configuration                      |
| ---------- | ------------------------------------------------------------- | ---------------------------------- |
| `feishu`   | `~/.openclaw/openclaw.json` → `channels.feishu.accounts.main` | Set `appId` / `appSecret`          |
| `telegram` | Environment variable `TELEGRAM_BOT_TOKEN`                     | `export TELEGRAM_BOT_TOKEN=xxx`    |
| `discord`  | Framework built-in (message tool)                             | No additional configuration needed |

---

## 7. Job Management

```bash
python3 scripts/artclaw.py job-status --job-id "job_xxxxxxxx"    # Query status
python3 scripts/artclaw.py list-jobs --status success --limit 10  # List history
python3 scripts/artclaw.py cancel-job --job-id "job_xxxxxxxx"     # Cancel job
python3 scripts/artclaw.py account-info                           # Check balance
python3 scripts/artclaw.py last-job                               # Latest job
python3 scripts/artclaw.py history --limit 50                     # Local history
```

---

## 8. Quick Commands Reference

| Command                                   | Description                    | User-Facing |
| ----------------------------------------- | ------------------------------ | ----------- |
| `generate-image --spawn`                  | Text-to-image / Image-to-image | Yes         |
| `generate-video --spawn`                  | Text-to-video / Image-to-video | Yes         |
| `generate-marketing-image --spawn`        | Marketing advertisement image  | Yes         |
| `run-workflow --spawn`                    | Execute workflow               | Yes         |
| `list-workflows`                          | List available workflows       | Yes         |
| `analyze-image` / `analyze-video`         | Multimodal analysis            | Yes         |
| `analyze-script` / `analyze-characters`   | Script / Character analysis    | Yes         |
| `job-status` / `list-jobs` / `cancel-job` | Job management                 | Yes         |
| `account-info`                            | Check balance                  | Yes         |
| `last-job` / `history`                    | Local job history              | Yes         |
| `verify-key`                              | Verify API Key                 | Setup only  |
| `config` / `config-init`                  | Configuration management       | Setup only  |

---

## 9. Key Rules

1. **Must be async** — Use `--spawn` if `sessions_spawn` is available, otherwise use framework background execution. Blocking the main Agent is prohibited
2. **Reply to user immediately after submission** — "Submitted, generating...", do not wait silently
3. **Use CLI, not curl** — `artclaw.py` already handles retry, polling, and error handling
4. **Guide users to top up when credits are insufficient** — https://artclaw.com/settings
5. **Deliver results as native messages** — Use native video messages for videos, native image messages for images, do not just send URLs

---

## 10. Error Handling

| Error                        | Cause                                      | Resolution                                          |
| ---------------------------- | ------------------------------------------ | --------------------------------------------------- |
| `401 Unauthorized`           | API Key invalid/missing/revoked            | Guide user to regenerate Key                        |
| `402` / Insufficient credits | Account balance depleted                   | Guide to top up: https://artclaw.com/settings       |
| `404 Job not found`          | job_id does not exist or has expired (24h) | Inform user the job has expired, please regenerate  |
| `404 Workflow not found`     | Workflow does not exist                    | Run `list-workflows` first to confirm available IDs |
| `429 Too Many Requests`      | Rate limit exceeded (120 requests/minute)  | Wait and retry                                      |

---

## 11. Data Storage

All data is stored in `~/.artclaw/`: `config.json` (API Key), `last_job.json` (latest job), `history/` (history records).
