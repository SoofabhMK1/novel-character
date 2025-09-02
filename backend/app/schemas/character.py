import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import computed_field
from pydantic import BaseModel, ConfigDict

from app.core.enums import (Alignment, BuildType, Gender, Race, RelationshipType,
                            Status)

# ===================================================================
# Schemas for Nested JSONB Fields
# ===================================================================
# 为 JSONB 字段创建独立的 Schema 可以提供更强的类型检查和编辑器自动补全功能

class MeasurementsSchema(BaseModel):
    bust_cm: Optional[int] = None
    waist_cm: Optional[int] = None
    hip_cm: Optional[int] = None

class PersonalitySchema(BaseModel):
    core_traits: List[str] = []
    mbti: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    likes: Optional[str] = None
    dislikes: Optional[str] = None

# ===================================================================
# Schemas for Character Relationships
# ===================================================================

class CharacterRelationshipBase(BaseModel):
    """关系模型的基础，包含创建时需要的数据"""
    character_to_id: uuid.UUID
    relationship_type: RelationshipType
    description: Optional[str] = None


class CharacterRelationshipCreate(CharacterRelationshipBase):
    """用于从 API 创建关系的 Schema"""
    pass


class CharacterRelationship(CharacterRelationshipBase):
    """用于从 API 读取（返回）关系的 Schema"""
    id: int
    character_from_id: uuid.UUID

    # Pydantic V2 的配置，允许模型从 ORM 对象属性中读取数据
    model_config = ConfigDict(from_attributes=True)


# ===================================================================
# Schemas for Characters
# ===================================================================

class CharacterBase(BaseModel):
    """角色的基础模型，包含所有模型共有的字段"""
    name: str
    nickname: Optional[str] = None
    age: Optional[int] = None
    occupation: Optional[str] = None
    height_cm: Optional[int] = None
    image_filename: Optional[str] = None
    gender: Gender = Gender.OTHER
    build: BuildType = BuildType.AVERAGE
    race: Race = Race.OTHER
    alignment: Alignment = Alignment.TRUE_NEUTRAL
    status: Status = Status.UNKNOWN
    
    # 使用嵌套的 Schema 来定义 JSONB 字段的结构
    measurements: MeasurementsSchema = MeasurementsSchema()
    personality_details: PersonalitySchema = PersonalitySchema()
    
    # 对于结构更自由的 JSONB 字段，可以使用字典类型
    appearance_details: Dict[str, Any] = {}
    background_details: Dict[str, Any] = {}
    speech_patterns: Dict[str, Any] = {}


class CharacterCreate(CharacterBase):
    """用于从 API 创建一个新角色的 Schema"""
    # 目前，创建角色所需的所有字段都在 CharacterBase 中
    pass


class CharacterUpdate(BaseModel):
    """用于从 API 更新一个已存在角色的 Schema"""
    # 所有字段都是可选的，因为用户可能只想更新其中一两个字段
    name: Optional[str] = None
    nickname: Optional[str] = None
    age: Optional[int] = None
    occupation: Optional[str] = None
    height_cm: Optional[int] = None
    image_filename: Optional[str] = None
    gender: Optional[Gender] = None
    build: Optional[BuildType] = None
    race: Optional[Race] = None
    alignment: Optional[Alignment] = None
    status: Optional[Status] = None
    measurements: Optional[MeasurementsSchema] = None
    personality_details: Optional[PersonalitySchema] = None
    appearance_details: Optional[Dict[str, Any]] = None
    background_details: Optional[Dict[str, Any]] = None
    speech_patterns: Optional[Dict[str, Any]] = None


class Character(CharacterBase):
    """用于从 API 读取（返回）一个角色的 Schema"""
    # 包含了数据库会自动生成的字段
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    # --- 新增：动态计算图片 URL ---
    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        """
        根据 image_filename 动态生成完整的图片 URL。
        """
        if self.image_filename:
            # 这里的路径前缀 /media/character_images/ 必须与 Nginx 配置 和 卷挂载路径 对应
            return f"/media/character_images/{self.image_filename}"
        return None

    model_config = ConfigDict(from_attributes=True)

class DashboardStats(BaseModel):
    """用于返回仪表盘统计数据的 Schema"""
    total_characters: int
    alive_characters: int
    good_alignment_count: int
    total_relationships: int