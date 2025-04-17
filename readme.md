cares_togo_api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models
│   │   ├── model_users.py
│   │   ├── model_homepage.py
│   │   ├── model_blog.py
│   │   ├── model_bibliothèque.py
│   │   ├── model_parteners.py
│   │   ├── model_media.py
│   ├── database.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── media.py
│   │   ├── blog.py
│   │   ├── partners.py
│   │   ├── homepage.py
│   ├── schemas.py
│   ├── services.py
├── .env
├── requirements.txt
├── alembic/
├── README.md


✅ Rôles :

Admin (admin) → Peut gérer les utilisateurs, articles et commentaires
Rédacteur (editor) → Peut publier et modifier ses propres articles
Utilisateur (user) → Peut commenter et voir les articles
✅ Fonctionnalités :
🔹 Limiter l’accès aux routes en fonction du rôle
🔹 Permettre aux admins d’attribuer des rôles
🔹 Gérer les rôles dans les services et routes