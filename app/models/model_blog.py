# app/models.py
from sqlalchemy import Table, Column, Integer, String, String, Text, ForeignKey, DateTime  # ✅ Ajout de DateTime
from sqlalchemy.orm import relationship, deferred
from datetime import datetime
from app.database import Base
from app.models.model_media import Media  # ✅ Ajout de l'import pour éviter l'erreur
from app.models.model_category import blog_post_categories  # ✅ Importer la table intermédiaire


# # 
# 
# ✅ Table intermédiaire pour la relation Many-to-Many entre BlogPost et Category
# blog_post_categories = Table(
#     "blog_post_categories",
#     Base.metadata,
#     Column("blog_post_id", Integer, ForeignKey("blog_posts.id")),
#     Column("category_id", Integer, ForeignKey("categories.id"))
# )

class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)  # ✅ Ajout du champ image
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Correction DateTime
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    
    user_id = Column(Integer, ForeignKey("users.id"))  # ✅ L’auteur de l’article
    user = relationship("User", back_populates="blog_posts")

    
    # ✅ Utiliser une relation différée pour éviter les problèmes de dépendance
    media = relationship("Media", back_populates="blog_post", cascade="all, delete-orphan", lazy="joined")

    comments = relationship("Comment", back_populates="blog_post", cascade="all, delete-orphan")
    
    categories = relationship("Category", secondary="blog_post_categories", back_populates="blog_posts")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))  # ✅ L’auteur du commentaire
    user = relationship("User", back_populates="comments")

    blog_id = Column(Integer, ForeignKey("blog_posts.id"))  # ✅ L’article concerné
    blog_post = relationship("BlogPost", back_populates="comments")
    

