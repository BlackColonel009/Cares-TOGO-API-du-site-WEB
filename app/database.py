from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
# from dotenv import load_dotenv

import psycopg2
import os


try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
        # Fonction pour obtenir une session de base de données
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    with engine.connect() as connection:
        print("✅ Connexion réussie à la base de données !")

except Exception as e:
    print(f"❌ Erreur de connexion : {e}")

