from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import NewsletterSubscribe
from app.models.model_newsletter import NewsletterSubscriber
from typing import Optional, List, Dict
from fastapi import BackgroundTasks
from app.utils.mail_config import send_newsletter_welcome_email  # à créer ci-dessous

router = APIRouter()

@router.get("/admin/newsletter", response_model=List[NewsletterSubscribe])
def get_all_subscribers(db: Session = Depends(get_db)):
    return db.query(NewsletterSubscriber).order_by(NewsletterSubscriber.subscribed_at.desc()).all()


@router.post("/subscribe")
def subscribe_to_newsletter(
    data: NewsletterSubscribe,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    exists = db.query(NewsletterSubscriber).filter_by(email=data.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Cet email est déjà abonné.")
    new_subscriber = NewsletterSubscriber(email=data.email)
    db.add(new_subscriber)
    db.commit()

    # Envoi du mail de bienvenue en tâche de fond
    background_tasks.add_task(send_newsletter_welcome_email, data.email)

    return {"message": "Merci pour votre abonnement ! Un mail de bienvenue a été envoyé."}

@router.delete("/clear")
def delete_all_subscribers(db: Session = Depends(get_db)):
    deleted = db.query(NewsletterSubscriber).delete()
    db.commit()
    return {"message": f"✅ {deleted} abonnés supprimés de la newsletter."}


@router.delete("/{subscriber_id}")
def delete_newsletter_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    subscriber = db.query(NewsletterSubscriber).filter(NewsletterSubscriber.id == subscriber_id).first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Abonné introuvable.")
    
    db.delete(subscriber)
    db.commit()
    return {"message": f"✅ Abonné avec ID {subscriber_id} supprimé."}

@router.get("/test-email")
async def send_test():
    await send_newsletter_welcome_email("didicko009@gmail.com")
    return {"message": "✅ Test envoyé"}