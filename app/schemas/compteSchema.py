# Modèles Pydantic pour les comptes
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel
from ..models.compte import AccountTypes


#TODO : Reajuster les modele plus tard en fonction du system d'authentification finale (Token ou user_id brut)

# Modèle d'une requetes pour création de compte
class AccountCreate(BaseModel):
    """Modèle d'une requetes pour création de compte"""
    user_id : int  #Ou Token
    account_type : AccountTypes
    initial_amount : Optional[float] = 0.0


# Modèle d'une requetes pour recuperer les différents comptes d'un User
class AccountsFetchRequest(BaseModel):
    """Modèle d'une requetes pour recuperer les différents comptes d'un User"""
    user_id : int
    token : str  # À voir après si ça va fonctionner comme ça


class AccountActionTypes(str, Enum):
    """Enumeration des actions possibles sur un compte"""
    READ = "read"
    DELETE = "delete"


# Modèle d'une requete pour effectuer une action sur un compte précis
class AccountActions(BaseModel):
    user_id : int
    account_id : int
    token : str  #À revoir toujours
    action : AccountActionTypes


# Modèle de réponse d'une requete d'informations de compte
class AccountInfo(BaseModel):
    """Modèle de réponse d'une requete d'informations de compte"""
    id_compte : int
    numero_compte : str
    type_compte : AccountTypes
    solde : float
    date_ouverture : str


# Modèle de réponse d'une requetes d'obtentions de comptes
class AccountsView(BaseModel):
    """Modèle de réponse d'une requetes d'obtentions de comptes"""
    accounts : List[AccountInfo] | None  # À revoir si ce n'est pas trop lourd
