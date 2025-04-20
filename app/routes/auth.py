from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Body
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
import shutil
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.model_users import User
# from app.services import authenticate_user, create_access_token
from app.services import create_access_token
from app import services  # ✅ Import de services
from app.services import get_admin_user, get_current_user, update_user_profile, get_user_by_id, get_password_hash, force_user_as_admin
from app.schemas import UserUpdate, UserResponse,ForgotPasswordRequest, ForceAdminRequest
import os
import random
import string
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"

UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # ✅ Créer le dossier avatars si inexistant


# @router.post("/login")
# def login_user(email: str, password: str, db: Session = Depends(get_db)):
#     """ Endpoint pour se connecter et récupérer un token JWT """
#     user = authenticate_user(db, email, password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")
    
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/test_login")
def test_login(form_data: OAuth2PasswordRequestForm = Depends()):
    print("✅ Requête reçue avec :", form_data.username, form_data.password)
    return {"username": form_data.username, "password": form_data.password}

#les admins peuvent odifier le role des  utilisateur
@router.put("/users/{user_id}/role")
def update_user_role(user_id: int,
                        role: str, 
                        db: Session = Depends(get_db), 
                        admin: User = Depends(get_admin_user)):
    """ Modifier le rôle d'un utilisateur (Admin uniquement) """
    valid_roles = ["admin", "editor", "user"]
    if role not in valid_roles:
        raise HTTPException(status_code=400, detail="Rôle invalide")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    user.role = role
    db.commit()
    db.refresh(user)
    return {"message": f"Le rôle de {user.username} a été mis à jour en {role}."}


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    access_token = services.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=dict)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """ Récupérer les infos du profil utilisateur connecté """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "bio": current_user.bio,
        "avatar_url": current_user.avatar_url,
        "is_admin": current_user.is_admin,
        "role": current_user.role
    }

@router.get("/admin/protected")
def admin_only_route(admin: User = Depends(services.get_admin_user)):
    return {"message": "Bienvenue Admin !"}


@router.get("/profile", response_model=UserResponse)
def get_profile(user: User = Depends(get_current_user)):
    """Récupérer le profil de l'utilisateur connecté"""
    return UserResponse.model_validate(user)  # ✅ Conversion explicite

@router.put("/profile")
async def update_profile(
    username: str = Form(None),
    email: str = Form(None),
    bio: str = Form(None),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Mettre à jour le profil de l'utilisateur"""
    
    avatar_path = user.avatar_url  # Garder l'ancien avatar si non fourni
    
    # ✅ Gestion de l'avatar
    if avatar:
        avatar_path = f"{UPLOAD_DIR}/{user.id}_{avatar.filename}"
        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)

    updated_user = update_user_profile(
        db, 
        user.id, 
        username=username or user.username, 
        email=email or user.email, 
        bio=bio or user.bio, 
        avatar_url=avatar_path
    )

    if not updated_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    return {
        "message": "Profil mis à jour avec succès",
        "username": updated_user.username,
        "email": updated_user.email,
        "bio": updated_user.bio,
        "avatar_url": updated_user.avatar_url
    }

'''Réinitialiser mon mots de pass'''

def generate_reset_token():
    """Génère un token aléatoire pour la réinitialisation"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Génère un token et envoie un lien de réinitialisation"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email introuvable")

    # ✅ Générer un token de réinitialisation
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    db.commit()

    # 🔹 Simule un envoi d'email (à remplacer par un vrai service d'email)
    reset_link = f"http://127.0.0.1:5000/auth/reset-password.html?token={reset_token}"
    print(f"🔹 Lien de réinitialisation : {reset_link}")

    return {"message": "Lien de réinitialisation envoyé (affiché en console pour test)"}


@router.post("/reset-password")
def reset_password( token: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)):
    """Réinitialise le mot de passe en utilisant le token"""
    user = db.query(User).filter(User.reset_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")

    # ✅ Met à jour le mot de passe
    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None  # Supprime le token après utilisation
    db.commit()

    return {"message": "Mot de passe réinitialisé avec succès"}









