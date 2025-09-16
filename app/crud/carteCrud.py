from sqlalchemy.orm import Session

from app.crud.compteCrud import get_account_by_id, get_user_accounts
from app.models.carte import Carte, CarteTypes
from typing import Optional, Sequence, List
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.utils.generator import generate_random_number
from app.utils.security import hash_password, verify_password
from datetime import datetime, timedelta

#TODO: Rajouter des essages d'erreurs clairs après
def create_new_carte(
    bd_session : Session, user_id : int, account_id : int, type_carte : CarteTypes, password : str
) -> Optional[Carte]:
    """
    Fonction pour créer une new carte sur un compte d'un user

    Args:
        bd_session: Insatance de la bd
        user_id: Id de l'user
        account_id: Id du compte
        type_carte: Le type de carte
        password: Le mdp de la nouvelle carte

    Returns:
        Optional[Carte] : La carte si la création a réussi

    """

    account = get_account_by_id(bd_session, user_id, account_id)    # On essaye de récup le compte

    if not account:     # Compte inexistant
        return None

    new_carte = Carte(
        hashed_code_secu=hash_password(password),       # mdp hashé dans la bd
        type_carte=type_carte,
        date_expiration=datetime.now() + timedelta(days=365 * 5),       # Validité de 5 ans par défaut
        id_compte=account.id_compte
    )

    while True:
        try:
            new_carte.numero_carte = generate_random_number(size=16)     # On génère un numéro aléatoire et unique
            bd_session.add(new_carte)
            bd_session.commit()
            break

        except IntegrityError:      # Cas ou le numéro de carte existe déja
            bd_session.rollback()   # On reset tout et on essaye un autre numéro
            continue

        except Exception as e:
            print(f'Exception {e.__class__.__name__} : {e}')
            return None

    bd_session.refresh(new_carte)

    return new_carte

def get_all_cartes(bd_session : Session, type_carte : Optional[CarteTypes]=None) -> Sequence[Carte]:
    """
    Fonction pour obtenir toutes les cartes de la bd, avec possibilité de filtrage

    Args:
        bd_session: Instance de la bd
        type_carte: Paramètre optionnel pour filtrer le résultat par rapport à au type de carte

    Returns:
        Sequence[Carte] : La liste des cartes recherchées
    """

    query = select(Carte)
    if type_carte:      # On filtre si on doit filtrer
        # noinspection PyTypeChecker
        query = query.where(Carte.type_carte == type_carte)

    return bd_session.scalars(query).all()

def get_user_cartes(bd_session : Session, user_id : int, type_carte : Optional[CarteTypes]=None) -> List[Carte]:
    """
    Fonction pour récuperer les cartes d'un utilisateur, avec possibilité de filtrage
    Args:
        bd_session: Instance de la bd
        user_id: Id de l'user
        type_carte: Parametre optionnel pour filtrer les resultats par rapport aux types de carte, si non passé la func
            renvoi toutes les cartes de l'user

    Returns:
        List[Carte] : La liste des cartes recherchées
    """

    #TODO: Chercher une autre approche plus rapide apreès, passer directement par requete sql
    cartes: List[Carte] = []
    accounts = get_user_accounts(bd_session, user_id)       # On récupère tous les comptes de l'user

    # On itère sur les comptes pour récuperer les cartes
    for account in accounts:
        account_cartes = account.cartes
        if account_cartes:      # On ajoute les cartes si présentes
            cartes.extend(account_cartes)

    if type_carte:      # On filtre si on doit filtrer
        cartes = [carte for carte in cartes if carte.type_carte is type_carte]

    return cartes

def get_user_specific_carte(bd_session : Session, user_id : int, carte_id : int, carte_password : str) -> Optional[Carte]:
    """
    Fonction pour récuperer une carte spécifique d'un utilisateur
    Args:
        bd_session: Instance de la bd
        user_id: Id de l'user
        carte_id: Id de la carte
        carte_password: Mdp de la carte

    Returns:
        Optional[Carte] : La carte si elle est trouvé, None sinon
    """

    # noinspection PyTypeChecker
    query = select(Carte).where(Carte.id_carte == carte_id)     # Requete

    carte : Carte | None = bd_session.scalar(query)             #Execution de la requete

    if not carte:
        return None     # Carte non trouvé

    if not verify_password(carte_password, carte.hashed_code_secu):     # On vérifie le mdp donné par l'user
        return None

    if carte.base_account.account_owner_id != user_id:          # On vérifie si la carte appartient bien à l'user
        return None

    return carte

def delete_user_carte(bd_session :Session, user_id : int, carte_id : int, carte_password : str) -> bool:
    """
    Fonction pour supprimer une carte spécifique d'un utilisateur
    Args:
        bd_session: Instance de la bd
        user_id: Id de l'user
        carte_id: Id de la carte
        carte_password: Mdp de la carte

    Returns:
        bool : True si la carte est supprimé, False sinon
    """
    # noinspection PyTypeChecker

    query = select(Carte).where(Carte.id_carte == carte_id)         # Requete

    carte: Carte | None = bd_session.scalar(query)                  # Execution de la requete

    if not carte:
        return False        #Carte inexistante

    if not verify_password(carte_password, carte.hashed_code_secu):     # Vérification du mdp
        return False

    if carte.base_account.account_owner_id != user_id:                # On vérifie si la carte appartient bien à l'user
        return False

    try:
        bd_session.delete(carte)        # Suppression effective de la carte
        bd_session.commit()
        return True
    except Exception as e:
        print(f'Exception {e.__class__.__name__} : {e}')
        return False

def change_carte_password(bd_session :Session, user_id : int, carte_id : int, old_password : str, new_password : str) -> bool:
    """
    Fonction pour changer le mot de passe d'une carte spécifique d'un utilisateur
    Args:
        bd_session: Instance de la bd
        user_id: Id de l'user
        carte_id: Id de la carte
        old_password: Ancien mdp de la carte
        new_password: Nouveau mdp de la carte

    Returns:
        bool : True si le mdp est changé, False sinon
    """

    # noinspection PyTypeChecker
    query = select(Carte).where(Carte.id_carte == carte_id)         # Requete

    carte: Carte | None = bd_session.scalar(query)                  # Execution de la requete

    if not carte:
        return False            # Carte inexistante

    if carte.base_account.account_owner_id != user_id:          # On vérifie si la carte appartient bien à l'user
        return False

    if not verify_password(old_password, carte.hashed_code_secu):   # On vérifie si le mdp est correct
        return False

    carte.hashed_code_secu = hash_password(new_password)        # Mise à jour du mdp de la carte
    try:
        bd_session.commit()                             # Commit des changements
        return True
    except Exception as e:
        print(f'Exception {e.__class__.__name__} : {e}')
        return False

