## fichier config.py

import os
from dotenv import load_dotenv

load_dotenv() ## permet de charger les config depuis le fichier .env

SECRET_KEY = os.getenv("SECRET_KEY", "super-cle-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES", 30))