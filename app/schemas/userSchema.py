### contient les models pydantic
from pydantic import BaseModel, EmailStr, str
from app.models.user import UserRole
from typing import Optional


class UserBase(BaseModel):
  
  nom_user: str
  email: EmailStr
  addresse: str
  date_naissance: str
  role: UserRole = UserRole.client
  id_banque: int


class UserCreate(UserBase):
  
  password: str



class UserUpdate(BaseModel):

  nom_user: Optional[str] = None 
  email: Optional[EmailStr] = None
  addresse: Optional[str] = None
  date_naissance: Optional[str] = None
  role: Optional[UserRole] = None
  id_banque: Optional[int] = None



class UserRead(BaseModel):
  
  id_user: int
  nom_user: str
  email: EmailStr
  addresse: str
  date_naissance: str
  role: UserRole = UserRole.client
  id_banque: int
  
  class Config:
    """pr permettre la validati de 
    pydantic en sqlalchemy et vice-versa"""
    orm_mode=True



UserRead.model_rebuild()