python -m venv venv
venv\Scripts\activate  # Sur Windows
# apres avoir activer l'environnement lance l'API
uvicorn app.main:app --reload
# Si tout fonctionne, l’API sera dispo sur http://127.0.0.1:8000