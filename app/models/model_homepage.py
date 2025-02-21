# app/models.py

from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class HomePageContent(Base):
    __tablename__ = 'homepage_content'

    id = Column(Integer, primary_key=True, index=True)
    section_name = Column(String)  # Exemple : 'hero', 'about', 'services'
    content = Column(Text)  # Texte à afficher
    image_url = Column(String)  # URL de l'image d'accueil
