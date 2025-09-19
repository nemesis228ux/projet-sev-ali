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


router = APIRouter(prefix="/users", tags=["users"])


## operation GET all users
@router.get("/", dependencies=[Depends(get_current_user)], response_model=list[UserRead])
def get_all_users(db: Session = Depends(get_db)) -> list[UserRead]:
  """routes pour avoir tous les utilisateurs"""

  all_users = get_users(db=db)
  return all_users



## operation GET un user a partir de son email

@router.get("/email", dependencies=[Depends(get_current_user)], response_model=UserRead)
def read_user_by_email(
  search: str = Query(description="Email qui va permettre de trouver user"), 
  db: Session = Depends(get_db)
  ) -> UserRead:

  """fucntion avec Query parameter pour rechercher 
  un user a partir de son email"""

  user = get_user_using_email(user_email=search, db=db)

  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Cet utilisateur n'existe pas"
    )

  return user



## operation GET user by id

@router.get("/{user_id}", dependencies=[Depends(get_current_user)], response_model=UserRead)
def get_user_by_id(
  user_id: int = Path(..., description="ID de user rechercher"), 
  db: Session = Depends(get_db)
  ) -> UserRead:
  """Lire un user a partir de son id"""

  user = get_user_using_id(user_id=user_id, db=db)

  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Cet utilisateur n'existe pas"
    )

  return user



## update un user en utilisant son email
@router.put("/", dependencies=[Depends(get_current_user)], response_model=UserRead)
def update_user_data(
  new_user: UserUpdate, 
  email: Annotated[str, Query(..., description="Email de user a update")], 
  db: Session = Depends(get_db)
  ) -> UserRead:
  """Mettre a jour les infos d'un user en connaissant seulement son email par exemple"""

  db_user = update_user_using_email(user_email=email, user_data=new_user, db=db)

  if db_user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Cet utilisateur n'existe pas"
    )

  return db_user



## operations delete un user a partir de son id
@router.delete("/{user_id}", dependencies=[Depends(isAdmin)], response_model=dict[str, str])
def delete_user_by_id(
  user_id: int = Path(..., description="ID de user a supprimer"), 
  db: Session = Depends(get_db)
  ) -> dict[str, str]:

  """Supprimer un user a partir de son id"""
   
  deleted_user = delete_user(user_id=user_id, db=db) 

  if deleted_user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Cet utilisateur n'existe pas"
    )
  
  return {"message": f"Utisateur {deleted_user.nom_user} supprimé"}