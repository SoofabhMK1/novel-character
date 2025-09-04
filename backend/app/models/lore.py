from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    func,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from app.db.base import Base

class LoreEntry(Base):
    """
    世界观设定条目模型，映射到 'lore_entries' 表
    """
    __tablename__ = "lore_entries"

    id = Column(Integer, primary_key=True, index=True)
    
    # 设定的类别 (e.g., "Race", "Alignment")
    category = Column(String(100), nullable=False, index=True)
    
    # 设定的键 (e.g., "HUMAN", "ELF")
    key = Column(String(100), nullable=False, index=True)
    
    # 设定的显示名称 (e.g., "人类")
    name = Column(String(255), nullable=False)
    
    # 详细描述
    description = Column(Text, nullable=True)
    
    # 其他半结构化属性 (e.g., {"traits": ["..."], "image": "..."})
    attributes = Column(JSONB, nullable=True)

    # 自动时间戳
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 创建 category 和 key 的联合唯一约束
    __table_args__ = (
        UniqueConstraint('category', 'key', name='_category_key_uc'),
    )