import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Enum as SQLAlchemyEnum,
    TIMESTAMP,
    func
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import declarative_base, relationship

from app.core.enums import (
    Gender,
    BuildType,
    RelationshipType,
    Race,
    Alignment,
    Status,
    Bloodline,
)
from app.db.base import Base
# Base = declarative_base()

class Character(Base):
    """
    角色模型，映射到 'characters' 表
    """
    __tablename__ = "characters"

    # --- 固定特征列 ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    nickname = Column(String(255))
    age = Column(Integer)
    occupation = Column(String(255))
    height_cm = Column(Integer)
    image_filename = Column(String(255))

    # --- 枚举类型列 ---
    gender = Column(SQLAlchemyEnum(Gender), default=Gender.OTHER)
    build = Column(SQLAlchemyEnum(BuildType), default=BuildType.AVERAGE)
    race = Column(SQLAlchemyEnum(Race), default=Race.OTHER)
    alignment = Column(SQLAlchemyEnum(Alignment), default=Alignment.TRUE_NEUTRAL)
    status = Column(SQLAlchemyEnum(Status), default=Status.UNKNOWN)
    bloodline = Column(SQLAlchemyEnum(Bloodline), default=Bloodline.UNKNOWN)

    # --- JSONB 灵活特征列 ---
    measurements = Column(JSONB)        # 存储三围等
    appearance_details = Column(JSONB)  # 存储外貌描述
    personality_details = Column(JSONB) # 存储个性特征
    background_details = Column(JSONB)  # 存储背景故事
    speech_patterns = Column(JSONB)     # 存储语言习惯

    # --- 自动时间戳 ---
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # --- 关系定义 ---
    # 'relationships_from' 表示此角色作为关系发起方的所有关系
    relationships_from = relationship(
        "CharacterRelationship",
        foreign_keys="[CharacterRelationship.character_from_id]",
        back_populates="character_from"
    )
    # 'relationships_to' 表示此角色作为关系接收方的所有关系
    relationships_to = relationship(
        "CharacterRelationship",
        foreign_keys="[CharacterRelationship.character_to_id]",
        back_populates="character_to"
    )

class CharacterRelationship(Base):
    """
    角色关系模型，映射到 'character_relationships' 表
    """
    __tablename__ = "character_relationships"

    id = Column(Integer, primary_key=True, index=True)
    character_from_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    character_to_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    relationship_type = Column(SQLAlchemyEnum(RelationshipType), nullable=False)
    description = Column(Text)

    # --- 关系定义 ---
    character_from = relationship("Character", foreign_keys=[character_from_id], back_populates="relationships_from")
    character_to = relationship("Character", foreign_keys=[character_to_id], back_populates="relationships_to")