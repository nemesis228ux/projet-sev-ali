from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.models.carte import CarteTypes
from .baseSchema import ApiBaseResponse


class CarteBase(BaseModel):
    account_id: int
    carte_type: CarteTypes


class CreateCarte(CarteBase):
    """Modèle d'une requete initier la création d'une carte"""

    password: str


class ChangeCartePassword(BaseModel):
    """Modèle d'une requete pour changer le mdp d'une carte"""

    carte_id: int
    old_password: str
    new_password: str


class CarteInfo(BaseModel):
    """Modèle de réponses d'obtentions d'infos sur une carte précise"""

    id_carte: int
    numero_carte: str
    type_carte: CarteTypes
    date_expiration: datetime
    id_compte: int

    class Config:
        from_attributes = True


class CarteView(ApiBaseResponse):
    """Modèle de réponse d'une requete d'informations de carte"""

    # Surcharge sur l'attribut result pour pouvoir spécifier la bonne donnée à valider
    result: Optional[CarteInfo] = Field(None, description="La carte recherchée")


class CartesView(ApiBaseResponse):
    """Modèle de réponse d'une requete d'informations de plusieurs cartes"""

    # Surcharge sur l'attribut result pour pouvoir spécifier la bonne donnée à valider
    result: Optional[List[CarteInfo]] = Field(
        None, description="Les cartes recherchées"
    )
