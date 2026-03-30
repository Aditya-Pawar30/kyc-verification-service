import io
import pytesseract
import requests
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from pdf2image import convert_from_bytes
from typing import Optional
import base64


# Tesseract path configuration
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image: Image.Image) -> Image.Image:
    """Preprocess image for better OCR results"""
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize for better OCR (300 DPI equivalent)
    width, height = image.size
    if width < 1000:
        new_size = (width * 2, height * 2)
        image = image.resize(new_size, Image.LANCZOS)
    
    # Convert to grayscale
    gray = image.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(1.5)
    
    # Apply slight sharpening
    gray = gray.filter(ImageFilter.SHARPEN)
    
    return gray

# Ollama configuration (optional)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_VISION_MODEL = "llava"


class OCRService:
    """OCR Service using Tesseract and optionally Ollama for text extraction"""
    
    @staticmethod
    def extract_with_tesseract(file_bytes: bytes, doc_type: str = "general") -> str:
        """Extract text using Tesseract OCR with preprocessing"""
        try:
            image = Image.open(io.BytesIO(file_bytes))
            
            # Preprocess the image for better OCR
            processed_image = preprocess_image(image)
            
            # Configure Tesseract for better results
            custom_config = r'--oem 3 --psm 6'
            extracted_text = pytesseract.image_to_string(processed_image, lang='eng', config=custom_config)
            
            print(f"Tesseract extracted for {doc_type}: {extracted_text[:500]}...")
            return extracted_text.strip()
        except Exception as e:
            print(f"Tesseract error: {str(e)}")
            return ""
    
    @staticmethod
    def extract_with_ollama(file_bytes: bytes, doc_type: str = "general") -> str:
        """Extract text using Ollama Vision API"""
        try:
            image_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
            if doc_type == "pan":
                prompt = """Extract ALL text from this PAN card image. Include:
- Name (look for "Name")
- Father's Name (look for "Father")
- Date of Birth (look for "DOB")
- PAN Number (10 character like ABCDE1234F)

Return ONLY:
NAME: <name>
FATHER_NAME: <father name>
DOB: <date of birth>
PAN_NUMBER: <pan number>"""
            elif doc_type == "aadhaar":
                prompt = """Extract ALL text from this Aadhaar card image. Include:
- Name
- Date of Birth (look for "DOB", "YOB")
- Aadhaar Number (12 digit)

Return ONLY:
NAME: <name>
DOB: <date of birth>
AADHAAR_NUMBER: <12 digit aadhaar>"""
            else:
                prompt = "Extract all text from this document image."
            
            payload = {
                "model": OLLAMA_VISION_MODEL,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False
            }
            
            response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                print(f"Ollama error: {response.status_code}")
                return ""
                
        except Exception as e:
            print(f"Ollama error: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_image_bytes(file_bytes: bytes, doc_type: str = "general") -> str:
        """Extract text from image using Tesseract OCR"""
        print(f"DEBUG: extract_text_from_image_bytes called for {doc_type}, file size: {len(file_bytes)} bytes")
        
        if not file_bytes or len(file_bytes) == 0:
            print("DEBUG: Empty file bytes!")
            return ""
        
        print(f"Using Tesseract for {doc_type}")
        result = OCRService.extract_with_tesseract(file_bytes, doc_type)
        print(f"DEBUG: OCR result length: {len(result)}")
        return result
    
    @staticmethod
    def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
        """Extract text from PDF"""
        try:
            images = convert_from_bytes(file_bytes)
            all_text = []
            for page_num, image in enumerate(images):
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                text = OCRService.extract_text_from_image_bytes(img_byte_arr.getvalue(), "pdf")
                all_text.append(f"--- Page {page_num + 1} ---\n{text}")
            return "\n".join(all_text)
        except Exception as e:
            print(f"PDF error: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text(file_bytes: bytes, content_type: str, filename: str = "", doc_type: str = "general") -> str:
        """Extract text from file based on type"""
        content_type = (content_type or "").lower()
        filename = (filename or "").lower()
        
        if "pdf" in content_type or filename.endswith(".pdf"):
            return OCRService.extract_text_from_pdf_bytes(file_bytes)
        
        return OCRService.extract_text_from_image_bytes(file_bytes, doc_type)