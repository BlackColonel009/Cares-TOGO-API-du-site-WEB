from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.model_blog import Comment
from app.models.model_users import User
from app.schemas import CommentCreate, CommentResponse
from app.services import create_comment, get_comments_by_blog, delete_comment
from app.services import get_current_user, get_admin_user

router = APIRouter()

@router.post("/{blog_id}", response_model=CommentResponse)
def add_comment(blog_id: int, comment: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Ajouter un commentaire à un article"""
    return create_comment(db=db, blog_id=blog_id, user_id=user.id, content=comment.content)

@router.get("/{blog_id}", response_model=List[CommentResponse])
def list_comments(blog_id: int, db: Session = Depends(get_db)):
    """Lister tous les commentaires d’un article"""
    comments = get_comments_by_blog(db, blog_id)
    return [CommentResponse.model_validate(c) for c in comments]  # ✅ Conversion

@router.delete("/{comment_id}")
def remove_comment(comment_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Supprimer un commentaire (Admin uniquement)"""
    if not delete_comment(db, comment_id):
        raise HTTPException(status_code=404, detail="Commentaire introuvable")
    return {"message": "Commentaire supprimé avec succès"}
