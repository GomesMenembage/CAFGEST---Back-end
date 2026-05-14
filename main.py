from fastapi import FastAPI
from Models.database import start_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    start_db()