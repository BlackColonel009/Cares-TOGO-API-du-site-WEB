# app/routes/library.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models.model_bibliotheque
from app import schemas, services, database

router = APIRouter()

# Ajouter un livre
@router.post("/create_book")
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    return services.create_book(db=db, book=book)
