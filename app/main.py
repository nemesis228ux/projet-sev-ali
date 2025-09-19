from fastapi import FastAPI
from app.routes import authRoute
from app.routes import banqueRoute
from app.routes import userRoute
from app.routes.compteRoute import router as compte_routes
from app.routes.transactionRoute import router as transaction_routes
from app.routes.carteRoute import router as carte_routes

from app.models import add_all_tables
add_all_tables()

app = FastAPI()

app.include_router(authRoute.router)

app.include_router(banqueRoute.router)

app.include_router(userRoute.router)

app.include_router(compte_routes)

app.include_router(transaction_routes)

app.include_router(carte_routes)



"""route a la racine : root"""
@app.get("/")
def root():
  return {"message": "Bienvenu Boss"}