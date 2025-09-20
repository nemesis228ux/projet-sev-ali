from uuid import uuid4


def generate_random_number(size: int = 16) -> str:
    """
    Fonction utilitaire pour générer des numéros aléatoirement, à utiliser pour les numéro de comptes, cartes et autres
        choses qui doivent etres aéatoire
    Args:
        size: La taille du nombre aléatoire à creer

    Returns:
        str: Le nombre aléatoire

    """
    final_number: str = ""

    while len(final_number) < size:
        final_number += uuid4().int.__str__()

    return final_number[:size]
