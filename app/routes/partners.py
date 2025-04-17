from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil
import os
from app.database import get_db
from app.models.model_users import User
from app.schemas import PartnerCreate, PartnerUpdate, PartnerResponse
from app.services import create_partner, get_partners, get_partner_by_id, update_partner, delete_partner, get_admin_user

router = APIRouter()

UPLOAD_DIR = "uploads/partners"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=PartnerResponse)
async def add_partner(
    name: str = Form(...),
    description: str = Form(None),
    website_url: str = Form(None),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Ajouter un partenaire (Admin uniquement)"""
    logo_url = None
    if logo:
        file_path = f"{UPLOAD_DIR}/{logo.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(logo.file, buffer)
        logo_url = file_path

    # ✅ Suppression des guillemets inutiles avant insertion
    cleaned_name = name.strip()
    cleaned_description = description.strip() if description else None
    cleaned_website_url = website_url.strip() if website_url else None
    
    partner = PartnerCreate(name=name, description=description, website_url=website_url, logo_url=logo_url)
    return create_partner(db, partner)

@router.get("/", response_model=list[PartnerResponse])
def list_partners(db: Session = Depends(get_db)):
    """Récupérer tous les partenaires"""
    return get_partners(db)

@router.put("/{partner_id}", response_model=PartnerResponse)
async def edit_partner(
    partner_id: int,
    name: str = Form(None),
    description: str = Form(None),
    website_url: str = Form(None),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Modifier un partenaire (Admin uniquement)"""
    partner = get_partner_by_id(db, partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partenaire introuvable")

    logo_url = partner.logo_url
    if logo:
        file_path = f"{UPLOAD_DIR}/{logo.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(logo.file, buffer)
        logo_url = file_path

    update_data = PartnerUpdate(
        name=name.strip() if name else partner.name,
        description=description.strip() if description else partner.description,
        website_url=website_url.strip() if website_url else partner.website_url,
        logo_url=logo_url
    )

    updated_partner = update_partner(db, partner_id, update_data)
    return updated_partner


@router.delete("/{partner_id}")
def remove_partner(partner_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Supprimer un partenaire (Admin uniquement)"""
    if not delete_partner(db, partner_id):
        raise HTTPException(status_code=404, detail="Partenaire introuvable")
    return {"message": "Partenaire supprimé avec succès"}
