from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.models.category import Category

router = APIRouter(prefix="/api/categories", tags=["Categories"])


class CategoryOut(BaseModel):
    id:   int
    name: str
    icon: str

    model_config = {"from_attributes": True}


@router.get("/", response_model=List[CategoryOut],
            summary="Список всех категорий")
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
