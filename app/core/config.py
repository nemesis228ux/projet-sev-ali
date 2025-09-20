## fichier config.py

import os
from dotenv import load_dotenv

load_dotenv() ## permet de charger les config depuis le fichier .env
ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")

DATABASE_USER: str = os.getenv("DATABASE_USER", "root")
DATABASE_PILOT: str = os.getenv("DATABASE_PILOT", "pymysql")
DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "mysql")
DATABASE_PASSWORD : str = os.getenv("DATABASE_PASSWORD", "super-cle-secret")
DATABASE_HOST : str = os.getenv("DATABASE_HOST", "localhost")
DATABASE_NAME : str = os.getenv("DATABASE_NAME", "systeme_banque")
SECRET_KEY : str = os.getenv("SECRET_KEY", "super-cle-secret")
ALGORITHM : str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRES_MINUTES : int = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES", 30))
