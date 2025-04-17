from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import urllib.parse
import shutil
import os
from app.database import get_db
from app.models.model_media import Media
from app.models.model_users import User
from app.services import get_current_user, get_admin_user

router = APIRouter()

UPLOAD_DIR = "uploads"

# Créer le dossier d'upload s'il n'existe pas
os.makedirs(UPLOAD_DIR, exist_ok=True)
    
@router.post("/upload/")
def upload_file(
    name: str = "",
    file: UploadFile = File(None),
    description: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ Uploader un fichier et enregistrer ses infos en DB """

    file_extension = file.filename.split(".")[-1]
    media_type = "image" if file_extension in ["jpg", "png", "jpeg"] else "video" if file_extension in ["mp4", "mov"] else "document"

    file_url = None
    if file:
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        file_url = file_path
    

    # Enregistrement en DB
    new_media = Media(
        name=name,
        file_url=file_url,
        media_type=media_type,
        description=description,
        user_id=current_user.id
    )
    db.add(new_media)
    db.commit()
    db.refresh(new_media)

    return {"message": "Fichier uploadé avec succès", "media_id": new_media.id, "file_url": file_path}

@router.get("/")
def get_all_media(db: Session = Depends(get_db)):
    """ Récupérer tous les médias """
    return db.query(Media).all()

@router.get("/{media_id}")
def get_media(media_id: int, db: Session = Depends(get_db)):
    """ Récupérer un média par ID """
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Média non trouvé")
    return media

@router.delete("/{media_id}")
def delete_media(media_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """ Supprimer un média (Admin uniquement) """
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Média non trouvé")
    
    # Supprimer le fichier du serveur
    if os.path.exists(media.file_url):
        os.remove(media.file_url)

    db.delete(media)
    db.commit()
    return {"message": "Média supprimé"}
