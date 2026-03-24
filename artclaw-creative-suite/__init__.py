"""ARTCLAW AI Creative Suite — OpenCode Skill Package

This package provides AI content creation capabilities via the ARTCLAW REST API,
including image generation, video generation, workflow execution,
multimodal analysis, and prompt enhancement.

REST API Base: http://artclaw.com/api/v1
Auth: API Key (starts with vk_) passed as `X-API-KEY` HTTP header
Get your key: https://artclaw.com/#/settings
"""

SKILL_NAME = "artclaw-creative-suite"
SKILL_VERSION = "2.0.0"
API_BASE_URL = "http://artclaw.com/api/v1"

API_CONFIG = {
    "base_url": API_BASE_URL,
    "auth_header": "X-API-KEY",
}

ENDPOINTS = {
    # 生成类（异步，返回 job_id）
    "generate_image": ("POST", "/generate/image"),
    "generate_video": ("POST", "/generate/video"),
    "generate_marketing_image": ("POST", "/generate/marketing-image"),
    # 工作流
    "list_workflows": ("GET", "/workflows"),
    "run_workflow": ("POST", "/workflows/{workflow_id}/run"),
    # 分析类（同步返回）
    "analyze_image": ("POST", "/analyze/image"),
    "analyze_video": ("POST", "/analyze/video"),
    "analyze_script": ("POST", "/analyze/script"),
    "analyze_characters": ("POST", "/analyze/characters"),
    # 任务管理
    "get_job": ("GET", "/jobs/{job_id}"),
    "list_jobs": ("GET", "/jobs"),
    "cancel_job": ("POST", "/jobs/{job_id}/cancel"),
    # 账户
    "account_info": ("GET", "/account/info"),
    # 鉴权
    "verify_key": ("POST", "/auth/verify"),
    # Prompt 工具（免费，无需 Key）
    "prompt_logo": ("POST", "/prompts/logo"),
    "prompt_cover": ("POST", "/prompts/cover"),
    "prompt_marketing": ("POST", "/prompts/marketing"),
}


def get_api_config() -> dict:
    """Return the REST API configuration for this skill."""
    return API_CONFIG
