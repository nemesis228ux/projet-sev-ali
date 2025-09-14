## fichier authCrud pour la logique metier des authentifications
from app.schemas.userSchema import UserCreate
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password


def create_user(user: UserCreate, db: Session) -> User:
  """function pour register un user//add un user

  Args:
      user (UserCreate): prend le user a creer
      db (Session): prend une instance de la database

  Returns:
      User: return le user creer
  """

  hashed_passwd = hash_password(user.password)
  db_user = User(
    **user.model_dump(exclude={"password"}), 
    hashed_password=hashed_passwd
    ) ## on exclu password car ca n'existe pas dans db c'est plutot hashed_password

  db.add(db_user)
  db.commit()
  db.refresh(db_user) ## mettre a jour id_user avant de retourner user

  return db_user