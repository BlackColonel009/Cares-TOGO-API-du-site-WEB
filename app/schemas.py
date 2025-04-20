from pydantic import BaseModel, EmailStr,  Field, HttpUrl
from datetime import datetime
from typing import Optional, List, Dict


class UserLogin(BaseModel):
    email: EmailStr
    password: str  # Mot de passe pour la connexion
      

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "user"
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_admin: bool  # ✅ CE CHAMP ÉTAIT MANQUANT
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class ForceAdminRequest(BaseModel):
    email: EmailStr


#BookCreate
class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None

class BookCreate(BookBase):
    file_url: str
    cover_url: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    file_url: Optional[str] = None
    cover_url: Optional[str] = None

class BookResponse(BookBase):
    id: int
    file_url: str
    cover_url: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

# ✅ Ajout de BlogPostUpdate
class BlogPostUpdate(BaseModel):
    title: str
    content: str
    image_url: str | None = None  # ✅ Image optionnelle



#Shemas BLOG post
class BlogPostBase(BaseModel):
    title: str
    content: str
    image_url: str | None = None  # ✅ Image optionnelle

class BlogPostCreate(BlogPostBase):
    pass  # ✅ Rien de plus à ajouter pour la création

class BlogPostUpdate(BlogPostBase):
    pass  # ✅ Permettra de modifier un article

class BlogPostResponse(BaseModel):
    id: int
    title: str
    content: str
    image_url: str | None
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse]
    
    class Config:
        from_attributes = True  # ✅ Assure que Pydantic convertit bien les objets SQLAlchemy
        json_encoders = {datetime: lambda v: v.isoformat()}  # ✅ Convertir en format ISO8601

#COMMENTS
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass  # ✅ Utilisé pour créer un commentaire

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    user_id: int
    blog_id: int

    class Config:
        from_attributes = True  # ✅ Convertir SQLAlchemy en Pydantic
        json_encoders = {datetime: lambda v: v.isoformat()}
        
#Categories
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

#Partners

class PartnerBase(BaseModel):
    name: str
    description: Optional[str] = None
    website_url: Optional[str] = None

class PartnerCreate(PartnerBase):
    logo_url: Optional[str] = None

class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None

class PartnerResponse(PartnerBase):
    id: int
    logo_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}
        
#MEMBRES

class MemberBase(BaseModel):
    nom_et_prenom: str = Field(..., example="Jean Dupont")
    poste: str = Field(..., example="Directeur Général")
    profil: Optional[str] = Field(None, example="uploads/profiles/jdupont.jpg")
    contact: Optional[str] = Field(None, example="+228 90000000")
    email: EmailStr = Field(..., example="jean.dupont@example.com")

class MemberCreate(MemberBase):
    pass

class MemberUpdate(MemberBase):
    pass

class MemberResponse(MemberBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

'''reccuperation de mots de pass'''

class ForgotPasswordRequest(BaseModel):
    email: EmailStr  # ✅ Vérification que c'est un email valide

#HOME PAGE

class HomepageBase(BaseModel):
    carousel_images: List[str] = Field(default=[])
    text_1: Optional[str] = None
    text_2: Optional[str] = None
    text_3: Optional[str] = None
    text_4: Optional[str] = None
    text_5: Optional[str] = None
    social_links: Dict[str, str] = Field(default={})
    contact_info: Optional[str] = None

class HomepageUpdate(BaseModel):
    carousel_images: list[str]
    text_1: str
    text_2: str
    text_3: str
    text_4: str
    text_5: str
    social_links: dict
    contact_info: str
    
class HomepageResponse(BaseModel):
    id: int
    carousel_images: List[str]
    text_1: Optional[str]
    text_2: Optional[str]
    text_3: Optional[str]
    text_4: Optional[str]
    text_5: Optional[str]
    social_links: Dict[str, str]
    contact_info: Optional[str]
    updated_at: str  # ✅ Assurez-vous qu'il est bien de type string
    
    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}  # ✅ Convertit `datetime` en `str`
        
#Media

class MediaResponse(BaseModel):
    id: int
    name: str
    file_url: str
    media_type: str
    description: str
    created_at: datetime
    updated_at: datetime
    user_id: Optional[int]  # si `Media` est relié à un utilisateur

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}
        
#Contacts

class ContactOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    subject: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

#Newsletter
class NewsletterSubscribe(BaseModel):
    email: EmailStr