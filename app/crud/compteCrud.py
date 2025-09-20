from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud import CRUDResponse
from app.models.compte import Compte, AccountTypes
from app.schemas.compteSchema import AccountCreate
from app.utils.generator import generate_random_number


def create_new_account(
    bd_session: Session, new_account_base: AccountCreate, user_id: int
) -> CRUDResponse[Optional[Compte]]:
    """
    Fonctionn pour ajjouter un utilisateur à la base de données

    Args:
        bd_session: Instance de la bd
        new_account_base: Informations de bases sur le nouveau compte à créer
        user_id: Id de l'user

    Returns:
        type: Le compte crée si l'opération a reussi
    """

    new_account = Compte(
        account_owner_id=user_id,
        solde=new_account_base.initial_amount,
        type_compte=new_account_base.account_type,
    )

    while True:
        try:
            random_num_compte = generate_random_number(
                size=16
            )  # Pour générer un numéro de compte aléatoire
            new_account.numero_compte = random_num_compte
            bd_session.add(new_account)
            bd_session.commit()
            bd_session.refresh(new_account)
            return CRUDResponse.crud_success(new_account)

        except IntegrityError:  # Cas ou le numéro de compte est déja présent
            bd_session.rollback()  # Reset des dernières modifications
            continue

        except Exception as e:
            exc = f"Exception {e.__class__.__name__} : {e}"
            print(exc)
            return CRUDResponse.crud_error(exc)


def delete_user_account(
    bd_session: Session, user_id: int, account_id: int
) -> CRUDResponse[Optional[Compte]]:
    """
    Fonction pour supprimer un compte de la base de donnée

    Args:
        bd_session: Instance de la bd
        user_id: Id de l'utilisateur recheché
        account_id: Id du compte recherché

    Returns:
        type: `True` si l'opération a réussi, `False` sinon
    """
    try:
        account = get_account_by_id(
            bd_session, user_id, account_id
        )  # On recupère le compte à supprimer
        if account.is_error():
            return CRUDResponse.crud_error(account.error)

        # On doit aussi supprimer les cartes liés au compte
        cartes = account.data.cartes
        for carte in cartes:
            bd_session.delete(carte)

        bd_session.delete(account.data)
        bd_session.commit()
        return CRUDResponse.crud_success(account)
    except Exception as e:
        exc = f"Exception {e.__class__.__name__} : {e}"
        print(exc)
        return CRUDResponse.crud_error(exc)


def get_accounts(
    bd_session: Session, account_type: Optional[AccountTypes] = None
) -> CRUDResponse[Sequence[Compte]]:
    """
    Fonction pour recuperer tous les comptes de la bd, avec possibilité de filtrage par type de compte

    Args:
        bd_session: Instance de la bd
        account_type: Parametre optionnel pour filtrer les compte par rapport au type

    Returns:
        type: Un tableau de `Compte`
    """

    query = select(Compte)
    if account_type:
        # noinspection PyTypeChecker
        query = query.where(Compte.type_compte == account_type)

    return CRUDResponse.crud_success(bd_session.scalars(query).all())


def get_user_accounts(
    bd_session: Session, user_id: int, account_type: Optional[AccountTypes] = None
) -> CRUDResponse[Optional[Sequence[Compte]]]:
    """
    Fonction pour recuperer tous les comptes d'un utilisateur spécifique, avec possibilité de filtrage par type de compte

    Args:
        bd_session: Instance de la bd
        user_id: Id de l'utilisateur recherché
        account_type: Parametre optionnel pour filtrer les compte par rapport au type

    Returns:
        type: Un tableau de `Compte`
    """
    # noinspection PyTypeChecker
    query = select(Compte).filter(Compte.account_owner_id == user_id)
    if account_type:
        # noinspection PyTypeChecker
        query = query.where(
            Compte.account_owner_id == user_id, Compte.type_compte == account_type
        )

    return CRUDResponse.crud_success(bd_session.scalars(query).all())


def get_account_by_id(
    bd_session: Session, user_id: int, account_id: int
) -> CRUDResponse[Optional[Compte]]:
    """
    Fonction pour recuperer un compte spécique d'un utilisateur par son user_id

    Args:
        bd_session: Instance de la bd
        user_id: Id de l'utilisateur recheché
        account_id: Id du compte recherché

    Returns:
        type: Le compte recherché si trouvé
    """

    # noinspection PyTypeChecker,PydanticTypeChecker
    query = select(Compte).where(Compte.id_compte == account_id)

    account: Compte = bd_session.scalar(query)
    if not account:
        return CRUDResponse.crud_error("Ce compte n'existe pas")
    if account.account_owner_id != user_id:
        return CRUDResponse.crud_error("Ce compte ne vous appartient pas")

    return CRUDResponse.crud_success(account)


def get_account_by_numero_compte(
    bd_session: Session, num_compte: str
) -> CRUDResponse[Optional[Compte]]:
    """
    Fonction pour recuperer un compte spécique d'un utilisateur par son numero de compte

    Args:
        bd_session (Session): Instance de la bd
        num_compte (str) : Numero de compte de l'utilisateur recheché

    Returns:
        type: Le compte recherché si trouvé
    """

    # noinspection PyTypeChecker,PydanticTypeChecker
    query = select(Compte).where(
        Compte.numero_compte == num_compte,
    )

    account = bd_session.scalar(query)

    if not account:
        return CRUDResponse.crud_error("Ce compte n'existe pas")

    return CRUDResponse.crud_success(account)
