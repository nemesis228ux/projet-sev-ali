from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class ApiBaseResponse(BaseModel, Generic[T]):
    """Scema de base pour uniformiser les réponses de l'API"""
    ok : bool = Field(..., title="Champ pour véreifier si la reequete à réussi")
    result : Optional[T] = Field(default=None, title='Champ de résultat', description= 'Présent seulement si la requet à réussi')
    error: Optional[str] = None
    
    
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