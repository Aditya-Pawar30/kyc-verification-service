"""
OCR Service for PAN and Aadhaar Card Extraction
"""
import re
import logging
from typing import Dict, Any, Optional
from PIL import Image
import pytesseract
import io

logger = logging.getLogger(__name__)


class OCRService:
    """Service for extracting text from PAN and Aadhaar card images"""
    
    def __init__(self):
        """Initialize OCR service"""
        # Configure pytesseract path for Windows if needed
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def extract_text_from_image(self, image_bytes: bytes) -> str:
        """
        Extract text from image bytes
        
        Args:
            image_bytes: Image bytes
            
        Returns:
            Extracted text string
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            return ""
    
    def extract_pan_details(self, text: str) -> Dict[str, Any]:
        """
        Extract PAN card details from text
        
        Args:
            text: Extracted text from PAN card image
            
        Returns:
            Dictionary with PAN details
        """
        details = {
            "name": None,
            "fatherName": None,
            "dob": None,
            "panNumber": None
        }
        
        try:
            # Extract PAN number (5 letters + 4 digits + 1 letter)
            pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]'
            pan_match = re.search(pan_pattern, text)
            if pan_match:
                details["panNumber"] = pan_match.group()
            
            # Extract DOB (DD/MM/YYYY format)
            dob_pattern = r'\d{2}/\d{2}/\d{4}'
            dob_match = re.search(dob_pattern, text)
            if dob_match:
                details["dob"] = dob_match.group()
            
            # Extract name (usually appears after "Name" or "नाम")
            lines = text.split('\n')
            for i, line in enumerate(lines):
                line_upper = line.upper().strip()
                
                # Look for name patterns
                if 'NAME' in line_upper or 'नाम' in line_upper:
                    # Name might be on the same line or next line
                    if ':' in line:
                        name_part = line.split(':', 1)[1].strip()
                        if name_part and len(name_part) > 2:
                            details["name"] = name_part.upper()
                    elif i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and len(next_line) > 2 and not any(char.isdigit() for char in next_line):
                            details["name"] = next_line.upper()
                
                # Look for father's name patterns
                if 'FATHER' in line_upper or 'पिता' in line_upper:
                    if ':' in line:
                        father_part = line.split(':', 1)[1].strip()
                        if father_part and len(father_part) > 2:
                            details["fatherName"] = father_part.upper()
                    elif i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and len(next_line) > 2 and not any(char.isdigit() for char in next_line):
                            details["fatherName"] = next_line.upper()
            
            # If name not found, try to find it by looking for capitalized words
            if not details["name"]:
                for line in lines:
                    line = line.strip()
                    # Look for lines with only letters and spaces (potential names)
                    if line and len(line) > 3 and re.match(r'^[A-Z\s]+$', line.upper()):
                        # Skip common words
                        skip_words = ['INCOME', 'TAX', 'DEPARTMENT', 'GOVERNMENT', 'INDIA', 'PERMANENT', 'ACCOUNT', 'NUMBER', 'CARD']
                        if not any(word in line.upper() for word in skip_words):
                            details["name"] = line.upper()
                            break
            
        except Exception as e:
            logger.error(f"Error extracting PAN details: {str(e)}")
        
        return details
    
    def extract_aadhaar_details(self, text: str) -> Dict[str, Any]:
        """
        Extract Aadhaar card details from text
        
        Args:
            text: Extracted text from Aadhaar card image
            
        Returns:
            Dictionary with Aadhaar details
        """
        details = {
            "name": None,
            "dob": None,
            "aadhaarNumber": None,
            "gender": None
        }
        
        try:
            # Extract Aadhaar number (12 digits)
            aadhaar_pattern = r'\d{4}\s?\d{4}\s?\d{4}'
            aadhaar_match = re.search(aadhaar_pattern, text)
            if aadhaar_match:
                # Remove spaces
                aadhaar_number = aadhaar_match.group().replace(' ', '')
                if len(aadhaar_number) == 12:
                    details["aadhaarNumber"] = aadhaar_number
            
            # Extract DOB (DD/MM/YYYY format)
            dob_pattern = r'\d{2}/\d{2}/\d{4}'
            dob_match = re.search(dob_pattern, text)
            if dob_match:
                details["dob"] = dob_match.group()
            
            # Extract year of birth (YYYY format)
            yob_pattern = r'\b(19|20)\d{2}\b'
            yob_match = re.search(yob_pattern, text)
            if yob_match and not details["dob"]:
                details["dob"] = f"01/01/{yob_match.group()}"
            
            # Extract gender
            text_upper = text.upper()
            if 'MALE' in text_upper or 'पुरुष' in text_upper:
                details["gender"] = "MALE"
            elif 'FEMALE' in text_upper or 'महिला' in text_upper:
                details["gender"] = "FEMALE"
            
            # Extract name
            lines = text.split('\n')
            for i, line in enumerate(lines):
                line_upper = line.upper().strip()
                
                # Look for name patterns
                if 'NAME' in line_upper or 'नाम' in line_upper:
                    if ':' in line:
                        name_part = line.split(':', 1)[1].strip()
                        if name_part and len(name_part) > 2:
                            details["name"] = name_part.upper()
                    elif i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and len(next_line) > 2 and not any(char.isdigit() for char in next_line):
                            details["name"] = next_line.upper()
            
            # If name not found, try to find it by looking for capitalized words
            if not details["name"]:
                for line in lines:
                    line = line.strip()
                    # Look for lines with only letters and spaces (potential names)
                    if line and len(line) > 3 and re.match(r'^[A-Z\s]+$', line.upper()):
                        # Skip common words
                        skip_words = ['GOVERNMENT', 'INDIA', 'UNIQUE', 'IDENTIFICATION', 'AUTHORITY', 'AADHAAR']
                        if not any(word in line.upper() for word in skip_words):
                            details["name"] = line.upper()
                            break
            
        except Exception as e:
            logger.error(f"Error extracting Aadhaar details: {str(e)}")
        
        return details
    
    def process_pan_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Process PAN card image and extract details
        
        Args:
            image_bytes: PAN card image bytes
            
        Returns:
            Dictionary with extracted PAN details
        """
        try:
            text = self.extract_text_from_image(image_bytes)
            if not text:
                return {"success": False, "error": "Could not extract text from image"}
            
            details = self.extract_pan_details(text)
            
            return {
                "success": True,
                "data": details,
                "rawText": text
            }
        except Exception as e:
            logger.error(f"Error processing PAN image: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def process_aadhaar_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Process Aadhaar card image and extract details
        
        Args:
            image_bytes: Aadhaar card image bytes
            
        Returns:
            Dictionary with extracted Aadhaar details
        """
        try:
            text = self.extract_text_from_image(image_bytes)
            if not text:
                return {"success": False, "error": "Could not extract text from image"}
            
            details = self.extract_aadhaar_details(text)
            
            return {
                "success": True,
                "data": details,
                "rawText": text
            }
        except Exception as e:
            logger.error(f"Error processing Aadhaar image: {str(e)}")
            return {"success": False, "error": str(e)}


# Create singleton instance
ocr_service = OCRService()
