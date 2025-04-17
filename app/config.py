import os
from dotenv import load_dotenv

load_dotenv()

print(f"📌 DATABASE_URL trouvée ? {os.getenv('DATABASE_URL') is not None}")

DATABASE_URL = "postgresql://cares_togo_user:Px5O08UIUFiaUh091VC3ueoWcuAYITrf@dpg-d00jpupr0fns73ec42n0-a.virginia-postgres.render.com/cares_togo"
print(f"📌 DATABASE_URL: {DATABASE_URL}")