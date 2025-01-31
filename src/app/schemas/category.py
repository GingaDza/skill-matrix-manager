# src/app/schemas/category.py
from typing import Optional, List
from pydantic import BaseModel
from .base import TimestampSchema

class CategoryBase(BaseModel):
    name: str
    description: str | None = None
    parent_id: int | None = None

class CategoryCreate(CategoryBase):
    pass

# CategoryModelからCategoryに名前を変更
class Category(CategoryBase, TimestampSchema):
    id: int
    
    class Config:
        from_attributes = True

class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    parent_id: int | None = None

class CategoryResponse(Category):
    subcategories: List["CategoryResponse"] = []
    parent_name: str | None = None

# 循環参照を解決するための型ヒント
CategoryResponse.model_rebuild()