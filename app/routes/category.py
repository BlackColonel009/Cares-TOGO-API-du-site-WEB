from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CategoryCreate, CategoryResponse
from app.services import create_category, get_all_categories, get_category_by_name
from app.models.model_users import User
from app.services import get_admin_user

router = APIRouter(prefix="/categories", tags=["Catégories"])

@router.post("/", response_model=CategoryResponse)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Créer une catégorie (Admin uniquement)"""
    existing_category = get_category_by_name(db, category.name)
    if existing_category:
        raise HTTPException(status_code=400, detail="Cette catégorie existe déjà.")
    return create_category(db, category)

@router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """Lister toutes les catégories"""
    return get_all_categories(db)
