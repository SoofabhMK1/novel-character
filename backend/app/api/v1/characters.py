from typing import List, Literal
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud.crud_character import character
# --- 新增导入我们刚创建的 DashboardStats Schema ---
from app.schemas.character import (Character, CharacterCreate, CharacterUpdate, 
                                     DashboardStats, Relationship, RelationshipCreate)
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

# =======================================================
# ==              新增的角色关系 API 端点              ==
# =======================================================

@router.post("/{character_id}/relationships", response_model=Relationship, status_code=status.HTTP_201_CREATED)
def create_relationship_for_character(
    *,
    db: Session = Depends(get_db),
    character_id: uuid.UUID,
    relationship_in: RelationshipCreate,
):
    """
    为指定 ID 的角色创建一个新的关系。
    """
    # 检查发起方角色是否存在
    db_character = character.get(db=db, id=character_id)
    if not db_character:
        raise HTTPException(status_code=404, detail="Origin character not found")
    
    # 检查目标角色是否存在
    target_character = character.get(db=db, id=relationship_in.character_to_id)
    if not target_character:
        raise HTTPException(status_code=404, detail="Target character not found")

    new_relationship = character.add_relationship(
        db=db, character_from_id=character_id, obj_in=relationship_in
    )
    return new_relationship


@router.get("/{character_id}/relationships", response_model=List[Relationship])
def get_relationships_for_character(
    *,
    db: Session = Depends(get_db),
    character_id: uuid.UUID,
):
    """
    获取指定 ID 角色的所有关系。
    """
    db_character = character.get(db=db, id=character_id)
    if not db_character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    relationships = character.get_relationships_for_character(db=db, character_id=character_id)
    return relationships


@router.delete("/relationships/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relationship(
    *,
    db: Session = Depends(get_db),
    relationship_id: int,
):
    """
    通过 ID 删除一个关系。
    """
    deleted_relationship = character.delete_relationship(db=db, relationship_id=relationship_id)
    if not deleted_relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")
    
    # 对于成功的 DELETE 操作，通常不返回任何内容
    return