from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    ok : bool = Field(..., title="Champ pour véreifier si la reequete à réussi")
    result : Optional[T] = Field(default=None, title='Champ de résultat', description= 'Présent seulement si la requet à réussi')
    error: Optional[str] = None

    @classmethod
    def success_response(cls, data : Any):
        return cls(ok=True, result=data, error=None)

    @classmethod
    def error_response(cls, error_message : str):
        return cls(ok=False, result=None, error=error_message)