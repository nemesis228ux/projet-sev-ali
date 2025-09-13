from app.core.database import Base
from sqlalchemy import Column, Integer, Enum as SqlEnum, DateTime, ForeignKey, Double, String
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy.orm import relationship

from app.models.compte import Compte


class TransactionTypes(str, Enum):
    TRANSFERT = "transfert"
    DEPOT = "depot"
    RETRAIT = "retrait"

class Transaction(Base):
    """Modèles SQLAlchemy de la table `transactions`"""

    __tablename__ = "transctions"

    id_transac: int = Column(
        Integer,
        primary_key=True,
        index=True
    )

    initiator_account_id: int = Column(
        Integer,
        ForeignKey("comptes.id_compte"),
        index=True
    )

    dest_num_compte: str = Column(
        String(16),
        index=True,
        nullable=True       #NULL en cas de dépotou retrait. Ou soit on remet juste l'id du compte du user
    )

    type_transac: str = Column(
        SqlEnum(TransactionTypes),
        index=True,
        nullable=False
    )

    montant: float = Column(
        Double,
        index=True,
        nullable=False
    )

    date_transaction: str = Column(
        DateTime,
        default=func.now()
    )

    base_account: Compte = relationship(
        "Compte",
        back_populates="transactions",
        uselist=False
    )




