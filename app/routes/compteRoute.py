from typing import Optional

from fastapi import APIRouter, Query, Path
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user_id
from app.core.database import get_db
from app.crud.compteCrud import (
    get_accounts,
    create_new_account,
    get_account_by_id,
    get_user_accounts,
    delete_user_account,
)
from app.models.compte import AccountTypes
from app.schemas.compteSchema import (
    AccountsView,
    AccountCreate,
    AccountView,
    ActionResult,
)

router = APIRouter(prefix="/comptes", tags=["comptes"])


# TODO : Penser à sécuriser cette route pour la rendre accessible admin only
@router.get("/all", response_model=AccountsView)
def get_all_accounts(
    account_type: Optional[AccountTypes] = Query(
        None, description="Param de requete otionnelle pour filtrer les comptes"
    ),
    bd_session: Session = Depends(get_db),
) -> AccountsView:
    """Route pour recupérer tous les comptes de la bd"""
    acconts = get_accounts(bd_session, account_type)
    return AccountsView.success_response(acconts.data)


@router.post("/create", response_model=AccountView)
def create_account(
    body: AccountCreate,
    user_id: int = Depends(get_current_user_id),
    bd_session: Session = Depends(get_db),
) -> AccountView:
    """Route pour la création d'un nouveau compte"""
    result = create_new_account(bd_session, body, user_id)

    if result.is_success():
        return AccountView.success_response(result.data)
    return AccountView.error_response(result.error)


@router.get("/", response_model=AccountsView)
def get_user_all_accounts(
    account_type: Optional[AccountTypes] = Query(
        None, description="Param de requete otionnelle pour filtrer les comptes"
    ),
    user_id: int = Depends(get_current_user_id),
    bd_session: Session = Depends(get_db),
) -> AccountsView:
    """Route pour récuperer tous les comptes d'un user"""
    accounts = get_user_accounts(bd_session, user_id, account_type)
    return AccountsView.success_response(accounts.data)


@router.get("/{account_id}", response_model=AccountView)
def get_an_account(
    account_id: int = Path(title="Id du compte recherché"),
    user_id: int = Depends(get_current_user_id),
    bd_session: Session = Depends(get_db),
) -> AccountView:
    """Route pour récuperer des infos sur un compte précis"""
    result = get_account_by_id(bd_session, user_id, account_id)

    if result.is_success():
        return AccountView.success_response(result.data)

    return AccountView.error_response(result.error)


@router.delete("/{account_id}", response_model=ActionResult)
def delete_account(
    account_id: int = Path(title="Id du compte à supprimer"),
    user_id: int = Depends(get_current_user_id),
    bd_session: Session = Depends(get_db),
) -> ActionResult:
    """Route pour supprimer un compte précis"""

    result = delete_user_account(bd_session, user_id, account_id)

    if result.is_success():
        return ActionResult.success_response("Compte supprimé avec succès")

    return ActionResult.error_response(result.error)
