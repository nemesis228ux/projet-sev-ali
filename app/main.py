from fastapi import FastAPI

from app.models import add_all_tables
from app.routes import authRoute
from app.routes import banqueRoute
from app.routes import userRoute
from app.routes.carteRoute import router as carte_routes
from app.routes.compteRoute import router as compte_routes
from app.routes.transactionRoute import router as transaction_routes
from fastapi.middleware.cors import CORSMiddleware


add_all_tables()

app = FastAPI()

app.include_router(authRoute.router)

app.include_router(banqueRoute.router)

app.include_router(userRoute.router)

app.include_router(compte_routes)

app.include_router(transaction_routes)

app.include_router(carte_routes)


# liste des origines autorisé
origins = [
    "http://localhost:5173", ## url front en local
    "" ## url front en prod
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods = ['*'],
    allow_headers = ['*']
)


# Route de monitoring
@app.api_route("/health", methods=["GET", "HEAD", "POST"], include_in_schema=False)
def health():
    """Route de monitoring"""
    return {"message": "running"}


@app.get("/")
def root():
    """Route à la racine : root"""
    return {"message": "Bienvenu Boss"}
