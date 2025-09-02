from typing import List, Literal
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.crud_character import character
# --- 新增导入我们刚创建的 DashboardStats Schema ---
from app.schemas.character import Character, CharacterCreate, CharacterUpdate, DashboardStats
from app.db.session import get_db

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
def read_dashboard_stats(
    db: Session = Depends(get_db),
):
    """
    获取用于仪表盘的统计数据。
    """
    stats = character.get_dashboard_stats(db=db)
    return stats


# --- 修改 read_characters 函数以支持排序 ---
@router.get("/", response_model=List[Character])
def read_characters(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    sort_by: str = Query("updated_at", description="Sort characters by this field."),
    order: Literal["asc", "desc"] = Query("desc", description="Sort order: 'asc' or 'desc'.")
):
    """
    获取角色列表，支持分页和排序。
    """
    characters = character.get_multi_sorted(
        db, skip=skip, limit=limit, sort_by=sort_by, order=order
    )
    return characters


@router.post("/", response_model=Character)
def create_character(
    *,
    db: Session = Depends(get_db),
    character_in: CharacterCreate,
):
    """
    创建一个新的角色。
    """
    new_character = character.create(db=db, obj_in=character_in)
    return new_character


@router.get("/{character_id}", response_model=Character)
def read_character(
    *,
    db: Session = Depends(get_db),
    character_id: uuid.UUID,
):
    """
    通过 ID 获取单个角色的详细信息。
    """
    db_character = character.get(db=db, id=character_id)
    if not db_character:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character


@router.put("/{character_id}", response_model=Character)
def update_character(
    *,
    db: Session = Depends(get_db),
    character_id: uuid.UUID,
    character_in: CharacterUpdate,
):
    """
    更新一个角色。
    """
    db_character = character.get(db=db, id=character_id)
    if not db_character:
        raise HTTPException(status_code=404, detail="Character not found")
    updated_character = character.update(db=db, db_obj=db_character, obj_in=character_in)
    return updated_character


@router.delete("/{character_id}", response_model=Character)
def delete_character(
    *,
    db: Session = Depends(get_db),
    character_id: uuid.UUID,
):
    """
    删除一个角色。
    """
    character_to_delete = character.get(db=db, id=character_id)
    if not character_to_delete:
        raise HTTPException(status_code=404, detail="Character not found")
    
    deleted_character = character.remove(db=db, id=character_id)
    return deleted_character