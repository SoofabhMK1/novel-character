import json
from openai import OpenAI # 导入 OpenAI 库
from fastapi import HTTPException

from app.core.config import settings
from app.core.prompts import (
    get_character_profile_json_schema,
    GENERATE_CHARACTER_PROFILE_TEMPLATE
)

def is_deepseek_configured() -> bool:
    """检查 DeepSeek API Key 是否已配置"""
    return settings.DEEPSEEK_API_KEY is not None

def generate_character_profile(user_prompt: str) -> dict:
    """
    使用 DeepSeek API 根据用户输入生成角色资料。
    """
    if not is_deepseek_configured():
        raise HTTPException(status_code=503, detail="DeepSeek service is not configured.")

    try:
        # 初始化 OpenAI 客户端，并配置为指向 DeepSeek 的 API
        client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"
        )
        
        # 动态构建 Prompt (与 Gemini 服务共用)
        json_schema_for_prompt = get_character_profile_json_schema()
        full_prompt = GENERATE_CHARACTER_PROFILE_TEMPLATE.format(
            user_prompt=user_prompt,
            json_schema=json_schema_for_prompt
        )
        
        # 调用 DeepSeek API
        chat_completion = client.chat.completions.create(
            model="deepseek-chat", # DeepSeek 的 chat 模型
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            # 启用 JSON 模式
            response_format={"type": "json_object"} 
        )
        
        # 提取、解析并返回 JSON 响应
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)

    except Exception as e:
        print(f"An error occurred during DeepSeek API call: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate character profile from DeepSeek AI.")