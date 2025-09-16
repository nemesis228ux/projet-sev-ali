from app.core.database import Base
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, DateTime, ForeignKey
from enum import Enum

from sqlalchemy.orm import relationship
from datetime import datetime
class CarteTypes(str, Enum):
    VISA = "visa"
    MASTERCARD = "mastercard"
    AUTRE = "autre"

class Carte(Base):
    """Modèles SQLAlchemy de la table `cartes_bancaires`"""
    __tablename__ = 'cartes_bancaires'

    id_carte : int = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    numero_carte : str = Column(
        String(16),
        index=True,
        nullable=False,
        unique=True
    )

    hashed_code_secu : str = Column(
        String(255),
        index=True,
        nullable=False
    )

    type_carte : CarteTypes = Column(
        SqlEnum(CarteTypes),
        nullable=False
    )

    date_expiration : datetime = Column(
        DateTime,
        nullable=False,
        index=True
    )

    id_compte :  int = Column(
        Integer,
        ForeignKey("comptes.id_compte"),
        index=True
    )

    base_account = relationship(
        "Compte",
        back_populates='cartes',
        uselist=False
    )
