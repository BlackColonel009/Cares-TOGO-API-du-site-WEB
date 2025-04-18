from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from app import schemas, services, database
# from app.schemas import UserCreate, UserLogin
from app.schemas import UserCreate, UserResponse, ForceAdminRequest
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db  # ✅ Assurez-vous que cette ligne est présente !
from app.models import model_users  # ✅ Ajout de l'import de `models`
from app import services  # ✅ Importation correcte du fichier `services.py`
from typing import Optional, List


router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):  # ✅ Change `database.get_db` en `get_db`
    existing_user = db.query(model_users.User).filter(model_users.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    return services.create_user(db=db, user=user)


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    access_token = services.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Obtenir la liste de tous les utilisateurs"""
    users = db.query(model_users.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="Aucun utilisateur trouvé")
    
    # ✅ Convertir chaque User SQLAlchemy en UserResponse Pydantic
    return [UserResponse.model_validate(user) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son ID"""
    user = db.query(model_users.User).filter(model_users.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user

@router.put("/force-admin")
def force_admin(data: ForceAdminRequest, db: Session = Depends(get_db)):
    user = services.force_user_as_admin(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    return {"message": f"{user.username} est maintenant administrateur ✅"}