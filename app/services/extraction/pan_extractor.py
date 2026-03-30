import re
from typing import Optional, Dict


class PanExtractor:
    """Extracts information from PAN card text using regex patterns"""
    
    PAN_REGEX = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    NAME_REGEX = r"(?:Name)[\s:]*([A-Z\s]+)"
    DOB_REGEXES = [
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
    ]

    @staticmethod
    def extract_pan_number(text: str) -> Optional[str]:
        """Extract PAN number from text"""
        # First check for Grok format: PAN_NUMBER: ABCDE1234F
        match = re.search(r"PAN_NUMBER[:\s]*([A-Z]{5}[0-9]{4}[A-Z])", text.upper())
        if match:
            return match.group(1)
        
        # Fall back to regex search
        match = re.search(PanExtractor.PAN_REGEX, text.upper())
        return match.group(0) if match else None

    @staticmethod
    def extract_name(text: str) -> Optional[str]:
        """Extract name from PAN card text"""
        # First check for Grok format: NAME: John Doe
        match = re.search(r"NAME[:\s]*([A-Z][A-Z\s]*)", text.upper())
        if match:
            name = match.group(1).strip()
            # Remove any trailing keywords
            for keyword in ['FATHER', 'MOTHER', 'DOB', 'PAN', 'DATE']:
                if name.endswith(keyword):
                    name = name[:-(len(keyword))].strip()
            return name if name else None
        
        # Fall back to original logic
        lines = text.upper().split('\n')
        for line in lines:
            if 'NAME' in line and ':' in line:
                name = line.split(':', 1)[1].strip()
                if name and 'FATHER' not in name and len(name) > 2:
                    return name
            # Look for name line without NAME label
            if re.match(r"^[A-Z]{3,}\s[A-Z]+$", line.strip()):
                if 'FATHER' not in line and 'DOB' not in line and 'PAN' not in line:
                    return line.strip()
        return None

    @staticmethod
    def extract_father_name(text: str) -> Optional[str]:
        """Extract father name from PAN card text"""
        # First check for Grok format: FATHER_NAME: Robert Doe
        match = re.search(r"FATHER_NAME[:\s]*([A-Z\s]+)", text.upper())
        if match:
            return match.group(1).strip()
        
        # Fall back to original logic
        lines = text.upper().split('\n')
        for line in lines:
            if 'FATHER' in line:
                if ':' in line:
                    return line.split(':', 1)[1].strip()
        return None

    @staticmethod
    def extract_dob(text: str) -> Optional[str]:
        """Extract date of birth from PAN card text"""
        # First check for Grok format: DOB: 01/01/1990
        match = re.search(r"DOB[:\s]*(\d{2}/\d{2}/\d{4})", text)
        if match:
            return match.group(1)
        
        # Fall back to regex search
        for pattern in PanExtractor.DOB_REGEXES:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None

    @staticmethod
    def extract(text: str) -> Dict[str, Optional[str]]:
        """Extract all PAN card information from OCR text"""
        return {
            "name": PanExtractor.extract_name(text),
            "fatherName": PanExtractor.extract_father_name(text),
            "dob": PanExtractor.extract_dob(text),
            "panNumber": PanExtractor.extract_pan_number(text)
        }