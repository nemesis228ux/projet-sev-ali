### contient les models pydantic
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole
from typing import Optional


class UserBase(BaseModel):
  
  nom_user: str
  email: EmailStr
  adresse: str
  date_naissance: str
  role: UserRole = UserRole.client
  id_banque: int



class UserCreate(UserBase):
  """Model pydantic pr valider le creation d'un user"""
  
  password: str

class UserLogin(BaseModel):
  """Modele pydantic pour valider les données au moment
  du login

  Args:
      BaseModel (_type_): _description_
  """

  nom_user: str
  email: EmailStr
  password: str
  
  

class UserUpdate(BaseModel):
  """Ceci est un model pydantic pr mettre a jour les infos d'un user

  Args:
      BaseModel (Pydantic): valide les données evoyées
  """

  nom_user: Optional[str] = None 
  email: Optional[EmailStr] = None
  adresse: Optional[str] = None
  date_naissance: Optional[str] = None
  role: Optional[UserRole] = None
  id_banque: Optional[int] = None




class UserRead(BaseModel):
  """Model pydantic pour valider la sortie des données pour ue
  requette GET par exemple

  Args:
      BaseModel (_type_): _description_
  """
  
  id_user: int
  nom_user: str
  email: EmailStr
  adresse: str
  date_naissance: str
  role: UserRole = UserRole.client
  id_banque: int
  
  class Config:
    """pr permettre la validati de 
    pydantic en sqlalchemy et vice-versa"""
    orm_mode=True



UserRead.model_rebuild()