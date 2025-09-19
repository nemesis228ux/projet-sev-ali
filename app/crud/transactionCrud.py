from sqlalchemy.orm import Session
from typing import Sequence, Optional
from sqlalchemy import select
from app.models.transaction import Transaction, TransactionTypes
from app.schemas.transactionSchema import TransactionResult
from app.crud.compteCrud import get_account_by_id, get_account_by_numero_compte
#TODO : Voir si on peut ajouter des message d'erreur clair

def get_all_transactions_in_bd(
    bd_session : Session,
    transaction_type : Optional[TransactionTypes] = None
) -> Sequence[Transaction]:
    """
    Fonction poour recupérer les transactions de la bd avec possibilité de filtrage

    Args:
        bd_session: Instance de la bd
        transaction_type: Parametre optionnel pour filtrer les transferts par rapport au type

    Returns:
        type: La liste des transactions voulues
    """

    query = select(Transaction)
    if transaction_type:
        # noinspection PyTypeChecker
        query = query.where(Transaction.type_transac == transaction_type)

    transacs = bd_session.scalars(query).all()
    return transacs

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
    if not transaction_type:
        transaction_type = TransactionTypes.TRANSFERT
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

def get_user_specific_transaction(
        bd_session : Session,
        user_id : int,
        account_id : int,
        transaction_id : int
) -> Optional[Transaction]:
    """
    Fonction pour obtenir une transaction spécifique
    Args:
        bd_session: Instance de bd
        user_id: Id de l'utilisateur
        account_id: Id du compte
        transaction_id: Id de la transaction recherchée

    Returns:
        type: La transaction si elle est trouvée et appartient à l'utilisateur
    """
    # noinspection PyTypeChecker,PydanticTypeChecker
    query = select(Transaction).where(Transaction.id_transac == transaction_id)
    transac = bd_session.scalar(query)      # On recuperere la transac
    if not transac:     # La teansaction n'existe pas
        return None

    # On vérifie si l'utilisateur est bien impliqué dans la transaction
    if transac.base_account.account_owner_id == user_id \
            or \
            get_account_by_id(bd_session, user_id, account_id).numero_compte == transac.dest_num_compte:
        return transac

    #Cas où l'user n'est pas impliqué dans la transac
    return None

class Transactor:
    """Classe utilitaire pour gérer les transactions easily"""
    def __init__(self, bd_session : Session, initiator_id : int, iniatior_account_id : int,
                 transaction_type : TransactionTypes, transaction_amount : float, destinator_num_compte : Optional[str] = None):
        """
        Instanciateur de l'objet de transaction
        Args:
            bd_session: instance de la bdd
            iniatior_account_id: Id de compte de l'initiateur
            transaction_type: Le type de transaction
            transaction_amount: La valeur de la transaction
            destinator_num_compte: Numéro de compte du destinataire, Optionnel
        """

        # On récupère toutes les infos nécessaires en attributs privés
        self.__bd_session: Session = bd_session
        self.__iniatior_id: int = initiator_id
        self.__iniatior_account_id: int = iniatior_account_id
        self.__transaction_type: TransactionTypes = transaction_type
        self.__transaction_amount: float = transaction_amount
        self.__destinator_num_compte: str = destinator_num_compte

    def __withdraw_transac(self) -> tuple[bool, str | None]:
        """
        Fonction interne pour effectuer un retrait, agit directement avec les attributs de l'objet en interne
        Returns:
            type: Un tuple avec le resultat et un message d'erreur au cas où l'op a échioué
        """
        try:
            account = get_account_by_id(self.__bd_session, self.__iniatior_id, self.__iniatior_account_id)
            if not account:
                return False, "Ce compte n'existe pas ou ne vous appartient pas"
            solde = account.solde
            if self.__transaction_amount > solde:
                return False, "Solde insuffisant pour le retrait"
            new_solde = solde - self.__transaction_amount
            account.solde = new_solde
            self.__bd_session.commit()      # On met tout à jour
            return True, None
        except Exception as e:
            exc = f'Exception {e.__class__.__name__} : {e}'     # La trace de l'éxception
            return False, exc

    def __deposit_transac(self) -> tuple[bool, str | None]:
        """
        Fonction interne pour effectuer un dépot, aagit directement avec les attributs de l'objet en interne
        Returns:
            type: Un tuple avec le resultat et un message d'erreur au cas où l'op a échioué
        """
        try:
            compte = get_account_by_id(self.__bd_session, self.__iniatior_id, self.__iniatior_account_id)
            if not compte:
                return False, "Ce compte n'existe pas ou ne vous appartient pas"
            current_solde = compte.solde
            compte.solde = current_solde + self.__transaction_amount
            self.__bd_session.commit()      # On met tout a jour
            return True, None
        except Exception as e:
            exc = f'Exception {e.__class__.__name__} : {e}'         # La trace de l'éxception
            return False, exc

    def __transfer_transac(self) -> tuple[bool, str | None]:
        """
        Fonction interne pour effectuer une transaction, agit directement avec les attributs de l'objet en interne
        Returns:
            type: Un tuple avec le resultat et un message d'erreur au cas où l'op a échioué
        """
        try:
            # On recupere le compte du sender
            sender_account = get_account_by_id(self.__bd_session, self.__iniatior_id, self.__iniatior_account_id)

            if not sender_account:      # Cas où le compte est inexistantt
                return False, "Le compte spécifié n'esxiste pas"

            sender_solde = sender_account.solde
            if sender_solde < self.__transaction_amount:
                return False, "Vous n'avez pas suffisament de fonds"

            # On recupere le compte du receiver
            receiver_account = get_account_by_numero_compte(self.__bd_session, self.__destinator_num_compte)

            if not receiver_account:      # Cas où le compte est inexistantt
                return False, "Le numéro de compte n'est pas valide"


            # Transaction des fonds
            sender_account.solde = sender_solde - self.__transaction_amount
            receiver_account.solde += self.__transaction_amount

            self.__bd_session.commit()      # On met tout à jour

            return True, None


        except Exception as e:
            exc = f'Exception {e.__class__.__name__} : {e}'     # Cause de l'exception
            return False, exc

    def launch_transaction(self) -> TransactionResult:
        """
        Fonction principale pour lancer une transaction après avoir instancié l'objet
        Returns:
            type: Le resultat de la transaction

        """
        transac_type = self.__transaction_type
        success = False
        message = None
        transaction = None

        match transac_type:     # SELON sur le type de transaction
            case TransactionTypes.DEPOT:
                success, message = self.__deposit_transac()
            case TransactionTypes.RETRAIT:
                success, message = self.__withdraw_transac()
            case TransactionTypes.TRANSFERT:
                success, message = self.__transfer_transac()

        if success:     # On ajoute la transaction seulement en cas de succès
            transaction = Transaction(
                initiator_account_id=self.__iniatior_account_id,
                dest_num_compte=self.__destinator_num_compte,
                type_transac=transac_type,
                montant=self.__transaction_amount
            )
            self.__bd_session.add(transaction)      # Ajout de la transac
            self.__bd_session.commit()              # Mise à jour effective des data
            self.__bd_session.refresh(transaction)

        return TransactionResult(success=success, error=message, transac=transaction)