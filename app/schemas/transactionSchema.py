from typing import Optional, List

from pydantic import BaseModel

from app.models.transaction import TransactionTypes


class TransactionInit(BaseModel):
    """Modèle d'une requetes pour initier une transaction"""
    user_id: int
    account_id: int
    transaction_type: TransactionTypes
    amount: float
    destinator_num_compte: Optional[str] = None      #À revoir dans le cas des dépot ou retrait


class TransactionActions(BaseModel):
    """Modèle d'une requetes pour effectuer une action (Voir, supprimer, annulé...) sur une transactiion"""
    user_id: int
    account_id: int
    transaction_id: int

class TransactionResult(BaseModel):
    """Modèle de reponse d'une requete de transaction"""
    success : bool
    error : Optional[str] = None

class TransactionInfo(BaseModel):
    """Modèle de reponse d'une requete de visualisation de transaction"""

    id_transac: int
    initiator_account_id: int
    dest_num_compte: Optional[str] = None
    type_transac: TransactionTypes
    montant: float
    date_transaction: str

class TransactionsFetch(BaseModel):
    """Modèle d'une requetes pour recuperer toutes les transactions d'un User ou Account"""
    user_id: int
    account_id: int

class TransactionViews(BaseModel):
    """Modèle de reponse d'une requete de visualisation de toutes les transactions d'un compte"""

    transactions: Optional[List[TransactionInfo]] = None

