from app.core.database import Base
from sqlalchemy import Column, Integer, Enum as SqlEnum, DateTime, ForeignKey, Double, String
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime

class TransactionTypes(str, Enum):
    TRANSFERT = "transfert"
    DEPOT = "depot"
    RETRAIT = "retrait"

class Transaction(Base):
    """Modèles SQLAlchemy de la table `transactions`"""

    __tablename__ = "transactions"

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
        nullable=True       #NULL en cas de dépotou retrait. Ou soit on remet juste l'id du compte de l'user
    )

    type_transac: TransactionTypes = Column(
        SqlEnum(TransactionTypes),
        index=True,
        nullable=False
    )

    montant: float = Column(
        Double,
        index=True,
        nullable=False
    )

    date_transaction: datetime = Column(
        DateTime,
        default=func.now()
    )

    base_account = relationship(
        "Compte",
        back_populates="transactions",
        uselist=False
    )




