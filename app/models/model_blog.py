# app/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(String)  # Date de création de l'article
    updated_at = Column(String)  # Dernière modification de l'article

    # Lier l'article au user
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relation avec les médias
    media = relationship("Media", back_populates="blog_post", cascade="all, delete-orphan")
