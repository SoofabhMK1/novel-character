from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.lore import LoreEntry
from app.schemas.lore import LoreEntryCreate, LoreEntryUpdate

class CRUDLoreEntry(CRUDBase[LoreEntry, LoreEntryCreate, LoreEntryUpdate]):
    
    def get_by_category(
        self, db: Session, *, category: str
    ) -> List[LoreEntry]:
        """
        通过类别获取该类别的所有设定条目。
        """
        return db.query(self.model).filter(self.model.category == category).all()

# 创建一个 CRUDLoreEntry 类的实例，以便在 API 路由中方便地导入和使用
lore_entry = CRUDLoreEntry(LoreEntry)