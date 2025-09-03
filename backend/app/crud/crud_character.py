from typing import Dict, Any, List, Optional 
from sqlalchemy import func, desc, or_
from sqlalchemy.orm import Session, joinedload
import uuid 

from app.crud.base import CRUDBase
from app.models.character import Character, CharacterRelationship
from app.schemas.character import CharacterCreate, CharacterUpdate, RelationshipCreate
from app.core.enums import Status, Alignment


class CRUDCharacter(CRUDBase[Character, CharacterCreate, CharacterUpdate]):
    
    def get_dashboard_stats(self, db: Session) -> Dict[str, Any]:
        """
        获取仪表盘所需的统计数据。
        """
        total_characters = db.query(func.count(self.model.id)).scalar()
        
        alive_characters = db.query(func.count(self.model.id)).filter(
            self.model.status == Status.ALIVE
        ).scalar()
        
        # 统计所有包含 'Good' 的阵营
        good_alignment_count = db.query(func.count(self.model.id)).filter(
            self.model.alignment.in_([
                Alignment.LAWFUL_GOOD, 
                Alignment.NEUTRAL_GOOD, 
                Alignment.CHAOTIC_GOOD
            ])
        ).scalar()
        
        total_relationships = db.query(func.count(CharacterRelationship.id)).scalar()

        return {
            "total_characters": total_characters,
            "alive_characters": alive_characters,
            "good_alignment_count": good_alignment_count,
            "total_relationships": total_relationships,
        }

    def get_multi_sorted(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100, 
        sort_by: str = "updated_at",
        order: str = "desc"
    ) -> List[Character]:
        """
        获取支持排序的角色列表。
        """
        query = db.query(self.model)
        
        # 检查 sort_by 字段是否存在于模型中，防止 SQL 注入
        if hasattr(self.model, sort_by):
            sort_column = getattr(self.model, sort_by)
            if order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
        
        return query.offset(skip).limit(limit).all()

# =======================================================
# ==              新增的关系管理方法                   ==
# =======================================================

    def add_relationship(
        self, db: Session, *, character_from_id: uuid.UUID, obj_in: RelationshipCreate
    ) -> CharacterRelationship:
        """
        为一个角色添加一个新的关系。
        """
        # 创建一个新的 CharacterRelationship ORM 对象
        db_relationship = CharacterRelationship(
            character_from_id=character_from_id,
            character_to_id=obj_in.character_to_id,
            relationship_type=obj_in.relationship_type,
            description=obj_in.description,
        )
        db.add(db_relationship)
        db.commit()
        db.refresh(db_relationship)
        return db_relationship

    def get_relationships_for_character(
        self, db: Session, *, character_id: uuid.UUID
    ) -> List[CharacterRelationship]:
        """
        获取一个特定角色的所有关系 (包括作为发起方和接收方)。
        """
        query = db.query(CharacterRelationship).options(
            # 使用 joinedload (预加载) 来高效地获取关联的角色信息
            # 这会通过一个 JOIN 查询，一次性把关系和两端的角色名都查出来
            joinedload(CharacterRelationship.character_from),
            joinedload(CharacterRelationship.character_to)
        ).filter(
            # 查询条件：当前角色ID是发起方 OR 是接收方
            or_(
                CharacterRelationship.character_from_id == character_id,
                CharacterRelationship.character_to_id == character_id,
            )
        )
        return query.all()

    def delete_relationship(self, db: Session, *, relationship_id: int) -> Optional[CharacterRelationship]:
        """
        通过 ID 删除一个关系。
        """
        # CharacterRelationship 的主键是 id (Integer)，不是 UUID
        relationship = db.query(CharacterRelationship).get(relationship_id)
        if relationship:
            db.delete(relationship)
            db.commit()
        return relationship

# 创建一个 CRUDCharacter 类的实例，以便在 API 路由中方便地导入和使用
character = CRUDCharacter(Character)