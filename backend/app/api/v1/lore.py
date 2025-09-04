from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.crud_lore import lore_entry
from app.schemas.lore import LoreEntry, LoreEntryCreate, LoreEntryUpdate

router = APIRouter()

@router.post("/", response_model=LoreEntry, status_code=status.HTTP_201_CREATED)
def create_lore_entry(
    *,
    db: Session = Depends(get_db),
    lore_in: LoreEntryCreate
):
    """
    创建一个新的设定条目。
    """
    new_lore_entry = lore_entry.create(db=db, obj_in=lore_in)
    return new_lore_entry


@router.get("/", response_model=List[LoreEntry])
def read_lore_entries(
    db: Session = Depends(get_db),
    category: str = None # 设为可选的查询参数
):
    """
    获取设定条目列表。
    可以通过 'category' 查询参数来筛选特定类别的条目。
    """
    if category:
        entries = lore_entry.get_by_category(db=db, category=category)
    else:
        entries = lore_entry.get_multi(db=db)
    return entries


@router.get("/{lore_id}", response_model=LoreEntry)
def read_lore_entry(
    *,
    db: Session = Depends(get_db),
    lore_id: int
):
    """
    通过 ID 获取单个设定条目。
    """
    db_lore_entry = lore_entry.get(db=db, id=lore_id)
    if not db_lore_entry:
        raise HTTPException(status_code=404, detail="Lore entry not found")
    return db_lore_entry


@router.put("/{lore_id}", response_model=LoreEntry)
def update_lore_entry(
    *,
    db: Session = Depends(get_db),
    lore_id: int,
    lore_in: LoreEntryUpdate
):
    """
    更新一个设定条目。
    """
    db_lore_entry = lore_entry.get(db=db, id=lore_id)
    if not db_lore_entry:
        raise HTTPException(status_code=404, detail="Lore entry not found")
    updated_lore_entry = lore_entry.update(db=db, db_obj=db_lore_entry, obj_in=lore_in)
    return updated_lore_entry


@router.delete("/{lore_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lore_entry(
    *,
    db: Session = Depends(get_db),
    lore_id: int
):
    """
    删除一个设定条目。
    """
    deleted_lore_entry = lore_entry.remove(db=db, id=lore_id)
    if not deleted_lore_entry:
        raise HTTPException(status_code=404, detail="Lore entry not found")
    return