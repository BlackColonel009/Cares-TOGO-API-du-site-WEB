# app/routes/blog.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models.model_blog
from app import schemas, services, database

router = APIRouter()

# Ajouter un article de blog
@router.post("/create_blog")
def create_blog(blog: schemas.BlogPostCreate, db: Session = Depends(database.get_db)):
    return services.create_blog_post(db=db, blog=blog)

# Modifier un article de blog
@router.put("/update_blog/{blog_id}")
def update_blog(blog_id: int, blog: schemas.BlogPostUpdate, db: Session = Depends(database.get_db)):
    return services.update_blog_post(db=db, blog_id=blog_id, blog=blog)
