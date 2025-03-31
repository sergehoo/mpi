import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat


def nettoyer_numero_international(numero_brut, pays_iso='CI'):
    """
    Nettoie, normalise et valide un numéro au format international (E.164)
    """
    if not numero_brut:
        return None
    try:
        # Nettoyage visuel (supprime espaces, tirets, etc.)
        numero_brut = ''.join(numero_brut.split())

        # Parsing intelligent
        numero = phonenumbers.parse(numero_brut, pays_iso)
        if not phonenumbers.is_valid_number(numero):
            return None

        # Retourne en format international +225xxxx
        return phonenumbers.format_number(numero, PhoneNumberFormat.E164)
    except NumberParseException:
        return None