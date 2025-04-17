# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)  # ✅ URL du fichier stocké
    media_type = Column(String, nullable=False)  # ✅ image, video, document, etc.
    description = Column(String, nullable=True) 

    blog_post_id = Column(Integer, ForeignKey('blog_posts.id'))  
    blog_post = relationship("BlogPost", back_populates="media")  # ✅ Relation correcte

    user_id = Column(Integer, ForeignKey("users.id"))  # ✅ L'utilisateur qui a uploadé
    user = relationship("User", back_populates="media")