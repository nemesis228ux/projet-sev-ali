# Contient le model sqlalchemy de la table compte
from typing import List

from app.core.database import Base
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, DateTime, ForeignKey, Double
from sqlalchemy.sql import func
from enum import Enum

from .transaction import Transaction
from .user import User
from sqlalchemy.orm import relationship


class AccountTypes(str, Enum):
    """Enumartions des types de compte possibles"""

    COURANT = "courant"

    EPARGNE = "epargne"


class Compte(Base):
    """Modèles SQLAlchemy de la table `comptes`"""

    __tablename__ = "comptes"

    id_compte: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    numero_compte: str = Column(  # A revoir en str pour plus de simplicité ou en int
        String,
        unique=True,
        nullable=False,
        index=True
    )

    type_compte: str = Column(
        SqlEnum(AccountTypes),
        default=AccountTypes.COURANT,
        nullable=False
    )

    solde: float = Column(
        Double,
        default=0.0,
        index=True
    )

    date_ouverture: str = Column(
        DateTime,
        default=func.now()
    )

    account_owner_id: int = Column(
        Integer,
        ForeignKey("users.id_user"),
        index=True
    )

    base_user: User = relationship(
        "User",
        back_populates="comptes",
        uselist=False
    )

    transactions: List[Transaction] = relationship(
        "Transaction",
        back_populates="base_account"
    )


    #TODO : Ajouter une relationship pour les cb quand ali aura terminé
