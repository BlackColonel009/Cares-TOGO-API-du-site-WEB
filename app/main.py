import sys
import os
import urllib.parse
import locale
import logging

# ✅ Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Encodage universel
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

logger.info(f"ENCODAGE SYSTÈME : {sys.getdefaultencoding()}")
logger.info(f"ENCODAGE LOCALE : {locale.getpreferredencoding()}")

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from app.database import Base, engine
from app.routes import (
    auth, media, blog, comments, category, bibliotheque,
    partners, members, homepage, stats, users
)

app = FastAPI()

# ✅ Création automatique des tables
Base.metadata.create_all(bind=engine)
logger.info("✅ Tables créées avec succès !")

@app.get("/")
def read_root():
    return {"message": "Welcome to CARES TOGO API!"}

# ✅ Inclusion des routers (sans doublon)
app.include_router(users.router, prefix="/users", tags=["Utilisateurs"])
app.include_router(auth.router, prefix="/auth", tags=["Authentification"])
app.include_router(media.router, prefix="/media", tags=["Médias"])
app.include_router(blog.router, prefix="/blog", tags=["Blog"])
app.include_router(comments.router, prefix="/comments", tags=["Commentaires"])
app.include_router(category.router)  # Pas de prefix
app.include_router(bibliotheque.router, prefix="/bibliotheque", tags=["Bibliothèque"])
app.include_router(partners.router, prefix="/partners", tags=["Partenaires"])
app.include_router(members.router, prefix="/members", tags=["Membres"])
app.include_router(homepage.router, prefix="/homepage", tags=["Page_Accueil"])
app.include_router(stats.router, prefix="/api", tags=["Statistiques"])

# ✅ Fichiers statiques (uploads)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
