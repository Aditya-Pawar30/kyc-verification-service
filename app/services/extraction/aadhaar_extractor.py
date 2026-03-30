import re
from typing import Optional, Dict


class AadhaarExtractor:
    """Extracts information from Aadhaar card text using regex patterns"""
    
    AADHAAR_REGEX = r"\b\d{4}\s?\d{4}\s?\d{4}\b"
    DOB_REGEXES = [
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{4}\b",  # Year only
    ]

    BLOCKED_WORDS = {
        "GOVERNMENT OF INDIA",
        "UNIQUE IDENTIFICATION AUTHORITY OF INDIA",
        "AADHAAR",
        "DOB",
        "YEAR OF BIRTH",
        "MALE",
        "FEMALE",
        "ADDRESS",
        "VID",
    }

    @staticmethod
    def extract_aadhaar_number(text: str) -> Optional[str]:
        """Extract Aadhaar number from text"""
        # First check for Grok format: AADHAAR_NUMBER: 123456789012
        match = re.search(r"AADHAAR_NUMBER[:\s]*(\d{12})", text)
        if match:
            return match.group(1)
        
        # Fall back to regex search
        match = re.search(AadhaarExtractor.AADHAAR_REGEX, text)
        if match:
            return re.sub(r"\s+", "", match.group(0))
        return None

    @staticmethod
    def extract_name(text: str) -> Optional[str]:
        """Extract name from Aadhaar card text"""
        # First check for Grok format: NAME: John Doe
        match = re.search(r"NAME[:\s]*([A-Z][A-Z\s]*)", text.upper())
        if match:
            name = match.group(1).strip()
            # Remove any trailing keywords
            for keyword in ['DOB', 'YEAR', 'MALE', 'FEMALE', 'ADDRESS', 'UID', 'AADHAAR']:
                if name.endswith(keyword):
                    name = name[:-(len(keyword))].strip()
            return name if name else None
        
        # Fall back to original logic
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            upper_line = line.upper()
            
            if any(word in upper_line for word in AadhaarExtractor.BLOCKED_WORDS):
                continue
            
            if re.search(AadhaarExtractor.AADHAAR_REGEX, upper_line):
                continue
            
            if re.fullmatch(r"[\d\-\/\s]+", upper_line):
                continue
            
            if len(upper_line) < 3:
                continue
            
            if re.match(r"^[A-Z\s]+$", upper_line):
                return upper_line
        
        return None

    @staticmethod
    def extract_dob(text: str) -> Optional[str]:
        """Extract date of birth from Aadhaar card text"""
        # First check for Grok format: DOB: 01/01/1990
        match = re.search(r"DOB[:\s]*(\d{2}/\d{2}/\d{4})", text)
        if match:
            return match.group(1)
        
        # Also check for year only format
        match = re.search(r"DOB[:\s]*(\d{4})", text)
        if match:
            return match.group(1)
        
        # Fall back to regex search
        for pattern in AadhaarExtractor.DOB_REGEXES:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None

    @staticmethod
    def extract(text: str) -> Dict[str, Optional[str]]:
        """Extract all Aadhaar card information from OCR text"""
        return {
            "name": AadhaarExtractor.extract_name(text),
            "dob": AadhaarExtractor.extract_dob(text),
            "aadhaarNumber": AadhaarExtractor.extract_aadhaar_number(text)
        }