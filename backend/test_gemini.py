# =======================================================
# ==              在这里添加诊断用的 print             ==
# =======================================================
print("Script execution started...")

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import sys

print("All imports were successful.")

# ------------------------------------------------------------------
# 1. 模拟我们的配置加载 (增强版，支持代理)
# ------------------------------------------------------------------
def load_config():
    """从 .env 文件加载环境变量，并检查系统代理设置"""
    # 我们假设 .env 文件在上一级目录
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=dotenv_path)
    
    # 加载 API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file.")
        
    # =======================================================
    # ==           新增：检查并设置代理服务器            ==
    # =======================================================
    # Python 的 HTTP 库通常会读取 'HTTP_PROXY' 和 'HTTPS_PROXY' 环境变量
    # 我们可以从 .env 文件中读取这些，或者让用户在系统中设置
    http_proxy = os.getenv("HTTP_PROXY")
    https_proxy = os.getenv("HTTPS_PROXY")
    
    # 如果找到了代理设置，就将其应用到当前 Python 进程的环境中
    # 这样 google-generativeai SDK 内部的 HTTP 请求就会自动使用它
    if http_proxy:
        os.environ['HTTP_PROXY'] = http_proxy
        print(f"Using HTTP Proxy: {http_proxy}")
    if https_proxy:
        os.environ['HTTPS_PROXY'] = https_proxy
        print(f"Using HTTPS Proxy: {https_proxy}")
        
    # 在 Windows 上，Python 可能无法直接读取系统代理设置。
    # 一个更可靠的方法是尝试从 Windows 注册表中读取
    if sys.platform == "win32":
        try:
            import winreg
            # 打开代理设置的注册表项
            internet_settings = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                               r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
            # 读取代理是否启用
            proxy_enable = winreg.QueryValueEx(internet_settings, 'ProxyEnable')[0]
            if proxy_enable:
                # 如果启用，读取代理服务器地址
                proxy_server = winreg.QueryValueEx(internet_settings, 'ProxyServer')[0]
                # 为 HTTP 和 HTTPS 设置相同的代理
                os.environ['HTTP_PROXY'] = f'http://{proxy_server}'
                os.environ['HTTPS_PROXY'] = f'http://{proxy_server}'
                print(f"Detected and using Windows system proxy: http://{proxy_server}")
            winreg.CloseKey(internet_settings)
        except (ImportError, FileNotFoundError, OSError):
             # 如果 winreg 失败或找不到键，就静默地忽略
            pass
            
    return api_key

# ------------------------------------------------------------------
# 2. 模拟我们的 Pydantic Schema
#    我们直接用一个多行字符串来表示它的 JSON 结构
# ------------------------------------------------------------------
# 这个结构是从 CharacterCreate.schema_json() 中复制过来的简化版
# 它告诉 AI 我们需要哪些字段和大致类型
CHARACTER_SCHEMA_JSON = """
{
    "name": "string (Required, Full name of the character, in English)",
    "nickname": "string (Optional, An alias or common name, in Chinese)",
    "age": "integer (Optional, The character's age in years. Example: 28)",
    "gender": "string (Required, Must be one of: 'Male', 'Female', 'Non-binary', 'Other')",
    "race": "string (Required, Must be one of: 'Human', 'Elf', 'Dwarf', 'Orc', 'Goblin', 'Dragon', 'Android', 'Other')",
    "occupation": "string (Required, Character's job or role. Must be in CHINESE. Example: '星际猎人')",
    "height_cm": "integer (Required, Height in centimeters. Only provide the number, WITHOUT units. Example: 175)",
    "build": "string (Required, Must be one of: 'Slim', 'Athletic', 'Average', 'Muscular', 'Heavyset')",
    "status": "string (Required, Must be one of: 'Alive', 'Deceased', 'Missing in Action', 'Unknown')",
    "alignment": "string (Required, Must be one of: 'Lawful Good', 'Neutral Good', 'Chaotic Good', 'Lawful Neutral', 'True Neutral', 'Chaotic Neutral', 'Lawful Evil', 'Neutral Evil', 'Chaotic Evil')",
    "image_filename": "null (This field MUST be null. Do not generate any value for it.)",
    "measurements": {
        "bust_cm": "integer (Optional, Number only)",
        "waist_cm": "integer (Optional, Number only)",
        "hip_cm": "integer (Optional, Number only)"
    },
    "personality_details": {
        "core_traits": ["string", "... (An array of 5-7 key personality adjectives. Must be in CHINESE. Example: ['聪慧', '果断'])"],
        "mbti": "string (Optional, e.g., 'INTJ', 'ENFP')",
        "strengths": "string (A brief description of positive traits. Must be in CHINESE.)",
        "weaknesses": "string (A brief description of flaws. Must be in CHINESE.)"
    },
    "appearance_details": {
        "hair": "string (Description of hair color and style. Must be in CHINESE.)",
        "eyes": "string (Description of eye color and shape. Must be in CHINESE.)",
        "skin_tone": "string (Description of skin tone. Must be in CHINESE.)",
        "distinguishing_features": "string (Scars, tattoos, etc. Must be in CHINESE.)"
    },
    "background_details": {
        "hometown": "string (Optional, Where they grew up. Must be in CHINESE.)",
        "family": "string (Brief description of family. Must be in CHINESE.)",
        "education": "string (Level and type of education. Must be in CHINESE.)",
        "key_life_events": "string (Significant events that shaped them. Must be in CHINESE.)"
    },
    "speech_patterns": {
        "voice": "string (Description of their voice. Must be in CHINESE. Example: '低沉且富有磁性')",
        "common_phrases": ["string", "... (An array of catchphrases. Must be in CHINESE.)"]
    }
}
"""

# ------------------------------------------------------------------
# 3. 模拟我们的 Prompt 模板
# ------------------------------------------------------------------
GENERATE_CHARACTER_PROFILE_TEMPLATE = """
你是一位经验丰富的小说家和角色设计师。
请根据用户的简短描述：“{user_prompt}”，为一个角色生成详细的个人资料。
你的输出必须是一个严格的、不包含任何注释或 markdown 格式的 JSON 对象。
JSON 对象的结构必须严格遵循以下定义：

{json_schema}
"""

# ------------------------------------------------------------------
# 4. 核心的测试函数
# ------------------------------------------------------------------
def test_generate_character(user_prompt: str):
    """
    在一个隔离的环境中测试 Gemini 的角色生成功能。
    """
    print("--- Starting Gemini Character Generation Test ---")
    
    try:
        # 加载配置
        api_key = load_config()
        print("API Key loaded successfully.")
        
        # 配置 Gemini SDK
        genai.configure(api_key=api_key)
        print("Gemini SDK configured.")
        
        # 构建 Prompt
        full_prompt = GENERATE_CHARACTER_PROFILE_TEMPLATE.format(
            user_prompt=user_prompt,
            json_schema=CHARACTER_SCHEMA_JSON
        )
        print("\n--- Sending Prompt to Gemini ---")
        # print(full_prompt) # 取消注释以查看完整的 prompt
        
        # 创建模型并设置生成配置（启用 JSON 模式）
        generation_config = {
          "response_mime_type": "application/json",
        }
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=generation_config
        )
        
        print("\n--- Waiting for Gemini response... ---")
        response = model.generate_content(full_prompt)
        
        print("\n--- Gemini Response Received ---")
        
        # 解析并打印结果
        response_text = response.text
        print("Raw response text:\n", response_text)
        
        parsed_json = json.loads(response_text)
        print("\n--- Parsed JSON Object ---")
        print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
        
        print("\n--- Test Finished Successfully! ---")
        return parsed_json

    except Exception as e:
        print(f"\n--- An error occurred ---")
        print(e)
        return None

# ------------------------------------------------------------------
# 5. 执行测试
# ------------------------------------------------------------------
if __name__ == "__main__":
    # 在这里输入你的简单描述
    test_prompt = "一个厌倦了战争、隐居在深林中的年迈精灵德鲁伊"
    generated_profile = test_generate_character(test_prompt)