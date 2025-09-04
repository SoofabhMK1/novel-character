# app/core/prompts.py
from app.core import enums

def get_character_profile_json_schema() -> str:
    """
    动态地、程序化地生成用于 Prompt 的 JSON Schema 描述字符串。
    """
    # 使用 f-string 和 .join() 来动态地从 enums 模块构建可选项列表
    gender_options = ", ".join([f"'{e.value}'" for e in enums.Gender])
    race_options = ", ".join([f"'{e.value}'" for e in enums.Race])
    build_options = ", ".join([f"'{e.value}'" for e in enums.BuildType])
    status_options = ", ".join([f"'{e.value}'" for e in enums.Status])
    alignment_options = ", ".join([f"'{e.value}'" for e in enums.Alignment])
    bloodline_options = ", ".join([f"'{e.value}'" for e in enums.Bloodline])

    # 使用一个多行 f-string 来构建最终的 schema 字符串
    schema = f"""
{{
    "name": "string (Required, Full name of the character, Must be in CHINESE)",
    "nickname": "string (Optional, An alias or common name, Must be in CHINESE)",
    "age": "integer (Optional, The character's age in years. Example: 28)",
    "gender": "string (Required, Must be one of: {gender_options})",
    "race": "string (Required, Must be one of: {race_options})",
    "occupation": "string (Required, Character's job or role. Must be in CHINESE. Example: '星际猎人')",
    "height_cm": "integer (Required, Height in centimeters. Only provide the number, WITHOUT units. Example: 175)",
    "build": "string (Required, Must be one of: {build_options})",
    "status": "string (Required, Must be one of: {status_options})",
    "bloodline": "string (Required, Must be one of: {bloodline_options})",
    "alignment": "string (Required, Must be one of: {alignment_options})",
    "image_filename": "null (This field MUST be null. Do not generate any value for it.)",
    "measurements": {{
        "bust_cm": "integer (Optional, Number only)",
        "waist_cm": "integer (Optional, Number only)",
        "hip_cm": "integer (Optional, Number only)"
    }},
    "personality_details": {{
        "core_traits": ["string", "... (An array of 5-7 key personality adjectives. Must be in CHINESE. Example: ['聪慧', '果断'])"],
        "mbti": "string (Optional, e.g., 'INTJ', 'ENFP')",
        "strengths": "string (A brief description of positive traits. Must be in CHINESE.)",
        "weaknesses": "string (A brief description of flaws. Must be in CHINESE.)"
    }},
    "appearance_details": {{
        "hair": "string (Description of hair color and style. Must be in CHINESE.)",
        "eyes": "string (Description of eye color and shape. Must be in CHINESE.)",
        "skin_tone": "string (Description of skin tone. Must be in CHINESE.)",
        "distinguishing_features": "string (Scars, tattoos, etc. Must be in CHINESE.)"
    }},
    "background_details": {{
        "hometown": "string (Optional, Where they grew up. Must be in CHINESE.)",
        "family": "string (Brief description of family. Must be in CHINESE.)",
        "education": "string (Level and type of education. Must be in CHINESE.)",
        "key_life_events": "string (Significant events that shaped them. Must be in CHINESE.)"
    }},
    "speech_patterns": {{
        "voice": "string (Description of their voice. Must be in CHINESE. Example: '低沉且富有磁性')",
        "common_phrases": ["string", "... (An array of catchphrases. Must be in CHINESE.)"]
    }}
}}
"""
    return schema.strip()


# 这个主模板保持不变
GENERATE_CHARACTER_PROFILE_TEMPLATE = """
你是一位经验丰富的小说家和角色设计师。
请根据用户的简短描述：“{user_prompt}”，为一个角色生成详细的个人资料。
你的输出必须是一个严格的、不包含任何注释或 markdown 格式的 JSON 对象。
JSON 对象的结构和值必须严格遵循以下定义：

{json_schema}
"""