## modeles pydantics pour banque
from pydantic import BaseModel
from typing import Optional


class BanqueCreate(BaseModel):
  
  nom_banque: str
  adresse: str


class BanqueUpdate(BaseModel):
  
  nom_banque: Optional[str] = None
  adresse: Optional[str] = None


class BanqueRead(BaseModel):
  
  id_banque: int
  nom_banque: str
  adresse: str
  
  class Config:
    orm_mode=True