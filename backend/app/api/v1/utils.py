from fastapi import APIRouter
from app.core import enums
from app.core.config import settings
from app.services import ai_manager

router = APIRouter()

@router.get("/enums", response_model=dict)
def get_all_enums():
    """
    获取应用中定义的所有枚举类型及其值。
    前端可以用这个接口来动态生成表单选项。
    """
    all_enums = {}
    # 遍历 enums 模块中的所有成员
    for name, member in enums.__dict__.items():
        # 确保成员是一个枚举类并且不是基类 Enum
        if isinstance(member, type) and issubclass(member, enums.enum.Enum) and member is not enums.enum.Enum:
            # 将枚举名和其所有成员的值组织成字典
            all_enums[name] = [item.value for item in member]
            
    return all_enums

@router.get("/features", response_model=dict)
def get_feature_flags():
    """
    返回一个功能开关列表，告诉前端哪些可选功能是可用的。
    """
    return {
        # 调用 ai_manager 获取当前所有已配置的 AI 服务商列表
        "available_ai_providers": ai_manager.get_available_providers()
    }