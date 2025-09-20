from typing import Optional

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user_id
from app.core.database import get_db
from app.models.carte import CarteTypes
from app.schemas.carteSchema import CartesView, CarteView, CreateCarte, ChangeCartePassword
from app.schemas.baseSchema import ApiBaseResponse
from fastapi import APIRouter, Query, Path
from app.crud.carteCrud import (get_all_cartes, create_new_carte, get_user_cartes, get_user_cartes_in_an_account,
    get_user_specific_carte, delete_user_carte, change_carte_password
)

# TODO: Essayer de mettre des messages d'erreurs clairs
router = APIRouter(prefix='/cartes', tags=['cartes'])

@router.get('/all', response_model=CartesView)
def get_all_cartes_in_bd(
    carte_type : Optional[CarteTypes] = Query(None, description='Param de requete otionnelle pour filtrer les comptes'),
    bd_session : Session = Depends(get_db)
) -> CartesView:
    """Route pour obtenir toutes les cartes de la bd"""

    cartes = get_all_cartes(bd_session, carte_type)

    return CartesView.success_response(cartes)

@router.post('/create', response_model=CarteView)
def create_a_new_carte(
    body : CreateCarte,
    user_id: int = Depends(get_current_user_id),
    bd_session : Session = Depends(get_db)
) -> CarteView:
    """Route pour créer une nouvelle carte"""

    new_carte = create_new_carte(bd_session, user_id, body.account_id, body.carte_type, body.password)

    return CarteView.success_response(new_carte)

@router.get('/', response_model=CartesView)
def get_user_all_cartes(
    carte_type: Optional[CarteTypes] = Query(None, description='Param de requete otionnelle pour filtrer les cartes par type'),
    account_id: Optional[int] = Query(None,description='Param de requète optionnel pour obtenir uniquement les cartes d\'un compte précis'),
    user_id: int = Depends(get_current_user_id),
    bd_session: Session = Depends(get_db)
) -> CartesView:
    """Route pour récuperer les cartes d'un user ou d'un compte"""

    if account_id:
        cartes = get_user_cartes_in_an_account(bd_session, user_id, account_id, carte_type)
    else:
        cartes = get_user_cartes(bd_session, user_id, carte_type)

    return CartesView.success_response(cartes)

@router.get('/{carte_id}', response_model=CarteView)
def get_a_carte(
    carte_id : int = Path(..., title='Id de la carte'),
    password: Optional[str] = Query(..., description='Mot de passe de la carte'),
    user_id: int = Depends(get_current_user_id),
    bd_session: Session = Depends(get_db)
) -> CarteView:
    """Route pour récuperer les infos sur une carte précise"""

    carte = get_user_specific_carte(bd_session, user_id, carte_id, password)

    return CarteView.success_response(carte)

@router.delete('/{carte_id}', response_model=ApiBaseResponse[bool])
def delete_a_carte(
    carte_id : int = Path(..., title='Id de la carte'),
    password: Optional[str] = Query(..., description='Mot de passe de la carte'),
    user_id: int = Depends(get_current_user_id),
    bd_session: Session = Depends(get_db)
) -> ApiBaseResponse[bool]:

    result = delete_user_carte(bd_session, user_id, carte_id, password)
    if result:
        return ApiBaseResponse.success_response(result)
    return ApiBaseResponse.error_response("Mot de passe incorrect")     # Je suppose


@router.put('/change-password', response_model=ApiBaseResponse[bool])
def modify_carte_password(
    body : ChangeCartePassword,
    user_id: int = Depends(get_current_user_id),
    bd_session: Session = Depends(get_db)
) -> ApiBaseResponse[bool]:
    """Route pour récuperer les infos sur une carte précise"""

    result = change_carte_password(bd_session, user_id, body.carte_id, body.old_password, body.new_password)

    if result:
        return ApiBaseResponse.success_response(result)
    return ApiBaseResponse.error_response("Mot de passe incorrect")     # Je suppose toujours

