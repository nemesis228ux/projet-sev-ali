## modeles pydantics pour banque
from typing import Optional

from pydantic import BaseModel


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
        orm_mode = True
