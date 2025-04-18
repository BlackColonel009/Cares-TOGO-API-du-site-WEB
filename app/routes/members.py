from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from sqlalchemy.orm import Session
from app.database import get_db
import os
import shutil
from app.models.model_members import Member
from app.models.model_users import User
from app.schemas import MemberCreate, MemberUpdate, MemberResponse
from app.services import get_admin_user, create_member, get_member, update_member, delete_member

router = APIRouter()

UPLOAD_DIR = "uploads/members"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=MemberResponse)
async def add_member(
    nom_et_prenom: str = Form(...),
    poste: str = Form(...),
    contact: str = Form(...),
    email: str = Form(...),
    profile: UploadFile = File(None),
    db: Session = Depends(get_db), 
    admin: User = Depends(get_admin_user)
):
    """Créer un nouveau membre (Admin uniquement)"""
    profil = None
    if profile:
        file_path = f"{UPLOAD_DIR}/{profile.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile.file, buffer)
        profil = file_path

    member_data = MemberCreate(
        nom_et_prenom=nom_et_prenom,
        poste=poste,
        contact=contact,
        email=email,
        profil=profil
    )

    new_member =  create_member(db, member_data)  # ✅ Utilisation de `await`
    return new_member  # ✅ Retourne bien un modèle Pydantic ou un dictionnaire


@router.get("/", response_model=List[MemberResponse])
def list_members(db: Session = Depends(get_db)):
    """Lister tous les membres"""
    members = db.query(Member).all()
    return [MemberResponse.model_validate(m) for m in members]  # ✅ Conversion Pydantic

@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    """Obtenir un membre spécifique"""
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Membre introuvable")
    return member

@router.put("/{member_id}", response_model=MemberResponse)
async def update_member(
    member_id: int,  # ✅ Ajout du paramètre member_id dans la fonction
    nom_et_prenom: str = Form(None),
    poste: str = Form(None),
    contact: str = Form(None),
    email: str = Form(None),
    profile: UploadFile = File(None),
    db: Session = Depends(get_db), 
    admin: User = Depends(get_admin_user)  # Seuls les admins peuvent modifier
):
    """Mettre à jour un membre (Admin uniquement)"""

    # ✅ Vérifier si le membre existe
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Membre introuvable")

    # ✅ Gérer l'upload de l'image de profil
    profil = member.profil  # Garder l'ancien profil si aucun fichier n'est envoyé
    if profile:
        file_path = f"{UPLOAD_DIR}/{profile.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile.file, buffer)
        profil = file_path  # ✅ Mise à jour du chemin de l'image

    # ✅ Préparer les nouvelles données du membre
    member.nom_et_prenom = nom_et_prenom.strip() if nom_et_prenom else member.nom_et_prenom
    member.poste = poste.strip() if poste else member.poste
    member.contact = contact.strip() if contact else member.contact
    member.email = email.strip() if email else member.email
    member.profil = profil

    # ✅ Enregistrer les modifications
    db.commit()
    db.refresh(member)

    return member  # ✅ Retourner l'objet mis à jour


@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db), user=Depends(get_admin_user)):
    """Supprimer un membre (Admin uniquement)"""
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Membre introuvable")

    db.delete(member)
    db.commit()
    return {"message": "Membre supprimé avec succès"}
