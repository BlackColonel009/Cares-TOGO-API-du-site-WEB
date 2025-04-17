from sqlalchemy import Column, DateTime, Integer, String, JSON, TIMESTAMP, TEXT, ARRAY, text
from app.database import Base
from datetime import datetime

class Homepage(Base):
    __tablename__ = "homepage"

    id = Column(Integer, primary_key=True, index=True)
    carousel_images = Column(ARRAY(String), default=[])  # ✅ Utilisation d'un tableau de textes
    text_1 = Column(String, nullable=True, default="Bienvenue sur notre site!")
    text_2 = Column(String, nullable=True, default="Découvrez nos services.")
    text_3 = Column(String, nullable=True, default="Contactez-nous pour plus d'infos.")
    text_4 = Column(String, nullable=True, default="titre Carroussel.")
    text_5 = Column(String, nullable=True, default="Info sur carrousel.")
    social_links = Column(JSON, default={})
    contact_info = Column(String, nullable=True, default="contact@carestogo.com")
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
