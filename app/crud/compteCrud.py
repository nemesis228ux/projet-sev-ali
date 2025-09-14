from sqlalchemy.orm import Session
from app.models.compte import Compte, AccountTypes
from typing import Optional, Sequence
from sqlalchemy import select


def get_all_accounts(bd: Session, account_type : Optional[AccountTypes] = None) -> Sequence[Compte]:
    """
    Fonction pour recuperer tous les comptes de la bd, avec possibilité de filtrage par type de compte

    Args :
        bd (Session) : Instance de la bd
        account_type (AccountTypes) : Parametre optionnel pour filtrer les compte par rapport au type

    Returns :
        type : Un tableau de `Compte`
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

    Args :
        bd (Session) : Instance de la bd
        user_id (int) : Id de l'utilisateur recherché
        account_type (AccountTypes) : Parametre optionnel pour filtrer les compte par rapport au type

    Returns :
        type : Un tableau de `Compte`
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

    Args :
        bd (Session) : Instance de la bd
        user_id (int) : Id de l'utilisateur recheché
        account_id (int) : Id du compte recherché

    Returns :
        type : Le compte recherché si trouvé
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

        Args :
            bd (Session) : Instance de la bd
            num_compte (str) : Numero de compte de l'utilisateur recheché

        Returns :
            type : Le compte recherché si trouvé
        """

    # noinspection PyTypeChecker,PydanticTypeChecker
    query = select(Compte).where(
        Compte.numero_compte == num_compte,
    )
    return bd.scalars(query).first()