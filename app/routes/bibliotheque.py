from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
import urllib.parse
import shutil
import os
from app.database import get_db
from app.models.model_users import User
from app.schemas import BookCreate, BookUpdate, BookResponse
from app.services import create_book, get_books, get_book_by_id, update_book, delete_book, get_current_user, check_role, get_admin_user

router = APIRouter()

UPLOAD_DIR = "uploads/books"
UPLOAD_DIR_COVER = "uploads/books/cover"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR_COVER, exist_ok=True)


@router.post("/upload_book/")
async def upload_book(file: UploadFile = File(...), cover_url: UploadFile = File(...)):
    """ 📥 Route pour uploader un fichier """
    
    # ✅ Vérifier si un fichier a été envoyé
    if not file:
        raise HTTPException(status_code=400, detail="Aucun fichier envoyé")
    if not cover_url:
        raise HTTPException(status_code=400, detail="Aucun fichier envoyé")

    # ✅ Nettoyage du nom du fichier pour éviter les caractères spéciaux
    safe_filename = file.filename.replace(" ", "_").replace("é", "e").replace("è", "e").replace("à", "a")
    safe_cover_filename = cover_url.filename.replace(" ", "_").replace("é", "e").replace("è", "e").replace("à", "a")
    
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    cover_path = os.path.join(UPLOAD_DIR_COVER, safe_cover_filename)

    # ✅ Sauvegarde du fichier principal
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Sauvegarde de l'image de couverture
    with open(cover_path, "wb") as buffer:
        shutil.copyfileobj(cover_url.file, buffer)

    # ✅ Retourne l'URL correcte des fichiers sauvegardés
    return {
        "file": {"filename": file.filename, "url": f"/uploads/books/{safe_filename}"},
        "cover_url": {"filename": cover_url.filename, "url": f"/uploads/books/cover/{safe_cover_filename}"}
    }


@router.post("/", response_model=BookResponse)
async def add_book(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    cover_url: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Ajouter un livre (Admin ou Éditeur uniquement)"""
    # ✅ Définition correcte du `user_id`
    user_id = admin.id  # 🔥 Correction de l'erreur !

    
    # ✅ Vérification et enregistrement du fichier
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
        # ✅ Vérification et enregistrement du fichier
    cover_path = f"{UPLOAD_DIR_COVER}/{cover_url.filename}"
    with open(cover_path, "wb") as buffer:
        shutil.copyfileobj(cover_url.file, buffer)

    book_data = {
        "title": title.strip(),
        "author": author.strip(),
        "description": description.strip() if description else None,
        "file_url": file_path,
        "cover_url":cover_path,
    }   

    return create_book(db, book_data, user_id)

@router.get("/", response_model=List[BookResponse])
def list_books(db: Session = Depends(get_db), search: Optional[str] = None):
    """Récupérer tous les livres avec option de recherche"""
    books = get_books(db, search)
    if not books:
        raise HTTPException(status_code=404, detail="📚 Aucun livre disponible pour le moment.")
    
    return [BookResponse.model_validate(b) for b in books]  # ✅ Conversion


@router.put("/{book_id}", response_model=BookResponse)
async def edit_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    file: Optional[UploadFile] = File(None),
    cover_url: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Modifier un livre (Admin & Editor uniquement)"""
    book_data = {"title": title, "author": author, "description": description}

    if file:
        file_location = f"uploads/books/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())
        book_data["file_url"] = file_location
        
    if cover_url:
        file_location = f"uploads/books/cover/{cover_url.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(cover_url.file.read())
        book_data["cover_url"] = file_location

    book = update_book(db, book_id, book_data, user)
    if not book:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return book


@router.delete("/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Supprimer un livre (Admin & Editor uniquement)"""
    if not delete_book(db, book_id, user):
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return {"message": "Livre supprimé avec succès"}
