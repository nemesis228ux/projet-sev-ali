# Contient le model sqlalchemy de la table compte
from app.core.database import Base
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, DateTime, ForeignKey, Double
from sqlalchemy.sql import func
from enum import Enum

from sqlalchemy.orm import relationship

from datetime import datetime


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
        String(16),
        unique=True,
        nullable=False,
        index=True
    )

    type_compte: AccountTypes = Column(
        SqlEnum(AccountTypes),
        default=AccountTypes.COURANT,
        nullable=False
    )

    solde: float = Column(
        Double,
        default=0.0,
        index=True
    )

    date_ouverture: datetime = Column(
        DateTime,
        default=func.now()
    )

    account_owner_id: int = Column(
        Integer,
        ForeignKey("users.id_user"),
        index=True
    )

    base_user = relationship(
        "User",
        back_populates="comptes",
        uselist=False
    )

    transactions = relationship(
        "Transaction",
        back_populates="base_account"
    )

    cartes = relationship(
        "Carte",
        back_populates="base_account",
    )