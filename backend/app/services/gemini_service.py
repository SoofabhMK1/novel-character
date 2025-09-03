import json
import google.generativeai as genai
from fastapi import HTTPException
import os
from typing import Optional

from app.core.config import settings
from app.core.prompts import (
    get_character_profile_json_schema,
    GENERATE_CHARACTER_PROFILE_TEMPLATE
)

def is_gemini_configured() -> bool:
    """检查 Gemini API Key 是否已配置"""
    return settings.GOOGLE_API_KEY is not None

def initialize_gemini():
    """在应用启动时初始化 Gemini SDK"""
    if is_gemini_configured():
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            print("Gemini SDK configured successfully.")
        except Exception as e:
            print(f"Error configuring Gemini SDK: {e}")

def generate_character_profile(user_prompt: str, proxy_url: Optional[str] = None) -> dict:
    """
    根据用户输入生成角色资料，通过动态设置环境变量来支持可选的代理。
    如果proxy_url为None，则不使用代理。
    """
    if not is_gemini_configured():
        raise HTTPException(status_code=503, detail="AI service is not configured.")

    # 保存原始的代理设置，以便后续恢复
    original_http_proxy = os.environ.get('HTTP_PROXY')
    original_https_proxy = os.environ.get('HTTPS_PROXY')

    try:
        # 动态构建 Prompt (保持不变)
        json_schema_for_prompt = get_character_profile_json_schema()
        full_prompt = GENERATE_CHARACTER_PROFILE_TEMPLATE.format(
            user_prompt=user_prompt,
            json_schema=json_schema_for_prompt
        )

        # =======================================================
        # ==         核心修改：动态设置环境变量              ==
        # =======================================================
        # 如果提供了代理URL，则使用它；否则清除环境变量中的代理设置
        if proxy_url:
            print(f"Setting environment proxy for this request: {proxy_url}")
            # 为当前进程设置代理环境变量
            os.environ['HTTP_PROXY'] = proxy_url
            os.environ['HTTPS_PROXY'] = proxy_url
        else:
            # 如果不使用代理，确保清除环境变量中的代理设置
            if 'HTTP_PROXY' in os.environ:
                del os.environ['HTTP_PROXY']
            if 'HTTPS_PROXY' in os.environ:
                del os.environ['HTTPS_PROXY']
            print("No proxy will be used for this request.")
        
        # 重新运行initialize_gemini以使客户端获取新配置
        initialize_gemini()
        
        # 设置生成配置
        generation_config = {"response_mime_type": "application/json"}
        
        # 创建一个全新的模型实例，它会读取当前的环境变量
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=generation_config
        )

        # 调用 API
        response = model.generate_content(full_prompt)
        
        return json.loads(response.text)

    except Exception as e:
        print(f"An error occurred during Gemini API call: {e}")
        if "proxy" in str(e).lower() or "connect" in str(e).lower():
            raise HTTPException(status_code=400, detail=f"Failed to connect via proxy: {proxy_url}")
        raise HTTPException(status_code=500, detail="Failed to generate character profile from AI.")
    
    finally:
        # =======================================================
        # ==      关键：在函数结束前，恢复原始环境变量        ==
        # =======================================================
        # 无论成功还是失败，都确保恢复环境，防止污染后续请求
        print("Restoring original proxy settings.")
        if original_http_proxy:
            os.environ['HTTP_PROXY'] = original_http_proxy
        elif 'HTTP_PROXY' in os.environ:
            del os.environ['HTTP_PROXY']
            
        if original_https_proxy:
            os.environ['HTTPS_PROXY'] = original_https_proxy
        elif 'HTTPS_PROXY' in os.environ:
            del os.environ['HTTPS_PROXY']