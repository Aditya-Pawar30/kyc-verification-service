
from typing import Dict, Any

from app.services.utils import (
    normalize_text,
    similarity_ratio,
    extract_surname,
    normalize_date,
)


def compare_names(pan_name: str, aadhaar_name: str) -> Dict[str, Any]:
    ratio = similarity_ratio(pan_name, aadhaar_name)

    if not pan_name or not aadhaar_name:
        return {
            "name_match": False,
            "match_type": "missing_data",
            "ratio": ratio
        }

    if ratio >= 0.90:
        return {
            "name_match": True,
            "match_type": "strong_match",
            "ratio": ratio
        }
    elif ratio >= 0.75:
        return {
            "name_match": False,
            "match_type": "minor_mismatch",
            "ratio": ratio
        }
    elif ratio >= 0.55:
        return {
            "name_match": False,
            "match_type": "moderate_mismatch",
            "ratio": ratio
        }
    else:
        return {
            "name_match": False,
            "match_type": "major_mismatch",
            "ratio": ratio
        }


def compare_surname_consistency(
    pan_name: str,
    father_name: str,
    aadhaar_name: str
) -> Dict[str, Any]:
    pan_surname = extract_surname(pan_name)
    father_surname = extract_surname(father_name)
    aadhaar_surname = extract_surname(aadhaar_name)

    if not father_name:
        return {
            "consistent": True,
            "consistency_type": "father_name_not_available"
        }

    if not pan_surname or not father_surname:
        return {
            "consistent": True,
            "consistency_type": "insufficient_data"
        }

    if pan_surname == father_surname:
        if aadhaar_surname and aadhaar_surname != pan_surname:
            return {
                "consistent": False,
                "consistency_type": "strong_inconsistency"
            }
        return {
            "consistent": True,
            "consistency_type": "consistent"
        }

    if aadhaar_surname and aadhaar_surname not in {pan_surname, father_surname}:
        return {
            "consistent": False,
            "consistency_type": "weak_inconsistency"
        }

    return {
        "consistent": True,
        "consistency_type": "consistent"
    }


def compare_dob(pan_dob: str, aadhaar_dob: str) -> Dict[str, Any]:
    pan_date = normalize_date(pan_dob)
    aadhaar_date = normalize_date(aadhaar_dob)

    if not pan_date["normalized"] or not aadhaar_date["normalized"]:
        return {
            "dob_match": False,
            "match_type": "missing_or_invalid_data"
        }

    if pan_date["precision"] == "full" and aadhaar_date["precision"] == "full":
        if pan_date["normalized"] == aadhaar_date["normalized"]:
            return {
                "dob_match": True,
                "match_type": "full_match"
            }
        return {
            "dob_match": False,
            "match_type": "complete_mismatch"
        }

    if pan_date["year"] and aadhaar_date["year"] and pan_date["year"] == aadhaar_date["year"]:
        if pan_date["precision"] == "year" or aadhaar_date["precision"] == "year":
            return {
                "dob_match": False,
                "match_type": "partial_match"
            }

    return {
        "dob_match": False,
        "match_type": "complete_mismatch"
    }