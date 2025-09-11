from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# databse url
user="root"
password=""
host="localhost"
db_name="systeme_banque"

DATABASE_URL =f"mysql+pymysql://{user}:{password}@{host}/{db_name}"


# configuration du engine
engine = create_engine(DATABASE_URL, echo=True)

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