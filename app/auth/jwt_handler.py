## fichierr jwt_handler pour creer et decoder access token

from datetime import datetime, timedelta, UTC
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRES_MINUTES
from jose import jwt, JWTError



def create_access_token(data_to_encode: dict, expire_delta: timedelta | None) -> str | dict[str, JWTError]:
  """function pour generer un access token

  Args:
      data_to_encode (dict): contient la donnée de l'utilisateur qu'on 
      use pour coder le token: ex: {"sub": user_id} 

      expire_delta (timedelta): le temps avant l'expiration du token. 
      si c'est None alors on prendre un par defaut

  Returns:
      str: retourne un str qui contient le token creer
  """

  to_encode = data_to_encode.copy()  ## on realise une copy des elements avec lesquels on veut travailler

  expiration = datetime.now(UTC) + (        #L'autre methode etait deprecated
    expire_delta  or timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
  ) ## donc ici on prend l'heure actuel + la durée du token pour avoir l'heure d'expiration

  to_encode.update({"exp": expiration}) ## met a jour pour ajouter une noyvelle info: le tmps d'expiration du token

  try:

    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
  
  except JWTError as err:
    return {"message": err}



def decode_access_token(token: str) -> dict | None:
  """function pour decoder le token et verifier si le token
  est toujours valid: le user_id et expiration 

  Args:
      token (str): Il prend en argument le token generer en str

  Returns:
      dict | None: retourne un dict qui contient les infos utiliser au debut pour
      creer le token si toutes les données sont valid sinon retourne None dans le cas contraire
  """

  try:
    
    claims_data = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    return claims_data 

  except JWTError:
    return None