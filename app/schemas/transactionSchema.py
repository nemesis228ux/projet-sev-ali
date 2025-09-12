from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from app.models.transaction import TransactionTypes


class TransactionInit(BaseModel):
    """Modèle d'une requetes pour initier une transaction"""
    account_id: int
    transaction_type: TransactionTypes
    amount: float
    destinator_account_id: Optional[int]      #À revoir dans le cas des dépot ou retrait


class TransactionActionTypes(str, Enum):
    """Enumeration des differentes actions possibles sur une transac"""
    STATUS = "status"
    CANCEL = "cancel"
    READ = "read"

class TransactionActions(BaseModel):
    """Modèle d'une requetes pour effectuer une action sur une transactiion"""
    account_id: int
    transaction_id: int
    action: TransactionActionTypes

class TransactionInfo(BaseModel):
    """Modèle de reponse d'une requete de visualisation de transaction"""

    id_transac: int
    initiator_account_id: int
    dest_account_id: Optional[int]
    type_transac: TransactionTypes
    montant: float
    date_transaction: str

class TransactionsFetch(BaseModel):
    """Modèle d'une requetes pour recuperer toutes les transactions d'un User ou Account"""
    account_id: int

class TransactionViews(BaseModel):

    transactions: Optional[List[TransactionInfo]]

