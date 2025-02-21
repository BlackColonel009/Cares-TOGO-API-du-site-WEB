import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from app.database import Base, engine

app = FastAPI()
#creaton des tables automomatiques
Base.metadata.create_all(bind=engine)
print("✅ Tables créées avec succès !")

@app.get("/")
def read_root():
    return {"message": "Welcome to CARES TOGO API!"}


