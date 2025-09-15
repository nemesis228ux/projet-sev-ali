## fichier dependencies.py pour avoir le current user et exiger un token 
## ca permettra d'exiger l'authentification pour certaines fonctionalités
from sqlalchemy.orm import Session
from .jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException
from app.models.user import User


## modele de token// url permettant de creer token
oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login") 


def get_current_user(token: str, db: Session):
  """function permettant de return le user actuellement connecter.
  Elle sera utiliser pr securiser certaine routes en exigant le token
  d'authentificatiion obtenu lors du login

  Args:
      token (str): prend le token recu
      db (Session): return les infos de current user si token valide
  """

  claims_data = decode_access_token(token=token)

  if claims_data is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token invalide ou expiré",
      headers={"www-Authenticate": "Bearer"}
    )

  user_id = claims_data.get("sub") ## on avait use user_id pr encoder donc on peut le recuperer ici en str

  if not user_id:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token invalide ou expiré",
      headers={"www-Authenticate": "Bearer"}
    )
    
  user = db.query(User).filter(User.id_user == int(user_id))
  
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Cet utilisateur n'existe pas"
    )

  return user

#TODO: ajouter dependence pour voir si c'est admin ou user simple