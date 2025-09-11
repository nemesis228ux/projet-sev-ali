from fastapi import FastAPI


app = FastAPI()


"""route a la racine : root"""
@app.get("/")
def root():
  return {"message": "Bienvenu Boss"}