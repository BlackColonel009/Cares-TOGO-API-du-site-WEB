import os
from dotenv import load_dotenv

load_dotenv()

print(f"📌 DATABASE_URL trouvée ? {os.getenv('DATABASE_URL') is not None}")
#DATABASE_URL="postgresql://postgres:roland2001@localhost:5433/cares_togo?client_encoding=UTF8"
DATABASE_URL = "postgresql://cares_admin:roland2001@31.220.87.142:5432/cares_db"
print(f"📌 DATABASE_URL: {DATABASE_URL}")