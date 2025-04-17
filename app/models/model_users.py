import sys
import os
from datetime import datetime
from sqlalchemy.orm import relationship
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    role = Column(String, default="user")
    avatar_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reset_token = Column(String, nullable=True)

    blog_posts = relationship("BlogPost", back_populates="user")  # ✅ Relation ajoutée
    
    media = relationship("Media", back_populates="user")
    
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    
    books = relationship("Book", back_populates="user", cascade="all, delete-orphan")  # ✅ Ajout de cette relation