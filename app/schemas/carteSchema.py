from pydantic import BaseModel

from app.models.carte import CarteTypes


class CarteBase(BaseModel):
    account_id: int
    carte_type: CarteTypes

class CreateCarte(CarteBase):
    """Modèle d'une requete initier la création d'une carte"""
    password: str

class CarteAction(CarteBase):
    """Modèle d'une requete pour effectuer une action sur une carte précise"""
    password: str
    carte_id: int

class CarteInfo(CarteBase):
    """Modèle de réponses d'obtentions d'infos sur une carte précise"""
    id_carte : int
    numero_carte: str
    type_carte: CarteTypes
    date_expiration: str

