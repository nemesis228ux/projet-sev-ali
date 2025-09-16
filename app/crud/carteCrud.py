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

    account = get_account_by_id(bd_session, user_id, account_id)

    if not account:
        return None

    new_carte = Carte(
        hashed_code_secu=hash_password(password),
        type_carte=type_carte,
        date_expiration=datetime.now() + timedelta(days=365 * 5),
        id_compte=account.id_compte
    )

    while True:
        try:
            new_carte.numero_carte = generate_random_number(size=16)
            bd_session.add(new_carte)
            bd_session.commit()
            break
        except IntegrityError:
            bd_session.rollback()
            continue
        except Exception as e:
            print(f'Exception {e.__class__.__name__} : {e}')
            return None
    bd_session.refresh(new_carte)

    return new_carte

def get_all_cartes(bd_session : Session, type_carte : Optional[CarteTypes]=None) -> Sequence[Carte]:
    query = select(Carte)
    if type_carte:
        # noinspection PyTypeChecker
        query = query.where(Carte.type_carte == type_carte)

    return bd_session.scalars(query).all()

def get_user_cartes(bd_session : Session, user_id : int, type_carte : Optional[CarteTypes]=None) -> List[Carte]:
    cartes: List[Carte] = []
    accounts = get_user_accounts(bd_session, user_id)
    for account in accounts:
        account_cartes = account.cartes
        if account_cartes:
            cartes.extend(account_cartes)

    if type_carte:
        cartes = [carte for carte in cartes if carte.type_carte is type_carte]

    return cartes

def get_user_specific_carte(bd_session : Session, user_id : int, carte_id : int, carte_password : str) -> Optional[Carte]:

    # noinspection PyTypeChecker
    query = select(Carte).where(Carte.id_carte == carte_id)

    carte : Carte | None = bd_session.scalar(query)

    if not carte:
        return None

    if not verify_password(carte_password, carte.hashed_code_secu):
        return None

    if carte.base_account.account_owner_id != user_id:
        return None

    return carte

def delete_user_carte(bd_session :Session, user_id : int, carte_id : int, carte_password : str) -> bool:

    # noinspection PyTypeChecker

    query = select(Carte).where(Carte.id_carte == carte_id)

    carte: Carte | None = bd_session.scalar(query)

    if not carte:
        return False

    if not verify_password(carte_password, carte.hashed_code_secu):
        return False

    if carte.base_account.account_owner_id != user_id:
        return False

    try:
        bd_session.delete(carte)
        bd_session.commit()
        return True
    except Exception as e:
        print(f'Exception {e.__class__.__name__} : {e}')
        return False

def change_carte_password(bd_session :Session, user_id : int, carte_id : int, old_password : str, new_password) -> bool:

    # noinspection PyTypeChecker

    query = select(Carte).where(Carte.id_carte == carte_id)

    carte: Carte | None = bd_session.scalar(query)

    if not carte:
        return False

    if carte.base_account.account_owner_id != user_id:
        return False

    if not verify_password(old_password, carte.hashed_code_secu):
        return False

    carte.hashed_code_secu = hash_password(new_password)
    try:
        bd_session.commit()
        return True
    except Exception as e:
        print(f'Exception {e.__class__.__name__} : {e}')
        return False

