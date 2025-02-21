from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Le mot de passe en clair (sera haché)

class UserLogin(BaseModel):
    email: EmailStr
    password: str  # Mot de passe pour la connexion

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        orm_mode = True
