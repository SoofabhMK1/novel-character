from enum import Enum
from typing import List
from fastapi import HTTPException

from app.services import gemini_service, deepseek_service, gcli_service

class AIServiceProvider(str, Enum):
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"
    GCLI = "gcli"

def get_available_providers() -> List[str]: # <-- 修改返回类型提示为 List[str]
    """
    检查所有已知的 AI 服务，并返回一个已成功配置、可供使用的服务商名称列表。
    """
    providers = []
    if gemini_service.is_gemini_configured():
        # =======================================================
        # ==         关键修正：返回枚举的 .value (字符串)        ==
        # =======================================================
        providers.append(AIServiceProvider.GEMINI.value)
    if deepseek_service.is_deepseek_configured():
        # =======================================================
        # ==         关键修正：返回枚举的 .value (字符串)        ==
        # =======================================================
        providers.append(AIServiceProvider.DEEPSEEK.value)
    if gcli_service.is_gcli_configured():
        providers.append(AIServiceProvider.GCLI.value)
    return providers

def generate_character_profile(user_prompt: str, provider: AIServiceProvider) -> dict:
    # (这个函数保持不变，它接收枚举类型是正确的，因为 FastAPI 会自动转换)
    if provider not in get_available_providers():
        raise HTTPException(
            status_code=400, 
            detail=f"AI provider '{provider}' is not available or not configured."
        )
    
    if provider == AIServiceProvider.GEMINI:
        return gemini_service.generate_character_profile(user_prompt)
    elif provider == AIServiceProvider.DEEPSEEK:
        return deepseek_service.generate_character_profile(user_prompt)
    elif provider == AIServiceProvider.GCLI:
        return gcli_service.generate_character_profile(user_prompt)
    
    raise HTTPException(status_code=500, detail="An unknown error occurred in the AI manager.")