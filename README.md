# 🎨 ARTCLAW AI Creative Suite — OpenClaw Skill

一站式 AI 内容创作 Skill，接入 [ARTCLAW](https://artclaw.com) 平台全套创作能力，支持 AI 生图、生视频、PPT 生成、多模态分析与工作流编排。

---
 
## ✨ 功能一览

| 能力 | 描述 |
|------|------|
| 🖼️ AI 生图 | 文生图、图生图、营销广告图、产品套图 |
| 🎬 AI 生视频 | 文生视频、图生视频 |
| 🔍 多模态分析 | 图片理解、视频分析、剧本分析、人物小传提炼 |
| ⚡ 工作流 | 一键执行预设流程（动画 / 漫画 / 电商详情页等） |
| ✏️ Prompt 工具 | Logo / 封面 / 营销图 / 轮播图提示词优化（免费，无需 Key） |

---

## 📦 在 OpenClaw 上安装

直接跟OpenClaw说：安装skill: https://github.com/ArtClaw1/skills.git

---

## 🔑 配置 API Key

本 Skill 的生成类功能需要 ARTCLAW API Key 进行鉴权。

1. 访问 ARTCLAW 官网设置页：**https://artclaw.com/#/settings**
2. 在 **API Keys** 区域点击「创建」，输入名称后复制生成的 Key（以 `vk_` 开头）
3. 在 OpenClaw Skill 配置页中，将 Key 填入环境变量：

   ```
   ARTCLAW_API_KEY=vk_your_key_here
   ```

> **注意：** Prompt 工具类功能无需 API Key，可免费直接使用。

---

## 🚀 快速上手

安装并配置完成后，在 OpenClaw 对话框中直接描述你的创作需求即可：

```
帮我画一张赛博朋克风格的猫咪
```

```
用这张产品图生成一组电商轮播图
```

---

## 📋 版本信息

- **版本：** 1.1.0
- **作者：** ARTCLAW Team
- **许可证：** MIT
