# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(Text)
    file_url = Column(String)  # URL du fichier du livre (PDF, etc.)

    # Si tu veux lier des catégories ou autres informations, tu peux ajouter ici
