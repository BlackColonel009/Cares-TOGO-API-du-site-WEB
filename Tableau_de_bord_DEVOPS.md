python -m venv venv
venv\Scripts\activate  # Sur Windows
# apres avoir activer l'environnement lance l'API
uvicorn app.main:app --reload
# Si tout fonctionne, l’API sera dispo sur http://127.0.0.1:8000

#mise a jour de creation de table psql
alembic revision --autogenerate -m "Ajout du modèle Media"
alembic upgrade head

#Affichage d'images
http://127.0.0.1:8000/uploads/articles/image.jpg


L'erreur 422 Unprocessable Entity signifie que la requête envoyée ne correspond pas au schéma attendu par FastAPI. Voici ce qu’il faut vérifier et corriger 