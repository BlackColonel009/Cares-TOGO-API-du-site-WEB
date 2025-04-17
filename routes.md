# 📌 Routes de l'API CARES TOGO

## 🔹 Authentification & Gestion des Utilisateurs

### 🔑 Connexion
- **POST** `/auth/login`
  - **Description :** Se connecter et obtenir un token JWT
  - **Body (form-data) :**
    ```json
    {
      "username": "email@example.com",
      "password": "motdepasse"
    }
    ```
  - **Réponse :**
    ```json
    {
      "access_token": "TOKEN_JWT",
      "token_type": "bearer"
    }
    ```

### 👤 Récupération des Infos de l’Utilisateur Connecté
- **GET** `/auth/me`
  - **Headers :** `Authorization: Bearer TOKEN`
  - **Réponse :**
    ```json
    {
      "id": 1,
      "username": "logan",
      "email": "logan@example.com",
      "role": "admin"
    }
    ```

### ⚡ Gestion des Rôles (Admin seulement)
- **PUT** `/auth/users/{user_id}/role?role=editor`
  - **Description :** Modifier le rôle d’un utilisateur
  - **Headers :** `Authorization: Bearer TOKEN_ADMIN`
  - **Réponse :**
    ```json
    {
      "message": "Le rôle de l'utilisateur a été mis à jour."
    }
    ```

---

## 📌 Gestion des Articles de Blog

### 📄 Récupérer les Articles (avec Recherche & Filtrage)
- **GET** `/blog/`
  - **Query Params :**
    - `search` : Filtrer par mot-clé
    - `category` : Filtrer par catégorie
    - `author_id` : Filtrer par auteur
    - `sort_by` : Trier par date (`recent` ou `oldest`)
  - **Réponse :** Liste des articles filtrés

### ✍️ Ajouter un Article (Admin & Rédacteur)
- **POST** `/blog/`
  - **Headers :** `Authorization: Bearer TOKEN`
  - **Body (form-data) :**
    - `title`
    - `content`
    - `categories` (liste séparée par des virgules)
    - `file` (image en option)
  - **Réponse :**
    ```json
    {
      "id": 1,
      "title": "Titre de l'article",
      "content": "Contenu ici...",
      "categories": ["Tech", "AI"],
      "created_at": "2024-02-21T12:34:56"
    }
    ```

### 📝 Modifier un Article
- **PUT** `/blog/{article_id}`
  - **Headers :** `Authorization: Bearer TOKEN`
  - **Body :**
    ```json
    {
      "title": "Nouveau titre",
      "content": "Mise à jour de l'article..."
    }
    ```

### ❌ Supprimer un Article
- **DELETE** `/blog/{article_id}`
  - **Headers :** `Authorization: Bearer TOKEN`
  - **Réponse :**
    ```json
    { "message": "Article supprimé" }
    ```

---

## 📌 Gestion des Catégories

### 📂 Ajouter une Catégorie (Admin seulement)
- **POST** `/categories/`
  - **Headers :** `Authorization: Bearer TOKEN_ADMIN`
  - **Body :**
    ```json
    { "name": "Technologie" }
    ```
  - **Réponse :**
    ```json
    { "id": 1, "name": "Technologie" }
    ```

### 📜 Voir Toutes les Catégories
- **GET** `/categories/`
  - **Réponse :**
    ```json
    [ { "id": 1, "name": "Technologie" }, { "id": 2, "name": "Science" } ]
    ```

---

## 📌 Gestion de la Bibliothèque (Livres)

### 📚 Ajouter un Livre (Admin & Rédacteur)
- **POST** `/bibliotheque/`
  - **Headers :** `Authorization: Bearer TOKEN`
  - **Body (form-data) :**
    - `title`
    - `author`
    - `description`
    - `file` (PDF ou EPUB)
  - **Réponse :**
    ```json
    {
      "id": 1,
      "title": "Nom du livre",
      "author": "Auteur",
      "file_url": "uploads/books/livre.pdf"
    }
    ```

### 📖 Voir la Liste des Livres
- **GET** `/bibliotheque/`
  - **Query Param :** `search` (optionnel pour filtrer par titre ou auteur)
  - **Réponse :**
    ```json
    [
      {
        "id": 1,
        "title": "Livre 1",
        "author": "Auteur",
        "file_url": "uploads/books/livre1.pdf"
      }
    ]
    ```

### 📝 Modifier un Livre (Admin & Rédacteur)
- **PUT** `/bibliotheque/{book_id}`
  - **Headers :** `Authorization: Bearer TOKEN`
  - **Body :**
    ```json
    {
      "title": "Nouveau Titre",
      "author": "Nouvel Auteur"
    }
    ```

### ❌ Supprimer un Livre (Admin & Rédacteur)
- **DELETE** `/bibliotheque/{book_id}`
  - **Headers :** `Authorization: Bearer TOKEN`
  - **Réponse :**
    ```json
    { "message": "Livre supprimé avec succès" }
    ```

