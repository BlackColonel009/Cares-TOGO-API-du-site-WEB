# app/routes/homepage.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import model_homepage
from app import schemas, services, database

router = APIRouter()

# Modifier la section de la page d'accueil
@router.put("/update_homepage/{section_name}")
def update_homepage(section_name: str, content: schemas.HomePageContentUpdate, db: Session = Depends(database.get_db)):
    return services.update_homepage_content(section_name, content, db)
