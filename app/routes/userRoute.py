# contient les routes : les endpoints sur user


from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.userSchema import UserRead, UserUpdate
from app.models.user import User
from app.core.database import get_db
from app.crud.userCrud import (
  get_user_using_email, get_user_using_id, get_users, 
  update_user_using_email, delete_user
)
from app.auth.dependencies import get_current_user, isAdmin
from app.schemas.baseSchema import ApiBaseResponse



router = APIRouter(prefix="/users", tags=["users"])


## operation GET all users
@router.get(
  "/", 
  dependencies=[Depends(get_current_user)], 
  response_model=ApiBaseResponse[list[UserRead]]
  )
def get_all_users(db: Session = Depends(get_db)) -> ApiBaseResponse[list[UserRead]]:
  """routes pour avoir tous les utilisateurs"""

  all_users = get_users(db=db)
  return ApiBaseResponse.success_response(all_users)



## operation GET un user a partir de son email

@router.get("/email", dependencies=[Depends(get_current_user)], response_model=ApiBaseResponse[UserRead])
def read_user_by_email(
  search: str = Query(description="Email qui va permettre de trouver user"), 
  db: Session = Depends(get_db)
  ) -> ApiBaseResponse[UserRead]:

  """fucntion avec Query parameter pour rechercher 
  un user a partir de son email"""

  user = get_user_using_email(user_email=search, db=db)

  if user is None:
    return ApiBaseResponse.error_response("Utilisateur non trouvé")

  return ApiBaseResponse.success_response(user)



## operation GET user by id

@router.get("/{user_id}", dependencies=[Depends(get_current_user)], response_model=ApiBaseResponse[UserRead])
def get_user_by_id(
  user_id: int = Path(..., description="ID de user rechercher"), 
  db: Session = Depends(get_db)
  ) -> ApiBaseResponse[UserRead]:
  """Lire un user a partir de son id"""

  user = get_user_using_id(user_id=user_id, db=db)

  if user is None:
   return ApiBaseResponse.error_response("Cet utilisateur n'existe pas")

  return ApiBaseResponse.success_response(user)



## update un user en utilisant son email
@router.put("/", dependencies=[Depends(get_current_user)], response_model=ApiBaseResponse[UserRead])
def update_user_data(
  new_user: UserUpdate, 
  email: Annotated[str, Query(..., description="Email de user a update")], 
  db: Session = Depends(get_db)
  ) -> ApiBaseResponse[UserRead]:
  """Mettre a jour les infos d'un user en connaissant seulement son email par exemple"""

  db_user = update_user_using_email(user_email=email, user_data=new_user, db=db)

  if db_user is None:
    return ApiBaseResponse.error_response("Cet utilisateur n'existe pas")

  return ApiBaseResponse.success_response(db_user)



## operations delete un user a partir de son id
@router.delete("/{user_id}", dependencies=[Depends(isAdmin)], response_model=ApiBaseResponse[str])
def delete_user_by_id(
  user_id: int = Path(..., description="ID de user a supprimer"), 
  db: Session = Depends(get_db)
  ) -> ApiBaseResponse[str]:

  """Supprimer un user a partir de son id"""
   
  deleted_user = delete_user(user_id=user_id, db=db) 

  if deleted_user is None:
    return ApiBaseResponse.error_response("Cet utilisateur n'existe pas")
  
  return ApiBaseResponse.success_response(f"Utisateur {deleted_user.nom_user} supprimé")