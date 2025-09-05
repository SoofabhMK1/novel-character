import json
from openai import OpenAI
from fastapi import HTTPException

from app.core.config import settings
from app.core.prompts import (
    get_character_profile_json_schema,
    GENERATE_CHARACTER_PROFILE_TEMPLATE
)

def is_gcli_configured() -> bool:
    """检查 GCLI API Key 是否已配置"""
    return settings.GCLI_API_KEY is not None

def generate_character_profile(user_prompt: str) -> dict:
    """
    使用 GCLI API 根据用户输入生成角色资料。
    """
    if not is_gcli_configured():
        raise HTTPException(status_code=503, detail="GCLI service is not configured.")

    try:
        # 初始化 OpenAI 客户端，并配置为指向 GCLI 的 API
        client = OpenAI(
            api_key=settings.GCLI_API_KEY,
            base_url="https://soofabh.zeabur.app/v1" # <--- 使用你提供的地址
        )
        
        # 复用通用的 Prompt
        json_schema_for_prompt = get_character_profile_json_schema()
        full_prompt = GENERATE_CHARACTER_PROFILE_TEMPLATE.format(
            user_prompt=user_prompt,
            json_schema=json_schema_for_prompt
        )
        
        # 调用 GCLI API
        chat_completion = client.chat.completions.create(
            model="gemini-2.5-flash", # <--- 使用你指定的模型名
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            response_format={"type": "json_object"} 
        )
        
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)

    except Exception as e:
        print(f"An error occurred during GCLI API call: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate character profile from GCLI AI.")