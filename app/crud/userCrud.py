# contient la logque metier des endpoints. 
# ce sont les fonctions qui font les operations souhaiter
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.userSchema import UserUpdate


def get_users(db: Session) -> list[User]:
  """function qui retourne tous les 
  utilisateurs de la database

  Args:
      db (Session): Il prend en argument la base de donnée dans app/core/database.py

  Returns:
      list[User]: return une liste contenant les utilisateurs ou une liste vide mais pas None
  """

  return db.query(User).all()



def get_user_using_id(user_id: int, db: Session) -> User | None:
  """function pour obtenir un user a partir de son id

  Args:
      user_id (int): prend ID de user
      db (Session): prend une session de aussi la db

  Returns:
      User: return le user s'il existe sinon None
  """

  db_user = db.query(User).filter(
    User.id_user == user_id
    ).first()
  return db_user



def get_user_using_email(user_email: str, db: Session) -> User | None:
  """function pour obtenir un user a partir de son email

  Args:
      user_email (int): prend le email de user
      db (Session): prend aussi une session de la db

  Returns:
      User: return le user s'il existe sinon None
  """

  db_user = db.query(User).filter(
    User.email == user_email
    ).first()
  
  return db_user




def update_user_using_email(user_email: str, user_data: UserUpdate, db: Session) -> User | None:
  """function pour mette a jour les infos d'un utilisateur

  Args:
      user_email(str): prend email pour trouver l'utilisateur a mettre a jour
      user_data (UserUpdate): prend les nouvelles données a mettre a jour
      db (Session): prend aussi une session de la db

  Returns:
      User: return le nouvel utilisateur modifier ou None si le user n'existe pas
  """



  db_user = get_user_using_email(user_email=user_email, db=db)
  
  if db_user is None:
    return None

  if user_data.nom_user:
    db_user.nom_user = user_data.nom_user

  if user_data.email:
    db_user.email = user_data.email

  if user_data.adresse:
    db_user.adresse = user_data.adresse

  if user_data.date_naissance:
    db_user.date_naissance = user_data.date_naissance

  if user_data.role:
    db_user.role = user_data.role

  if user_data.id_banque:
    db_user.id_banque = user_data.id_banque

  db.commit() ## commit/save les changements dans le db
  return db_user

  

def delete_user(user_id: int, db: Session) -> User | None:
  """function pour supprimer un utilisateurs

  Args:
      user_id (int): _description_
      db (Session): _description_

  Returns:
      User: return l'utilisateur supprimer ou None s'il n'existe pas 
  """
  
  db_user = get_user_using_id(user_id=user_id, db=db)

  if db_user is not None:
    
    try:
      
      db.delete(db_user)
      db.commit()

    except Exception as e:
      print(f"Exception {e.__class__.__name__}: {e}")

  return db_user
