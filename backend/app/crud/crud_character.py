from typing import Dict, Any, List
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.character import Character, CharacterRelationship
from app.schemas.character import CharacterCreate, CharacterUpdate
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


# 创建一个 CRUDCharacter 类的实例，以便在 API 路由中方便地导入和使用
character = CRUDCharacter(Character)