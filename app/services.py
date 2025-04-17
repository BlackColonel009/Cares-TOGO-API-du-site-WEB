# app/services.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, List
from fastapi import status
from app.database import get_db  # ✅ Assurez-vous que cette ligne est présente !
from sqlalchemy.orm import Session
from app.schemas import UserCreate, BlogPostCreate, BlogPostUpdate, BookCreate, CommentCreate, CategoryCreate, BookUpdate, PartnerCreate, PartnerUpdate, MemberCreate, MemberUpdate, HomepageUpdate# ✅ Ajoute `UserCreate`
from app.models.model_users import User  # ✅ Importation correcte
from app.models.model_blog import BlogPost, Comment
from app.models.model_bibliotheque import Book
from app.models.model_category import Category
from app.models.model_partners import Partner
from app.models.model_members import Member
from app.models.model_homepage import Homepage
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
import json
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Configuration du hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clé secrète et algorithme JWT
SECRET_KEY = "mysecretkey"  # 🔴 À stocker dans un .env plus tard
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


#USER AUTHENTICATION
def is_admin(user: User) -> bool:
    return user.is_admin

def check_role(user: User, required_role: str):
    """ Vérifie si l'utilisateur a le rôle requis """
    if user.role != required_role and user.role != "admin":  # ✅ Les admins ont tous les droits
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé : Vous n'avez pas la permission."
        )


def update_user_profile(db: Session, user_id: int, username: str, email: str, bio: str, avatar_url: str):
    """Met à jour le profil utilisateur"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    user.username = username
    user.email = email
    user.bio = bio
    user.avatar_url = avatar_url  # ✅ Correction ici

    db.commit()
    db.refresh(user)
    return user



def get_user_by_id(db: Session, user_id: int):
    """ Récupérer un utilisateur par son ID """
    return db.query(User).filter(User.id == user_id).first()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ Vérifier et décoder le JWT pour récupérer l'utilisateur connecté """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur introuvable")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

def get_admin_user(current_user: User = Depends(get_current_user)):
    """ Vérifier si l'utilisateur est un admin """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return current_user

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print("✅ Token généré :", token)  # ✅ Debug
        return token
    except Exception as e:
        print("❌ Erreur JWT:", str(e))  # ✅ Debug
        return None


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user  # ✅ On retourne directement l'utilisateur
    return None


#BLOGPOST
def create_blog_post(db: Session, blog: BlogPostCreate, user_id: int, image_url: str = None):
    """ Créer un nouvel article de blog """
    db_blog = BlogPost(title=blog.title,
                        content=blog.content, 
                        image_url=image_url, 
                        user_id=user_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_all_blog_posts(db: Session):
    """ Récupérer tous les articles """
    return db.query(BlogPost).all()

def get_blog_post(db: Session, blog_id: int):
    """ Récupérer un article par son ID """
    return db.query(BlogPost).filter(BlogPost.id == blog_id).first()

def update_blog_post(db: Session, blog_id: int, blog: BlogPostUpdate):
    """ Modifier un article de blog """
    db_blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if db_blog:
        db_blog.title = blog.title
        db_blog.content = blog.content
        db.blog.image_url = blog.image_url
        db.commit()
        db.refresh(db_blog)
        return db_blog
    return None

def delete_blog_post(db: Session, blog_id: int):
    """ Supprimer un article de blog """
    db_blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
        return True
    return False


def get_blogs(db: Session):
    return db.query(BlogPost).options(joinedload(BlogPost.user)).all()


# app/services.py

def create_book(db: Session, book_data: dict, user_id: int):
    """Créer un livre en base de données"""
    from app.models.model_bibliotheque import Book  # Import interne pour éviter les boucles d'import

    db_book = Book(
        title=book_data["title"],
        author=book_data["author"],
        description=book_data.get("description"),
        file_url=book_data["file_url"],
        user_id=user_id, # ✅ Correction ici
        cover_url=book_data["cover_url"],
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, search: Optional[str] = None):
    """Récupérer tous les livres (avec option de recherche)"""
    query = db.query(Book)
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%") | Book.author.ilike(f"%{search}%"))
    return query.all()

def get_book_by_id(db: Session, book_id: int):
    """Récupérer un livre par son ID"""
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, book_data: BookUpdate, user: User):
    """Modifier un livre (Admin & Editor uniquement)"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    if user.role not in ["admin", "editor"] and db_book.user_id != user.id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    
    for key, value in book_data.items():

        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int, user: User):
    """Supprimer un livre (Admin & Editor uniquement)"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    if user.role not in ["admin", "editor"] and db_book.user_id != user.id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    
    db.delete(db_book)
    db.commit()
    return True


#Comments users

def create_comment(db: Session, blog_id: int, user_id: int, content: str):
    """ Ajouter un commentaire à un article """
    comment = Comment(content=content, blog_id=blog_id, user_id=user_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments_by_blog(db: Session, blog_id: int):
    """ Récupérer tous les commentaires d’un article """
    return db.query(Comment).filter(Comment.blog_id == blog_id).all()

def delete_comment(db: Session, comment_id: int):
    """ Supprimer un commentaire """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
        return True
    return False


#Category
def create_category(db: Session, category: CategoryCreate):
    """Créer une nouvelle catégorie"""
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_categories(db: Session):
    """Récupérer toutes les catégories"""
    return db.query(Category).all()

def get_category_by_name(db: Session, name: str):
    """Récupérer une catégorie par son nom"""
    return db.query(Category).filter(Category.name == name).first()


#Partners
def create_partner(db: Session, partner: PartnerCreate):
    """Ajouter un nouveau partenaire"""
    db_partner = Partner(**partner.dict())
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner

def get_partners(db: Session):
    """Récupérer tous les partenaires"""
    return db.query(Partner).all()

def get_partner_by_id(db: Session, partner_id: int):
    """Récupérer un partenaire par son ID"""
    return db.query(Partner).filter(Partner.id == partner_id).first()

def update_partner(db: Session, partner_id: int, partner_data: PartnerUpdate):
    """Modifier un partenaire (Admin uniquement)"""
    db_partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not db_partner:
        return None
    
    for key, value in partner_data.dict(exclude_unset=True).items():
        setattr(db_partner, key, value)

    db.commit()
    db.refresh(db_partner)
    return db_partner

def delete_partner(db: Session, partner_id: int):
    """Supprimer un partenaire (Admin uniquement)"""
    db_partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not db_partner:
        return None

    db.delete(db_partner)
    db.commit()
    return True

#Members

def get_members(db: Session):
    return db.query(Member).all()

def get_member(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()

def create_member(db: Session, member_data: MemberCreate):
    new_member = Member(**member_data.dict())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def update_member(db: Session, member_id: int, member_data: MemberUpdate):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        return None
    for key, value in member_data.dict(exclude_unset=True).items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member

def delete_member(db: Session, member_id: int):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        return None
    db.delete(member)
    db.commit()
    return member

#HOME PAGE


def get_homepage(db: Session):
    homepage = db.query(Homepage).first()
    
    # ✅ Si aucune entrée n'existe, en créer une avec des valeurs par défaut
    if not homepage:
        homepage = Homepage(
            carousel_images=json.dumps([]),
            text_1="Bienvenue sur notre site!",
            text_2="Découvrez nos services.",
            text_3="Contactez-nous pour plus d'infos.",
            text_4="titre Carroussel.",
            text_5="Info sur carrousel.",
            social_links={},
            contact_info="contact@carestogo.com"
        )
        db.add(homepage)
        db.commit()
        db.refresh(homepage)  # ✅ Recharger les données après commit pour éviter NoneType
    
    return homepage


def update_homepage(db: Session, homepage_data: HomepageUpdate):
    homepage = get_homepage(db)
    for key, value in homepage_data.dict(exclude_unset=True).items():
        setattr(homepage, key, value)
    homepage.updated_at = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(homepage)
    return homepage
