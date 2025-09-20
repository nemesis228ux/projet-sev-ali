from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.models.transaction import TransactionTypes
from .baseSchema import ApiBaseResponse

NUM_COMPTE_PATTERN = r"^\d{16}$"  # Regex pour valider les numéros de comptes


class TransactionBase(BaseModel):
    """Modèle d'une requetes pour initier une transaction"""

    account_id: int
    amount: float = Field(..., description="La valeur de la transaction", gt=0)


class TransferTransac(TransactionBase):
    """Modele d'une requete de transfert"""

    destinator_num_compte: str = Field(..., pattern=NUM_COMPTE_PATTERN)


class RetraitTransac(TransactionBase):
    """Modele d'une requete de retrait"""

    pass


class DepotTransac(TransactionBase):
    """Modele d'une requete de depot"""

    pass


class TransactionsFetch(BaseModel):
    """Modèle d'une requetes pour recuperer toutes les transactions d'un Account"""

    account_id: int


class TransactionInfo(BaseModel):
    """Modèle de reponse d'une requete de visualisation de transaction"""

    id_transac: int
    initiator_account_id: Optional[int] = (
        None  # Ce champ peut ne pas exister si on supprime le compte initiateur
    )
    dest_num_compte: Optional[str] = None
    type_transac: TransactionTypes
    montant: float
    date_transaction: datetime = None

    class Config:
        from_attributes = True


class TransactionResult(BaseModel):
    """Modèle de base d'une transaction"""

    success: bool
    error: Optional[str] = None
    transac: Optional[TransactionInfo] = None


class TransactionView(ApiBaseResponse):
    """Modèle de reponse d'une requete de visualisation d'une seule transaction"""

    # Surcharge sur l'attribut result pour pouvoir spécifier la bonne donnée à valider
    result: Optional[TransactionInfo] = None


class TransactionsView(ApiBaseResponse):
    """Modèle de reponse d'une requete de visualisation de toutes les transactions d'un compte"""

    # Surcharge sur l'attribut result pour pouvoir spécifier la bonne donnée à valider
    result: Optional[List[TransactionInfo]] = None
