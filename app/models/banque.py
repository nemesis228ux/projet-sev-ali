## banque.py pour gerer le model sqlalchemy de la table banques
from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class Banque(Base):

    __tablename__ = "banques"

    id_banque: int = Column(Integer, primary_key=True, index=True, nullable=False)
    nom_banque: str = Column(String(50), index=True, nullable=False)
    adresse: str = Column(String(50), index=True, nullable=False)

    users = relationship("User", back_populates="banque")
