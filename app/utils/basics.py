from datetime import datetime

# Fonction du robot
def format_datetime_custom(time : datetime):
    """
    Fonction personnalisée pour avoir un formattage de datetime en français By Claude

    Args:
        time (datetime): Objet datetime de base

    Returns:
        str: Date formatée en français
    """
    if not time:
        return ""
    try:
        # Dictionnaires pour la traduction française
        jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
        mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
                'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

        # Extraire les composants de la date
        jour_semaine = jours[time.weekday()]  # weekday() commence à 0 = lundi
        jour = time.day
        mois_nom = mois[time.month - 1]  # month commence à 1
        annee = time.year
        heure = time.hour
        minute = time.minute
        seconde = time.second

        # Formater la chaîne
        return f"{jour_semaine} {jour} {mois_nom} {annee} à {heure:02d}:{minute:02d}:{seconde:02d}".title()

    except (ValueError, OSError, OverflowError):
        return "DateTime invalide"