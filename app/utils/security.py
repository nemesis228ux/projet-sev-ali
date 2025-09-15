# creer les fonctions pour le hashage

from passlib.context import CryptContext


## creation du context de hashage

pwd_context = CryptContext(schemes=("bcrypt"), deprecated="auto") ## bcrypt est le type d'algorithme pour le hashage



def hash_password(password: str) -> str:
  """function pour hasher les mots de pass utilisateur dans 
   base de donnée

  Args:
      password (str): mot de passe claire soumis par le user

  Returns:
      str: retourne un mot de passe crypter: c'est un str
  """
  return pwd_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
  """function pour verifier le mot de passe lors de login

  Args:
      plain_password (str): c'est le mot de pass en clair fourni lors du login
      hashed_password (str):c'est le  mot de pass crypter qui se trouve dans la database

  Returns:
      bool: retourn true si ca match sinon false si les mots de passe sont differents
  """

  return pwd_context.verify(plain_password, hashed_password)