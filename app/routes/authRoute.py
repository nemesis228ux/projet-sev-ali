from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.userSchema import UserCreate, UserRead, UserLogin
from app.core.database import get_db
from app.crud.authCrud import create_user
from app.models.user import User
from app.auth.jwt_handler import create_access_token
from app.utils.security import verify_password



router = APIRouter(prefix="/auth", tags=["auth"])


## operation pour creer un user
@router.post("/register", response_model=UserRead)
def register_new_user(
  user: UserCreate, 
  db: Session = Depends(get_db) ) -> UserRead:

  """Route /auth/register pour enregistrer/creer un utisateur"""

  created_user = create_user(user=user, db=db)
  return created_user



## operation pour se connecter/login
@router.post("/login", response_model=dict[str, str])
def user_login( login_user: UserLogin, db: Session = Depends(get_db) ) -> dict[str, str] :
  """function login pour authentifié l'utilisateur et 
  generer un token d'authentification

  Args:
      user (UserLogin): prend les infos de connexion
      db (Session, optional): prend aussi une session la database. Defaults to Depends(get_db).

  Returns:
      dict[str, str]: _description_
  """

  db_user = db.query(User).filter(User.nom_user == login_user.nom_user).first()

  if not db_user or not verify_password(plain_password=login_user.password, hashed_password=db_user.hashed_password):
    raise HTTPException(
      status_code=404,
      detail="Urilisateur non trouvé"
    )
    
  token = create_access_token({"sub": str(db_user.id_user)})

  return {"access_token": token, "token_type": "Bearer"}