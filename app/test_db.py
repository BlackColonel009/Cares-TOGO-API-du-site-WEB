import psycopg2
from config import DATABASE_URL

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connexion réussie à PostgreSQL")
    conn.close()
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
