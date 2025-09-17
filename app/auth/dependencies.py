## fichier dependencies.py pour avoir le current user et exiger un token 
## ca permettra d'exiger l'authentification pour certaines fonctionalités
from sqlalchemy.orm import Session
from .jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends
from app.models.user import User, UserRole
from typing import Annotated
from app.core.database import get_db


## modele de token// url permettant de creer token
oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login") ## indique ou trouver le token


def get_current_user(token: Annotated[str, Depends(oauth_schema)], db: Session = Depends(get_db)) -> User:
  """function permettant de return le user actuellement connecter.
  Elle sera utiliser pr securiser certaine routes en exigant le token
  d'authentificatiion obtenu lors du login


  Args:
      token (Annotated[str, Depends): Extait directement le token dans le Header avec Bearer
      db (Session): Une session de la db

  Raises:
      HTTPException: Token invalide ou expiré
      HTTPException: Token invalide ou expiré
      HTTPException: Cet utilisateur n'existe pas

  Returns:
      User: return un objet User qui est les infos de user actuellement connecter  
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
    
  user = db.query(User).filter(User.id_user == int(user_id)).first()
  
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Cet utilisateur n'existe pas"
    )

  return user




def isAdmin(current_user: User = Depends(get_current_user)) -> User:
  """function pour restraindre les accès uniquement aux admis

  Args:
      current_user (User, optional): recuperere les infos de current_user. Defaults to Depends(get_current_user).

  Raises:
      HTTPException: lever une exection si c'est pas un admin

  Returns:
      User: return tjrs les infos de current_user
  """

  if current_user.role != UserRole.admin :
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Accès reservé uniquement aux administrateurs"
    )
    
  return current_user

  