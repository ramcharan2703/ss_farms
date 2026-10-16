import re
from django.conf import settings
from django.core.exceptions import ValidationError


def normalize_indian_whatsapp_number(value):
    """
    Normalizes an Indian phone number into international digits-only format
    (91XXXXXXXXXX) for wa.me links. Returns None if the value is empty or not
    a valid Indian mobile number.
    """
    if not value:
        return None

    raw = str(value).strip()
    digits = re.sub(r"\D", "", raw)

    # 10 digits starting with valid Indian mobile prefix (6, 7, 8, 9)
    if len(digits) == 10 and digits[0] in "6789":
        return f"91{digits}"

    # 11 digits starting with 0 (STD trunk prefix)
    if len(digits) == 11 and digits.startswith("0") and digits[1] in "6789":
        return f"91{digits[1:]}"

    # 12 digits starting with country code 91
    if len(digits) == 12 and digits.startswith("91") and digits[2] in "6789":
        return digits

    return None


def validate_indian_whatsapp_number(value):
    """
    Django model/form validator for Indian WhatsApp mobile numbers.
    Accepts 10-digit numbers or numbers with +91/91 country code.
    Rejects corrupted/invalid numbers like '8' or non-Indian lengths.
    """
    if not value:
        return
    normalized = normalize_indian_whatsapp_number(value)
    if not normalized:
        raise ValidationError(
            "Enter a valid 10-digit Indian mobile number (e.g. 8790733189 or 918790733189)."
        )
