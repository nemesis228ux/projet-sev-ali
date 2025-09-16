## fichier banqueRoute pour la gestion des operations des routes

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.banqueCrud import create_banque, read_all_banKs
from app.schemas.banqueSchema import BanqueRead, BanqueCreate


router = APIRouter(prefix="/banques", tags=["banques"]) ## instance de notre router fastapi / petite instance de notre app ☺


# operation GET
@router.get("/", response_model=list[BanqueRead])
def get_all_banques(db: Session = Depends(get_db)) -> list[BanqueRead]: 
  """route pour lire toutes les banques

  Args:
      db (Session, optional): prend une session de  db. Defaults to Depends(get_db).

  Returns:
      list[BanqueRead]: return liste de banque ou liste vide
  """

  all_banques = read_all_banKs(db=db)
  return all_banques



## operation POST
@router.post("/", response_model=BanqueRead)
def create_a_banque(banque: BanqueCreate, db: Session = Depends(get_db)) -> BanqueRead:
    """route pour creer une banque

    Args:
        banque (BanqueCreate): instance d'objet banque a creer
        db (Session, optional): session de la db. Defaults to Depends(get_db).

    Returns:
        BanqueRead: return banque creer
    """

    new_banque = create_banque(banque=banque, db=db)
    return new_banque