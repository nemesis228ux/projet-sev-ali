# cet fichier excuter une seule fois pour creer les tables dans le database
# avec la powershell : python -m app/create_table ou python -m app/create_table.py

# s'assure aussi que tout les modeles sqlalchemy des tables 
# sont importer avnt d'executer ex: from app.models.user import User

from app.core.database import Base, engine


Base.metadata.create_all(bind=engine)