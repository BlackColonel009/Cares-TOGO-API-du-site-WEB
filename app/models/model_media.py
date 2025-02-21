# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # Nom du fichier
    file_url = Column(String)  # URL du fichier média
    media_type = Column(String)  # 'image', 'video', 'book'
    description = Column(String)

    blog_post_id = Column(Integer, ForeignKey('blog_posts.id'))  # Lier ce média à un article de blog
    blog_post = relationship("BlogPost", back_populates="media")
