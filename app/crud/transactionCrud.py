from sqlalchemy.orm import Session
from typing import Sequence
from sqlalchemy import select
from app.models.transaction import Transaction, TransactionTypes
from app.schemas.transactionSchema import TransactionInit, TransactionResult
from app.crud.compteCrud import get_account_by_id, get_account_by_numero_compte
#TODO : Voir si on peut ajouter des message d'erreur clair

def get_user_transactions(
        bd_session : Session,
        user_id : int,
        account_id : int,
        transaction_type : TransactionTypes = TransactionTypes.TRANSFERT) -> Sequence[Transaction]:
    """
    Fonction poour recupérer les transactions d'un compte avec possibilité de filtrage

    Args:
        bd_session: Instance de la bd
        user_id: Id de l'utilisateur
        account_id: Id du compte
        transaction_type: Parametre optionnel pour filtrer les transferts par rapport au type

    Returns:
        type: La liste des transactions voulues
    """

    user_account = get_account_by_id(bd_session, user_id, account_id)   # On recupere le compte cible
    if not user_account:    #Si le compte n'est pas trouvé, on retourne un tableau vide
        return []       #TODO: Voir si c'est possible de rajouter un message clair

    transactions = user_account.transactions
    match transaction_type.value:       # SELON sur le type de transaction
        case TransactionTypes.TRANSFERT:
            # Si ce sont des transferts, on doit aussi recuperer les transferts entrants à travers le numero de compte
            account_num = user_account.numero_compte
            # noinspection PyTypeChecker,PydanticTypeChecker
            query = select(Transaction).where(Transaction.dest_num_compte == account_num)
            other_transacs = bd_session.scalars(query).all()
            transactions.extend(other_transacs)

        case TransactionTypes.DEPOT:
            transactions = [transac for transac in transactions if transac.type_transac == TransactionTypes.DEPOT]

        case TransactionTypes.RETRAIT:
            transactions = [transac for transac in transactions if transac.type_transac == TransactionTypes.RETRAIT]

    return transactions


class Transactor:
    def __init__(self, bd_session : Session, transac_info : TransactionInit):
        self.__bd_session: Session = bd_session
        self.__iniatior_id: int = transac_info.user_id
        self.__iniatior_account_id: int = transac_info.account_id
        self.__transaction_type: TransactionTypes = transac_info.transaction_type
        self.__transaction_amount: float = transac_info.amount
        self.__destinator_num_compte: str = transac_info.destinator_num_compte

    def __withdraw_transac(self) -> tuple[bool, str | None]:
        try:
            account = get_account_by_id(self.__bd_session, self.__iniatior_id, self.__iniatior_account_id)
            solde = account.solde
            if self.__transaction_amount > solde:
                return False, "Solde insuffisant pour le retrait"
            new_solde = solde - self.__transaction_amount
            account.solde = new_solde
            self.__bd_session.commit()
            return True, None
        except Exception as e:
            exc = f'Exception {e.__class__.__name__} : {e}'
            return False, exc

    def __deposit_transac(self) -> tuple[bool, str | None]:
        try:
            compte = get_account_by_id(self.__bd_session, self.__iniatior_id, self.__iniatior_account_id)
            current_solde = compte.solde
            compte.solde = current_solde + self.__transaction_amount
            self.__bd_session.commit()
            return True, None
        except Exception as e:
            exc = f'Exception {e.__class__.__name__} : {e}'
            return False, exc

    def __transfer_transac(self) -> tuple[bool, str | None]:
        try:
            sender_account = get_account_by_id(self.__bd_session, self.__iniatior_id, self.__iniatior_account_id)
            if not sender_account:
                return False, "Le compte spécifié n'esxiste pas"


            sender_solde = sender_account.solde
            if sender_solde < self.__transaction_amount:
                return False, "Vous n'avez pas suffisament de fonds"

            receiver_account = get_account_by_numero_compte(self.__bd_session, self.__destinator_num_compte)
            if not receiver_account:
                return False, "Le numéro de compte n'est pas valide"


            sender_account.solde = sender_solde - self.__transaction_amount
            receiver_account.solde += self.__transaction_amount

            self.__bd_session.commit()

            return True, None


        except Exception as e:
            exc = f'Exception {e.__class__.__name__} : {e}'
            return False, exc

    def launch_transaction(self) -> TransactionResult:
        transac_type = self.__transaction_type
        success = False
        message = None
        match transac_type:
            case TransactionTypes.DEPOT:
                success, message = self.__deposit_transac()
            case TransactionTypes.RETRAIT:
                success, message = self.__withdraw_transac()
            case TransactionTypes.TRANSFERT:
                success, message = self.__transfer_transac()

        if success:
            transaction = Transaction(
                initiator_account_id=self.__iniatior_account_id,
                dest_num_compte=self.__destinator_num_compte,
                type_transac=transac_type,
                montant=self.__transaction_amount
            )
            self.__bd_session.add(transaction)
            self.__bd_session.commit()

        return TransactionResult(success=success, error=message)