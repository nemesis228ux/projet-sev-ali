from sqlalchemy.orm import Session
from app.models.compte import Compte, AccountTypes
from app.schemas.compteSchema import AccountCreate
from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from app.models import add_all_tables
add_all_tables()

def create_new_account(bd : Session, new_account_base : AccountCreate) -> Optional[Compte]:
    """
    Fonctionn pour ajjouter un utilisateur à la base de données

    Args:
        bd: Instance de la bd
        new_account_base: Informations de bases sur le nouveau compte à créer

    Returns:
        type: Le compte crée si l'opération a reussi
    """

    new_account = Compte(
        account_owner_id=new_account_base.user_id,
        solde=new_account_base.initial_amount,
        type_compte=new_account_base.account_type
    )

    while True:
        try:
            random_num_compte = uuid4().int.__str__()[:16]      # Pour générer un numéro de compte aléatoire
            new_account.numero_compte = random_num_compte
            bd.add(new_account)
            bd.commit()
            bd.refresh(new_account)
            return new_account

        except IntegrityError:      # Cas ou le numéro de compte est déja présent
            bd.rollback()
            new_account.numero_compte = uuid4().int.__str__()[:16]
            continue

        except Exception as e:
            print(f'Exception {e.__class__.__name__} : {e}')
            break

def delete_user_account(bd : Session, user_id : int, account_id : int) -> bool:
    """
    Fonction pour supprimer un compte de la base de donnée

    Args:
        bd: Instance de la bd
        user_id: Id de l'utilisateur recheché
        account_id: Id du compte recherché

    Returns:
        type: `True` si l'opération a réussi, `False` sinon
    """
    try:
        account = get_account_by_id(bd, user_id, account_id)    # On recupère le compte à supprimer
        if not account:
            return False

        bd.delete(account)
        bd.commit()
        return True
    except Exception as e:
        print(f'Exception {e.__class__.__name__} : {e}')
        return False

def get_all_accounts(bd: Session, account_type : Optional[AccountTypes] = None) -> Sequence[Compte]:
    """
    Fonction pour recuperer tous les comptes de la bd, avec possibilité de filtrage par type de compte

    Args:
        bd: Instance de la bd
        account_type: Parametre optionnel pour filtrer les compte par rapport au type

    Returns:
        type: Un tableau de `Compte`
    """

    query = select(Compte)
    if account_type:
        # noinspection PyTypeChecker
        query = query.where(
            Compte.type_compte == account_type
        )

    return bd.scalars(query).all()

def get_user_accounts(
        bd : Session,
        user_id : int,
        account_type : Optional[AccountTypes] = None
) -> Optional[Sequence[Compte]]:
    """
    Fonction pour recuperer tous les comptes d'un utilisateur spécifique, avec possibilité de filtrage par type de compte

    Args:
        bd: Instance de la bd
        user_id: Id de l'utilisateur recherché
        account_type: Parametre optionnel pour filtrer les compte par rapport au type

    Returns:
        type: Un tableau de `Compte`
    """
    # noinspection PyTypeChecker
    query = select(Compte).filter(
        Compte.account_owner_id == user_id
    )
    if account_type:
        # noinspection PyTypeChecker
        query = query.where(
            Compte.account_owner_id == user_id,
            Compte.type_compte == account_type
        )

    return bd.scalars(query).all()

def get_account_by_id(bd : Session, user_id : int, account_id : int) -> Optional[Compte]:
    """
    Fonction pour recuperer un compte spécique d'un utilisateur par son user_id

    Args:
        bd: Instance de la bd
        user_id: Id de l'utilisateur recheché
        account_id: Id du compte recherché

    Returns:
        type: Le compte recherché si trouvé
    """

    # noinspection PyTypeChecker,PydanticTypeChecker
    query = select(Compte).where(
        Compte.account_owner_id == user_id,
        Compte.id_compte == account_id
    )
    return bd.scalars(query).first()

def get_account_by_numero_compte(bd : Session, num_compte : str) -> Optional[Compte]:
    """
    Fonction pour recuperer un compte spécique d'un utilisateur par son numero de compte

    Args:
        bd (Session): Instance de la bd
        num_compte (str) : Numero de compte de l'utilisateur recheché

    Returns:
        type: Le compte recherché si trouvé
    """

    # noinspection PyTypeChecker,PydanticTypeChecker
    query = select(Compte).where(
        Compte.numero_compte == num_compte,
    )
    return bd.scalars(query).first()