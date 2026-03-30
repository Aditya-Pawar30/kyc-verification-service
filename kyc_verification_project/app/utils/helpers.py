"""
Utility helpers for KYC Verification System
"""
from typing import Optional
from difflib import SequenceMatcher
import re


def normalize_name(name: Optional[str]) -> str:
    """
    Normalize name for comparison
    
    Args:
        name: Name to normalize
        
    Returns:
        Normalized name string
    """
    if not name:
        return ""
    
    # Convert to uppercase and remove extra spaces
    normalized = " ".join(name.upper().split())
    
    # Remove common prefixes/suffixes
    prefixes = ["MR.", "MRS.", "MS.", "DR.", "SHRI", "SMT", "SMT.", "KUMARI"]
    suffixes = ["JR", "SR", "I", "II", "III"]
    
    words = normalized.split()
    filtered_words = [
        word for word in words 
        if word not in prefixes and word not in suffixes
    ]
    
    return " ".join(filtered_words)


def normalize_dob(dob: Optional[str]) -> Optional[str]:
    """
    Normalize date of birth for comparison
    
    Args:
        dob: Date of birth string (DD/MM/YYYY or other formats)
        
    Returns:
        Normalized DOB string in DD/MM/YYYY format or None if invalid
    """
    if not dob:
        return None
    
    # Remove extra spaces
    dob = dob.strip()
    
    # Try to parse different date formats
    # DD/MM/YYYY
    if re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
        return dob
    
    # DD-MM-YYYY
    if re.match(r'^\d{2}-\d{2}-\d{4}$', dob):
        parts = dob.split('-')
        return f"{parts[0]}/{parts[1]}/{parts[2]}"
    
    # YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}$', dob):
        parts = dob.split('-')
        return f"{parts[2]}/{parts[1]}/{parts[0]}"
    
    # YYYY/MM/DD
    if re.match(r'^\d{4}/\d{2}/\d{2}$', dob):
        parts = dob.split('/')
        return f"{parts[2]}/{parts[1]}/{parts[0]}"
    
    # DD.MM.YYYY
    if re.match(r'^\d{2}\.\d{2}\.\d{4}$', dob):
        parts = dob.split('.')
        return f"{parts[0]}/{parts[1]}/{parts[2]}"
    
    return dob


def calculate_name_similarity(name1: str, name2: str) -> float:
    """
    Calculate similarity between two names
    
    Args:
        name1: First name
        name2: Second name
        
    Returns:
        Similarity score between 0 and 1
    """
    normalized1 = normalize_name(name1)
    normalized2 = normalize_name(name2)
    
    if not normalized1 or not normalized2:
        return 0.0
    
    return SequenceMatcher(None, normalized1, normalized2).ratio()


def compare_names(name1: Optional[str], name2: Optional[str], threshold: float = 0.75) -> bool:
    """
    Compare two names with fuzzy matching
    
    Args:
        name1: First name
        name2: Second name
        threshold: Similarity threshold (0-1)
        
    Returns:
        True if names match above threshold
    """
    if not name1 or not name2:
        return False
    
    similarity = calculate_name_similarity(name1, name2)
    return similarity >= threshold


def compare_dobs(dob1: Optional[str], dob2: Optional[str]) -> bool:
    """
    Compare two dates of birth
    
    Args:
        dob1: First DOB
        dob2: Second DOB
        
    Returns:
        True if DOBs match
    """
    if not dob1 or not dob2:
        return False
    
    normalized1 = normalize_dob(dob1)
    normalized2 = normalize_dob(dob2)
    
    if not normalized1 or not normalized2:
        return False
    
    return normalized1 == normalized2


def validate_pan_format(pan_number: Optional[str]) -> bool:
    """
    Validate PAN number format
    
    Args:
        pan_number: PAN number to validate
        
    Returns:
        True if format is valid
    """
    if not pan_number:
        return False
    
    # PAN format: 5 letters + 4 digits + 1 letter
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    return bool(re.match(pattern, pan_number.upper()))


def validate_aadhaar_format(aadhaar_number: Optional[str]) -> bool:
    """
    Validate Aadhaar number format
    
    Args:
        aadhaar_number: Aadhaar number to validate
        
    Returns:
        True if format is valid
    """
    if not aadhaar_number:
        return False
    
    # Aadhaar format: 12 digits
    return aadhaar_number.isdigit() and len(aadhaar_number) == 12
