from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services import gemini_service
from app.schemas.ai import AIGenerationRequest
from app.schemas.character import CharacterCreate
from app.services.ai_manager import AIServiceProvider
from app.services import ai_manager

router = APIRouter()

class AIGenerationRequest(BaseModel):
    prompt: str
    # 新增 provider 字段，并使用我们的枚举作为类型
    provider: AIServiceProvider
    
    # 代理功能我们暂时搁置，但在 Schema 中保留以便未来使用
    use_proxy: bool = False
    proxy_url: Optional[str] = None

@router.post("/generate-character", response_model=CharacterCreate)
def generate_character_from_ai(
    request_data: AIGenerationRequest
):
    """
    使用 AI 根据用户 prompt 生成角色特征。
    将请求调度到用户指定的 AI 服务商。
    """
    try:
        # =======================================================
        # ==         调用 ai_manager 的统一入口            ==
        # =======================================================
        generated_data = ai_manager.generate_character_profile(
            user_prompt=request_data.prompt,
            provider=request_data.provider # 将用户选择的 provider 传递下去
        )
        return generated_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"AI returned invalid data structure: {e}")