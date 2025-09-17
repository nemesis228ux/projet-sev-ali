from fastapi import FastAPI
from app.routes import authRoute
from app.routes import banqueRoute
from app.routes import userRoute

from app.models import add_all_tables
add_all_tables()

app = FastAPI()

app.include_router(authRoute.router)

app.include_router(banqueRoute.router)

app.include_router(userRoute.router)



"""route a la racine : root"""
@app.get("/")
def root():
  return {"message": "Bienvenu Boss"}