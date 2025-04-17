from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.model_homepage import Homepage  # ✅ Importer le modèle
from app.services import get_homepage, update_homepage
from app.schemas import HomepageUpdate, HomepageResponse
import base64

router = APIRouter()


@router.get("/", response_model=HomepageResponse)
def read_homepage(db: Session = Depends(get_db)):
    """Récupérer les informations de la page d'accueil"""
    homepage = get_homepage(db)
    if not homepage:
        raise HTTPException(status_code=404, detail="Page d'accueil introuvable")

    # ✅ Conversion explicite de `updated_at` en string
    homepage_dict = homepage.__dict__
    homepage_dict["updated_at"] = str(homepage.updated_at)

    return homepage_dict


@router.put("/")
async def update_homepage_data(data: HomepageUpdate, db: Session = Depends(get_db)):
    homepage = db.query(Homepage).first()
    if not homepage:
        raise HTTPException(status_code=404, detail="Page d'accueil introuvable")

    homepage.text_1 = data.text_1
    homepage.text_2 = data.text_2
    homepage.text_3 = data.text_3
    homepage.text_4 = data.text_4
    homepage.text_5 = data.text_5
    homepage.contact_info = data.contact_info
    homepage.social_links = data.social_links

    # ✅ Gérer les images encodées en Base64 et stocker l'URL complète
    if data.carousel_images:
        image_urls = []
        for index, base64_image in enumerate(data.carousel_images):
            try:
                image_path = f"uploads/carousel_{index}.jpg"
                with open(image_path, "wb") as file:
                    file.write(base64.b64decode(base64_image))
                
                # ✅ Construire l'URL accessible
                image_url = f"{image_path}"
                image_urls.append(image_url)

            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erreur lors du décodage de l'image : {str(e)}")

        homepage.carousel_images = image_urls  # ✅ Stocker les URLs complètes

    db.commit()
    db.refresh(homepage)
    return {"message": "Homepage mise à jour avec succès", "carousel_images": homepage.carousel_images}
