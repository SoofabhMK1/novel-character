from fastapi import APIRouter, HTTPException
from app.services import gemini_service
from app.schemas.ai import AIGenerationRequest
from app.schemas.character import CharacterCreate

router = APIRouter()

@router.post("/generate-character", response_model=CharacterCreate)
def generate_character_from_ai(
    request_data: AIGenerationRequest
):
    """
    使用 AI 根据用户 prompt 生成角色特征。
    支持可选的代理。
    """
    proxy_to_use = None
    if request_data.use_proxy:
        if not request_data.proxy_url:
            raise HTTPException(status_code=400, detail="Proxy is enabled but no proxy URL was provided.")
        proxy_to_use = request_data.proxy_url
    
    try:
        # =======================================================
        # ==         关键修正：使用正确的关键字参数          ==
        # =======================================================
        generated_data = gemini_service.generate_character_profile(
            user_prompt=request_data.prompt, # <-- 从 'prompt' 改为 'user_prompt'
            proxy_url=proxy_to_use           # <-- 确保 proxy_url 被传递
        )
        
        # Pydantic 会自动验证 Gemini 返回的数据是否符合 CharacterCreate 的结构
        return generated_data
        
    except HTTPException as e:
        # 重新抛出由 service 层或我们自己抛出的 HTTP 异常
        raise e
    except Exception as e:
        # 捕获其他意外错误，例如 Pydantic 验证失败
        raise HTTPException(status_code=400, detail=f"AI returned invalid data structure: {e}")