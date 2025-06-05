import sys
import os
import urllib.parse
import locale
import logging

from app.utils.policy import afficher_banner

afficher_banner()

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
from sqlalchemy import text
from app.database import engine

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, Depends
from app.database import get_db
from sqlalchemy.orm import Session
# from models.model_newsletter import NewsletterSubscriber

from app.database import Base, engine
from app.routes import (
    auth, media, blog, comments, category, bibliotheque,
    partners, members, homepage, stats, users, contact, newsletter
)

app = FastAPI()

# ✅ Création automatique des tables
Base.metadata.create_all(bind=engine)
logger.info("✅ Tables créées avec succès !")



@app.get("/")
def read_root():
    return {"message": "Welcome to CARES TOGO API!"}

# @app.get("/force-drop-newsletter-index")
# def force_drop_newsletter_index():
#     try:
#         with engine.connect() as connection:
#             connection.execute(text("DROP INDEX IF EXISTS ix_newsletter_subscribers_id"))
#         return {"message": "✅ Index 'ix_newsletter_subscribers_id' supprimé avec succès."}
#     except Exception as e:
#         return {"error": str(e)}

# @app.get("/force-create-table")
# def create_contact_table(db: Session = Depends(get_db)):
#     NewsletterSubscriber.__table__.create(bind=db.bind, checkfirst=True)
#     return {"message": "Table créée (si elle n'existait pas déjà)."}

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
app.include_router(contact.router, prefix="/contact", tags=["Contact"])
app.include_router(newsletter.router, prefix="/newsletter", tags=["Newsletter"])


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
