from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import (DATABASE_PASSWORD, DATABASE_USER, DATABASE_HOST, DATABASE_NAME,DATABASE_PILOT,
    DATABASE_TYPE, ENVIRONMENT)

# databse url
other_args = ""
pool_class = None
if ENVIRONMENT == "PROD":
    other_args = "?sslmode=require"
    pool_class = NullPool

DATABASE_URL =f"{DATABASE_TYPE}+{DATABASE_PILOT}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}{other_args}"


# configuration du engine
engine = create_engine(DATABASE_URL, echo=True, poolclass=pool_class)

# creation de  Base: classe qui va servir a creer
# les model sqlalchemy et les tables
Base = declarative_base()

## creation d'une session qui va permettre d'interagir avec la db
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


## function get_db qui permet d'acceder/ouvrrir une session avec la db
def get_db():
  db = SessionLocal()

  try:
    """ouvre la session avec db et attend la
    fin de toute operation engagées"""
    yield db

  finally:
    """Et finnalmy ferme la session
    pr eviter fuite des données"""
    db.close()