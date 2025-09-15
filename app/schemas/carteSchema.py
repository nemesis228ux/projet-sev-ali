from pydantic import BaseModel

from app.models.carte import CarteTypes


class CreateCarte(BaseModel):
    """Modèle d'une requete initier la création d'une carte"""
    account_id : int
    carte_type : CarteTypes

class CarteAction(BaseModel):
    """Modèle d'une requete pour effectuer une action sur une carte précise"""
    account_id: int
    carte_id: int

class CarteInfo(BaseModel):
    """Modèle de réponses d'obtentions d'infos sur une carte précise"""
    id_carte : int
    numero_carte: str
    type_carte: CarteTypes
    date_expiration: str

