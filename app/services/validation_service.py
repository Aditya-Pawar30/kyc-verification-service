import re
from app.services.utils import clean_aadhaar_number


PAN_REGEX = r"^[A-Z]{5}[0-9]{4}[A-Z]$"
AADHAAR_REGEX = r"^\d{12}$"


def validate_pan_number(pan_number: str) -> bool:
    if not pan_number:
        return False
    return bool(re.fullmatch(PAN_REGEX, pan_number.strip().upper()))


def validate_aadhaar_number(aadhaar_number: str) -> bool:
    cleaned = clean_aadhaar_number(aadhaar_number)
    if not cleaned:
        return False
    return bool(re.fullmatch(AADHAAR_REGEX, cleaned))