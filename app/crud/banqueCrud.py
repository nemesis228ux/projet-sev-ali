## Logique metier por banque
from sqlalchemy.orm import Session
from app.models.banque import Banque
from app.schemas.banqueSchema import BanqueCreate

def create_banque(banque: BanqueCreate, db: Session) -> Banque:
  """function pour créer une banque

  Args:
      banque (BanqueCreate): prend une instance d'objet BanqueCreate
      db (Session): prend une session de la database

  Returns:
      Banque: return l'isntance d'objet banque créer
  """

  db_banque = Banque(**banque.model_dump()) ## permet de creer une instance d'objet Banque // model sqlalchemy

  db.add(db_banque)
  db.commit()
  db.refresh(db_banque) ## mettre a jour id_banque avant de retourner l'objet

  return db_banque



def read_all_banKs(db: Session) -> list[Banque]:
  """function pour return toutes les banque en meme 
  temps vu que c'est une seul banque

  Args:
      db (Session): prend une session de la database

  Returns:
      list[Banque]: return une liste des banques ou une liste vide
  """
  
  return db.query(Banque).all()
  
  


