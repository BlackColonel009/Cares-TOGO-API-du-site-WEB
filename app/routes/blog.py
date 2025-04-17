from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File, Form
from typing import Optional, List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.model_blog import BlogPost
from app.models.model_users import User
from app.models.model_category import Category
from app.schemas import BlogPostCreate, BlogPostUpdate, BlogPostResponse, CategoryCreate
from app.services import create_blog_post, get_all_blog_posts, get_blog_post, update_blog_post, delete_blog_post, check_role, get_category_by_name, create_category
from app.services import get_current_user, get_admin_user
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads/articles"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # ✅ Créer le dossier si inexistant



@router.post("/", response_model=BlogPostResponse)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    categories: list[str] = Form([]),  # ✅ Liste de catégories
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Créer un article (Rédacteur ou Admin uniquement)"""
    check_role(user, "editor")

    image_url = None
    if file:
        file_path = f"uploads/articles/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_url = file_path

    # ✅ Associer les catégories
    category_objects = []
    for cat_name in categories:
        category = get_category_by_name(db, cat_name)
        if not category:
            category = create_category(db, CategoryCreate(name=cat_name))
        category_objects.append(category)

    new_blog = create_blog_post(
        db=db,
        blog=BlogPostCreate(title=title, content=content),
        user_id=user.id,
        image_url=image_url
    )
    new_blog.categories = category_objects  # ✅ Ajouter les catégories à l'article
    db.commit()

    return new_blog




from sqlalchemy.orm import joinedload

@router.get("/", response_model=List[BlogPostResponse])
def list_blog_posts(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Rechercher un article par mots-clés"),
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    author_id: Optional[int] = Query(None, description="Filtrer par ID de l'auteur"),
    sort_by: Optional[str] = Query("recent", description="Trier par date : 'recent' ou 'oldest'")
):
    """ Récupérer la liste des articles avec recherche et filtres """
    query = db.query(BlogPost).options(joinedload(BlogPost.user))  # 🔹 Charger l'utilisateur

    # 🔍 Filtre par mots-clés
    if search:
        query = query.filter(BlogPost.title.ilike(f"%{search}%") | BlogPost.content.ilike(f"%{search}%"))

    # 📂 Filtre par catégorie
    if category:
        query = query.join(BlogPost.categories).filter(Category.name == category)

    # 🧑 Filtre par auteur
    if author_id:
        query = query.filter(BlogPost.user_id == author_id)

    # 📅 Tri par date
    if sort_by == "oldest":
        query = query.order_by(BlogPost.created_at.asc())
    else:
        query = query.order_by(BlogPost.created_at.desc())

    return query.all()


@router.get("/{blog_id}", response_model=BlogPostResponse)
def read_post(blog_id: int, db: Session = Depends(get_db)):
    """Récupérer un article précis avec les détails de l'auteur"""
    post = db.query(BlogPost).options(joinedload(BlogPost.user)).filter(BlogPost.id == blog_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Article introuvable")
    return post


@router.put("/{blog_id}")
async def edit_post(
    blog_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),  # L'image est optionnelle
    db: Session = Depends(get_db)
):
    """Modifier un article de blog et gérer l'upload d'image"""
    post = get_blog_post(db, blog_id)
    if not post:
        raise HTTPException(status_code=404, detail="Article introuvable")

    if image:
        # Sauvegarder l'image sur le serveur
        image_path = f"{UPLOAD_DIR}/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        post.image_url = image_path  # Mettre à jour l'URL de l'image

    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)

    return {"message": "Article mis à jour avec succès", "image_url": post.image_url}

@router.delete("/{blog_id}")
def remove_post(blog_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Supprimer un article (Admin uniquement)"""
    if not delete_blog_post(db, blog_id):
        raise HTTPException(status_code=404, detail="Article introuvable")
    return {"message": "Article supprimé avec succès"}
