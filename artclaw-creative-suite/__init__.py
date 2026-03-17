"""ARTCLAW AI Creative Suite — OpenCode Skill Package

This package provides AI content creation capabilities via the ARTCLAW MCP server,
including image generation, video generation, PPT creation, workflow execution,
multimodal analysis, and prompt enhancement.

MCP Server: http://43.156.26.92:8892/mcp
Auth: API Key (starts with vk_) passed as `api_key` tool argument
Get your key: https://staging.artclaw.ai/#/settings
"""

SKILL_NAME = "artclaw-creative-suite"
SKILL_VERSION = "1.0.0"
MCP_SERVER_URL = "http://43.156.26.92:8892/mcp"
MCP_TRANSPORT = "streamable-http"

MCP_CONFIG = {
    "artclaw": {
        "url": MCP_SERVER_URL,
    }
}

TOOLS = [
    "generate_image",
    "generate_marketing_image",
    "generate_product_carousel",
    "generate_video",
    "generate_ppt_slides",
    "list_workflows",
    "run_workflow",
    "view_image",
    "view_video",
    "analyze_video_script",
    "analyze_character_profiles",
    "get_job_status",
    "get_job_result",
    "list_jobs",
    "cancel_job",
    "generate_logo_prompt",
    "generate_cover_prompt",
    "enhance_marketing_prompt",
    "generate_carousel_prompts",
]


def get_mcp_config() -> dict:
    """Return the MCP server configuration for this skill."""
    return MCP_CONFIG
