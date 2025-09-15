from typing import Optional, List

from pydantic import BaseModel

from app.models.transaction import TransactionTypes


class TransactionInit(BaseModel):
    """Modèle d'une requetes pour initier une transaction"""
    account_id: int
    transaction_type: TransactionTypes
    amount: float
    destinator_num_compte: Optional[str]      #À revoir dans le cas des dépot ou retrait


class TransactionActions(BaseModel):
    """Modèle d'une requetes pour effectuer une action (Voir, supprimer, annulé...) sur une transactiion"""
    account_id: int
    transaction_id: int

class TransactionInfo(BaseModel):
    """Modèle de reponse d'une requete de visualisation de transaction"""

    id_transac: int
    initiator_account_id: int
    dest_num_compte: Optional[str]
    type_transac: TransactionTypes
    montant: float
    date_transaction: str

class TransactionsFetch(BaseModel):
    """Modèle d'une requetes pour recuperer toutes les transactions d'un User ou Account"""
    account_id: int

class TransactionViews(BaseModel):
    """Modèle de reponse d'une requete de visualisation de toutes les transactions d'un compte"""

    transactions: Optional[List[TransactionInfo]]

