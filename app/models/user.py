# contient le model sqlalchemy de la table user
from app.core.database import Base
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, Date, ForeignKey
from enum import Enum as UserEnum
from sqlalchemy.orm import relationship
from typing import List

from app.models.banque import Banque
from app.models.compte import Compte


class UserRole(UserEnum):
  
  client = "client"
  admin = "admin"


class User(Base):
  
  __tablename__ = "users"

  id_user: int = Column(Integer, primary_key=True, index=True, nullable=False)
  nom_user: str = Column(String(50), index=True, nullable=False)
  email: str = Column(String(50), index=True, nullable=False)
  hashed_password: str = Column(String(180), index=True, nullable=False)
  adresse: str = Column(String(50), index=True, nullable=False)
  date_naissance: str = Column(Date, index=True, nullable=False)
  role: str = Column(SqlEnum(UserRole), default=UserRole.client, index=True, nullable=False)

  id_banque: int = Column(Integer, ForeignKey("banques.id_banque"), index=True, nullable=False)

  banque : Banque = relationship("Banque", back_populates="users")

  comptes : List[Compte] = relationship(
      "Compte",
      back_populates = "base_user"
  )
