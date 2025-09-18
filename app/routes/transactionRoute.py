from typing import Optional

from fastapi import APIRouter, Query, Depends, Path
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user_id
from app.core.database import get_db
from app.crud.transactionCrud import get_all_transactions_in_bd, get_user_transactions, Transactor, \
    get_user_specific_transaction
from app.models.transaction import TransactionTypes
from app.schemas.transactionSchema import TransactionsView, TransactionsFetch, TransactionView, DepotTransac, \
    RetraitTransac, TransferTransac

router = APIRouter(prefix="/transactions", tags=["transactions"])

#TODO : Penser à sécuriser cette route pour la rendre accessible admin only
@router.get('/all', response_model=TransactionsView)
def get_all_transactions(
        transac_type : Optional[TransactionTypes] = Query(None, description='Param de requete otionnelle pour filtrer les transactions'),
        bd_session : Session = Depends(get_db)
) -> TransactionsView:
    """Route pour obtenir toutes les transactions de la bd"""
    transacs = get_all_transactions_in_bd(bd_session, transac_type)
    return TransactionsView.success_response(transacs)

@router.get("/", response_model=TransactionsView)
def get_user_all_transactions(
    body : TransactionsFetch,
    transac_type : Optional[TransactionTypes] = Query(None, description='Param de requete otionnelle pour filtrer les transactions'),
    user_id : int = Depends(get_current_user_id),
    bd_session : Session = Depends(get_db)
) -> TransactionsView:
    """Route pour obtenir toutes les transactions d'un user"""
    transacs = get_user_transactions(bd_session, user_id, body.account_id, transac_type)
    return TransactionsView.success_response(transacs)

@router.post("/transfert", response_model=TransactionView)
def do_a_transfert(
    body : TransferTransac,
    user_id : int = Depends(get_current_user_id),
    bd_session : Session = Depends(get_db)
) -> TransactionView:
    """Route pour effectuer un transfert"""

    transactor = Transactor(
        bd_session=bd_session,
        initiator_id=user_id,
        iniatior_account_id=body.account_id,
        transaction_type=TransactionTypes.TRANSFERT,
        transaction_amount=body.amount,
        destinator_num_compte=body.destinator_num_compte
    )
    result = transactor.launch_transaction()

    if result.success:      # Reponse de succes si la transac a réussi
        return TransactionView.success_response(result.transac)

    return TransactionView.error_response(result.error)  # La transac n'a pas réussi donc on renvoi une reponse d'erreur

@router.post("/retrait", response_model=TransactionView)
def do_a_retrait(
    body : RetraitTransac,
    user_id : int = Depends(get_current_user_id),
    bd_session : Session = Depends(get_db)
) -> TransactionView:
    """Route pour effectuer un retrait"""

    transactor = Transactor(
        bd_session=bd_session,
        initiator_id=user_id,
        iniatior_account_id=body.account_id,
        transaction_type=TransactionTypes.RETRAIT,
        transaction_amount=body.amount
    )
    result = transactor.launch_transaction()

    if result.success:      # Reponse de succes si la transac a réussi
        return TransactionView.success_response(result.transac)

    return TransactionView.error_response(result.error) # La transac n'a pas réussi donc on renvoi une reponse d'erreur


@router.post("/depot", response_model=TransactionView)
def do_a_depot(
    body : DepotTransac,
    user_id : int = Depends(get_current_user_id),
    bd_session : Session = Depends(get_db)
) -> TransactionView:
    """Route pour effectuer un depot"""

    transactor = Transactor(
        bd_session=bd_session,
        initiator_id=user_id,
        iniatior_account_id=body.account_id,
        transaction_type=TransactionTypes.DEPOT,
        transaction_amount=body.amount
    )
    result = transactor.launch_transaction()

    if result.success:      # Reponse de succes si la transac a réussi
        return TransactionView.success_response(result.transac)

    return TransactionView.error_response(result.error) # La transac n'a pas réussi donc on renvoi une reponse d'erreur

@router.get('/{transac_id}', response_model=TransactionView)
def see_a_transaction(
    transac_id : int = Path(gt=0, description="L'id de la transaction rechechée"),
    account_id : int = Query(..., description="Le numéro de compte de l'user", gt=0),
    user_id : int = Depends(get_current_user_id),
    bd_session : Session = Depends(get_db)
) -> TransactionView:
    """Route pour avoir une transac specifique"""

    transac = get_user_specific_transaction(bd_session, user_id, account_id, transac_id)

    return TransactionView.success_response(transac)