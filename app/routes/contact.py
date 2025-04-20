from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.model_contact import Contact
from app.schemas import ContactCreate
from app.schemas import ContactOut
from typing import List
from app.utils.mail_config import send_contact_email  # si tu l’as mis là

router = APIRouter()

@router.get("/", response_model=List[ContactOut])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).order_by(Contact.created_at.desc()).all()

@router.post("/", status_code=201)
async def submit_contact(
    contact: ContactCreate,
    background_tasks: BackgroundTasks, # ✅ SANS Depends(),
    db: Session = Depends(get_db),

):
    new_msg = Contact(**contact.dict())
    db.add(new_msg)
    db.commit()

    # Envoi en tâche de fond
    background_tasks.add_task(
        send_contact_email,
        contact.name,
        contact.email,
        contact.subject,
        contact.message
    )

    return {"message": "Message reçu et envoyé par email avec succès !"}

@router.delete("/clear")
def delete_all_contacts(db: Session = Depends(get_db)):
    deleted = db.query(Contact).delete()
    db.commit()
    return {"message": f"✅ {deleted} messages de contact supprimés."}


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Message de contact introuvable.")
    
    db.delete(contact)
    db.commit()
    return {"message": f"✅ Message avec ID {contact_id} supprimé."}

