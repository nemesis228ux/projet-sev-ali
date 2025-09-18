from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

# Modele de base pour toutes les reponses de l'API
#TODO: Faire des recherches et voir si çà ne serait pas mieux de mettre en classe abstraite
class ApiBaseResponse(BaseModel, Generic[T]):
    """Scema de base pour uniformiser les réponses de l'API"""

    ok : bool = Field(..., title="Champ pour véreifier si la reequete à réussi, True si la requete a reussi, False sinon")

    result : Optional[T] = Field(
        default=None, title='Champ de résultat',
        description= 'Présent seulement si la requet à réussi'
    )
    error: Optional[str] = Field(
        default=None, title='Champ des erreurs',
        description= "Présent seulement si la requet à échouée ou si quelque chose s'est mal passé durant le traitement"
    )
    
    # Cette methode permettra de renvoyer les reponse de succèss directement depuis les classes filles
    @classmethod
    def success_response(cls, data : Any):
        """
        Methode pour instancier une reponse de succes
        Args:
            data: Données à retourner
        Returns:
            Une instance de ApiBaseResponse
        """
        return cls(ok=True, result=data, error=None)

    # Cette methode permettra de renvoyer les reponse d'erreur directement depuis les classes filles
    @classmethod
    def error_response(cls, error_message : str):
        """
        Methode pour instancier une réponse d'échec
        Args:
            error_message: Le message d'erreur à retourner

        Returns:
            Une instance de ApiBaseResponse
        """
        return cls(ok=False, result=None, error=error_message)