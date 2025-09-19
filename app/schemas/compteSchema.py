# Modèles Pydantic pour les comptes
from typing import Optional, List

from pydantic import BaseModel, Field
from ..models.compte import AccountTypes
from .baseSchema import ApiBaseResponse
from datetime import datetime

#TODO : Reajuster les modele plus tard en fonction du system d'authentification finale (Token ou user_id brut)

# Modèle d'une requetes pour création de compte
class AccountCreate(BaseModel):
    """Modèle d'une requetes pour création de compte"""
    account_type : AccountTypes
    initial_amount : Optional[float] = 0.0

# Modèle d'une requete pour effectuer une action sur un compte précis
class AccountActions(BaseModel):
    """Modèle d'une requete pour effectuer une action sur un compte précis"""
    account_id : int = Field(..., description="Id du compte sur laquelle l'action doit etre effectuée")

class ActionResult(ApiBaseResponse):
    """Modèle de réponse d'une requete d'action sur un compte"""
    result : Optional[str] = Field(None, description="Le resultat de l'action")

class AccountInfo(BaseModel):
    """Modèle de base d'un compte"""
    id_compte : int
    numero_compte : str
    type_compte : AccountTypes
    solde : float
    date_ouverture : datetime | None = None
    account_owner_id : int

    class Config:
        from_attributes = True

class AccountView(ApiBaseResponse):
    """Modèle de réponse d'une requete d'informations de compte"""

    # Surcharge sur l'attribut result pour pouvoir spécifier la bonne donnée à valider
    result: Optional[AccountInfo] = Field(None, description="Le compte recherché")


class AccountsView(ApiBaseResponse):
    """Modèle de réponse d'une requete d'informations de plusieurs comptes"""

    # Surcharge sur l'attribut result pour pouvoir spécifier la bonne donnée à valider
    result: Optional[List[AccountInfo]] = Field(None, description='Les comptes recherchés')
