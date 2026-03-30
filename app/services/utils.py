import re
from datetime import datetime
from difflib import SequenceMatcher
from typing import Optional, Dict, Any


def normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""

    value = value.upper().strip()
    value = re.sub(r"[^A-Z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def clean_aadhaar_number(aadhaar_number: Optional[str]) -> str:
    if not aadhaar_number:
        return ""
    return re.sub(r"\s+", "", aadhaar_number.strip())


def extract_surname(full_name: Optional[str]) -> str:
    normalized = normalize_text(full_name)
    if not normalized:
        return ""

    parts = normalized.split()
    return parts[-1] if parts else ""


def similarity_ratio(value1: Optional[str], value2: Optional[str]) -> float:
    text1 = normalize_text(value1)
    text2 = normalize_text(value2)

    if not text1 or not text2:
        return 0.0

    return SequenceMatcher(None, text1, text2).ratio()


def normalize_date(date_value: Optional[str]) -> Dict[str, Any]:
    """
    Returns:
    {
        "raw": original input,
        "normalized": "YYYY-MM-DD" or "YYYY",
        "year": "YYYY" or None,
        "precision": "full" | "year" | "unknown"
    }
    """
    if not date_value:
        return {
            "raw": date_value,
            "normalized": None,
            "year": None,
            "precision": "unknown"
        }

    value = date_value.strip()

    if re.fullmatch(r"\d{4}", value):
        return {
            "raw": date_value,
            "normalized": value,
            "year": value,
            "precision": "year"
        }

    formats = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"]

    for fmt in formats:
        try:
            parsed_date = datetime.strptime(value, fmt)
            return {
                "raw": date_value,
                "normalized": parsed_date.strftime("%Y-%m-%d"),
                "year": parsed_date.strftime("%Y"),
                "precision": "full"
            }
        except ValueError:
            continue

    return {
        "raw": date_value,
        "normalized": None,
        "year": None,
        "precision": "unknown"
    }