import sys
import os
from app.routes import users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth
from app.routes import media
from app.routes import blog
from app.routes import comments
from app.routes import auth
from app.routes import category
from app.routes import bibliotheque






app = FastAPI()

# Supprime toutes les tables existantes
# Base.metadata.drop_all(bind=engine)   
#creaton des tables automomatiques
Base.metadata.create_all(bind=engine)
print("✅ Tables créées avec succès !")

@app.get("/")
def read_root():
    return {"message": "Welcome to CARES TOGO API!"}


app.include_router(users.router, prefix="/users", tags=["Utilisateurs"])

app.include_router(auth.router, prefix="/auth", tags=["Authentification"])

app.include_router(media.router, prefix="/media", tags=["Médias"])

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(blog.router, prefix="/blog", tags=["Blog"])

app.include_router(comments.router, prefix="/comments", tags=["Commentaires"])

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router, prefix="/auth", tags=["Authentification"])

app.include_router(category.router)  # ✅ Enregistrement de la route des catégories

app.include_router(bibliotheque.router, prefix="/bibliotheque", tags=["Bibliothèque"])

#Pour pouvoir envoyer les requetes directement et eviter les erreur 405 (requete options) Methode not allowed

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permettre l'accès depuis n'importe quel domaine
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, DELETE...)
    allow_headers=["*"],  # Autoriser tous les headers
)

