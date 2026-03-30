from fastapi import UploadFile
from typing import Dict, Any

from app.services.extraction.ocr_service import OCRService
from app.services.extraction.pan_extractor import PanExtractor
from app.services.extraction.aadhaar_extractor import AadhaarExtractor
from app.services.fraud_detection.fraud_detection_service import FraudDetectionService
from app.models.request_models import FraudDetectionRequest, PanCardData, AadhaarCardData
from app.models.response_models import FraudDetectionResponse, ProcessAndDetectResponse, ExtractedData


class ProcessAndDetectService:
    """Orchestrates the entire process: file upload -> OCR -> extraction -> fraud detection"""
    
    @staticmethod
    async def process_files(pan_file: UploadFile, aadhaar_file: UploadFile) -> ProcessAndDetectResponse:
        """
        Process uploaded PAN and Aadhaar files, extract data, and perform fraud detection
        
        Args:
            pan_file: Uploaded PAN card file (image or PDF)
            aadhaar_file: Uploaded Aadhaar card file (image or PDF)
            
        Returns:
            ProcessAndDetectResponse with extracted data and fraud analysis results
        """
        
        # Read file contents
        pan_content = await pan_file.read()
        aadhaar_content = await aadhaar_file.read()
        
        # Get content type
        pan_content_type = pan_file.content_type
        aadhaar_content_type = aadhaar_file.content_type
        
        # Extract text using OCR
        print(f"DEBUG: PAN content type: {pan_content_type}, filename: {pan_file.filename}, content length: {len(pan_content)}")
        pan_text = OCRService.extract_text(
            pan_content, 
            pan_content_type, 
            pan_file.filename or "",
            "pan"
        )
        print(f"DEBUG: PAN extracted text: {pan_text[:200] if pan_text else 'EMPTY'}")
        
        print(f"DEBUG: Aadhaar content type: {aadhaar_content_type}, filename: {aadhaar_file.filename}, content length: {len(aadhaar_content)}")
        aadhaar_text = OCRService.extract_text(
            aadhaar_content, 
            aadhaar_content_type, 
            aadhaar_file.filename or "",
            "aadhaar"
        )
        print(f"DEBUG: Aadhaar extracted text: {aadhaar_text[:200] if aadhaar_text else 'EMPTY'}")
        
        # Extract structured data using extractors
        pan_data = PanExtractor.extract(pan_text)
        aadhaar_data = AadhaarExtractor.extract(aadhaar_text)
        
        # Create request object for fraud detection
        request_data = FraudDetectionRequest(
            panCard=PanCardData(**pan_data),
            aadhaarCard=AadhaarCardData(**aadhaar_data)
        )
        
        # Perform fraud detection
        fraud_result = FraudDetectionService.detect_fraud(request_data)
        
        # Build response with extracted data
        return ProcessAndDetectResponse(
            extractedPan=ExtractedData(**pan_data),
            extractedAadhaar=ExtractedData(
                name=aadhaar_data.get("name"),
                dob=aadhaar_data.get("dob"),
                aadhaarNumber=aadhaar_data.get("aadhaarNumber")
            ),
            fraudResult=fraud_result
        )
    
    @staticmethod
    def process_text_only(pan_text: str, aadhaar_text: str) -> ProcessAndDetectResponse:
        """
        Process text directly (for testing without file upload)
        
        Args:
            pan_text: OCR text from PAN card
            aadhaar_text: OCR text from Aadhaar card
            
        Returns:
            ProcessAndDetectResponse with extracted data and fraud analysis results
        """
        
        # Extract structured data using extractors
        pan_data = PanExtractor.extract(pan_text)
        aadhaar_data = AadhaarExtractor.extract(aadhaar_text)
        
        # Create request object for fraud detection
        request_data = FraudDetectionRequest(
            panCard=PanCardData(**pan_data),
            aadhaarCard=AadhaarCardData(**aadhaar_data)
        )
        
        # Perform fraud detection
        fraud_result = FraudDetectionService.detect_fraud(request_data)
        
        # Build response with extracted data
        return ProcessAndDetectResponse(
            extractedPan=ExtractedData(**pan_data),
            extractedAadhaar=ExtractedData(
                name=aadhaar_data.get("name"),
                dob=aadhaar_data.get("dob"),
                aadhaarNumber=aadhaar_data.get("aadhaarNumber")
            ),
            fraudResult=fraud_result
        )