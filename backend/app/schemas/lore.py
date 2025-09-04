from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class LoreEntryBase(BaseModel):
    """设定条目的基础模型"""
    category: str
    key: str
    name: str
    description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = {}


class LoreEntryCreate(LoreEntryBase):
    """用于从 API 创建一个新的设定条目的 Schema"""
    pass


class LoreEntryUpdate(BaseModel):
    """用于从 API 更新一个设定条目的 Schema (所有字段可选)"""
    category: Optional[str] = None
    key: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None


class LoreEntry(LoreEntryBase):
    """用于从 API 读取（返回）一个设定条目的 Schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)