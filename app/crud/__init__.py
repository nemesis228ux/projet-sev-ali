# By Gemini

from typing import TypeVar, Generic, Optional

# Définition d'une variable de type (TypeVar)
# 'T' représentera le type de la donnée en cas de succès
T = TypeVar('T')

class CRUDResponse(Generic[T]):
    """
    Classe générique pour typer les réponses d'opérations CRUD.

    Elle encapsule soit une donnée de succès (data), soit un message d'erreur (error).
    Similaire au concept 'Result' ou 'Either' dans d'autres langages.
    """
    def __init__(self, data: Optional[T] = None, error: Optional[str] = None):
        if data is not None and error is not None:
            raise ValueError("Une réponse ne peut pas contenir à la fois des données et une erreur.")
        if data is None and error is None:
            raise ValueError("Une réponse doit contenir soit des données, soit une erreur.")

        self._data: Optional[T] = data
        self._error: Optional[str] = error

    def is_success(self) -> bool:
        """Retourne True si la réponse contient des données (succès)."""
        return self._data is not None

    def is_error(self) -> bool:
        """Retourne True si la réponse contient une erreur."""
        return self._error is not None

    @property
    def data(self) -> T:
        """
        Retourne les données de succès. Lève une exception si c'est une erreur.
        """
        if self._data is None:
            raise RuntimeError("Tentative d'accéder aux données sur une réponse d'erreur.")
        return self._data

    @property
    def error(self) -> str:
        """
        Retourne le message d'erreur. Lève une exception si c'est un succès.
        """
        if self._error is None:
            raise RuntimeError("Tentative d'accéder à l'erreur sur une réponse de succès.")
        return self._error

    # --- Méthodes utilitaires (Optional) ---

    def __repr__(self) -> str:
        if self.is_success():
            return f"<CRUDResponse Success: {self._data!r}>"
        return f"<CRUDResponse Error: {self._error!r}>"

    # --- Fonctions d'aide (Helpers) ---

    @classmethod
    def crud_success(cls, data: T):
        """Crée une réponse de succès avec les données fournies."""
        return cls(data=data)

    @classmethod
    def crud_error(cls, message: str):
        """Crée une réponse d'erreur avec le message fourni."""
        # On utilise Any pour le type de données car on sait qu'il n'y en aura pas.
        return cls(error=message)