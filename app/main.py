from fastapi import FastAPI
from app.routes import authRoute
from app.routes import banqueRoute


app = FastAPI()

app.include_router(authRoute.router)
app.include_router(banqueRoute.router)


"""route a la racine : root"""
@app.get("/")
def root():
  return {"message": "Bienvenu Boss"}