from fastapi import FastAPI
from Models.database import start_db

app = FastAPI()

from Apps.Aluno.Views.AuthView import auth
@app.on_event("startup")
async def startup():
    start_db()
    
    
app.include_router(auth)