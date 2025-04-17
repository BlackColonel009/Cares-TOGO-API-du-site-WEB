from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.model_users import User
from app.models.model_blog import BlogPost
from app.models.model_bibliotheque import Book
from app.models.model_partners import Partner
from app.models.model_members import Member
from app.models.model_media import Media

router = APIRouter()

@router.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    """Obtenir les statistiques générales du système"""
    user_count = db.query(User).count()
    blog_count = db.query(BlogPost).count()
    book_count = db.query(Book).count()
    partner_count = db.query(Partner).count()
    member_count = db.query(Member).count()
    Galery_count = db.query(Media).count()

    return {
        "total_users": user_count,
        "total_articles": blog_count,
        "total_books": book_count,
        "total_partners": partner_count,
        "total_members": member_count,
        "total_pictures": Galery_count,
    }
