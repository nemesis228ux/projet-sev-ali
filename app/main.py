from fastapi import FastAPI
from app.routes import authRoute


app = FastAPI()

app.include_router(authRoute.router)


"""route a la racine : root"""
@app.get("/")
def root():
  return {"message": "Bienvenu Boss"}