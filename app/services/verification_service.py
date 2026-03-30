"""
KYC Verification Service
Handles PAN and Aadhaar verification using Sandbox.co.in APIs
"""
import requests
import logging
from typing import Optional, Tuple
from difflib import SequenceMatcher

from app.config.settings import settings
from app.models.request_models import PanCardData, AadhaarCardData
from app.models.verification_response_models import (
    PanVerificationResult,
    AadhaarVerificationResult,
    VerificationStatus
)

logger = logging.getLogger(__name__)


class VerificationService:
    """Service for KYC verification using Sandbox APIs"""
    
    def __init__(self):
        """Initialize verification service"""
        self.api_key = settings.SANDBOX_API_KEY
        self.api_secret = settings.SANDBOX_API_SECRET
        self.base_url = settings.SANDBOX_BASE_URL
        self.timeout = settings.API_TIMEOUT
        self.headers = {
            "x-api-key": self.api_key,
            "x-api-secret": self.api_secret,
            "Content-Type": "application/json"
        }
    
    def normalize_name(self, name: Optional[str]) -> str:
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
    
    def calculate_name_similarity(self, name1: str, name2: str) -> float:
        """
        Calculate similarity between two names
        
        Args:
            name1: First name
            name2: Second name
            
        Returns:
            Similarity score between 0 and 1
        """
        normalized1 = self.normalize_name(name1)
        normalized2 = self.normalize_name(name2)
        
        if not normalized1 or not normalized2:
            return 0.0
        
        return SequenceMatcher(None, normalized1, normalized2).ratio()
    
    def verify_pan(self, pan_number: str, name: Optional[str] = None) -> PanVerificationResult:
        """
        Verify PAN number using Sandbox API
        
        Args:
            pan_number: PAN number to verify
            name: Name on PAN card (optional, for matching)
            
        Returns:
            PanVerificationResult with verification details
        """
        try:
            # Validate PAN number format
            if not pan_number or len(pan_number) != 10:
                return PanVerificationResult(
                    panValid=False,
                    panStatus="INVALID",
                    nameMatch=False
                )
            
            # Call Sandbox PAN verification API
            url = f"{self.base_url}{settings.PAN_VERIFICATION_ENDPOINT}"
            payload = {
                "pan": pan_number
            }
            
            logger.info(f"Verifying PAN: {pan_number}")
            
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract verification results from API response
                # Note: Actual response structure depends on Sandbox API
                pan_valid = data.get("valid", False)
                pan_status = data.get("status", "INVALID").upper()
                
                # Check name match if API returns name
                api_name = data.get("name", "")
                name_match = False
                
                if name and api_name:
                    similarity = self.calculate_name_similarity(name, api_name)
                    name_match = similarity >= settings.NAME_SIMILARITY_THRESHOLD
                elif not name:
                    # If no name provided, consider it a match
                    name_match = True
                
                return PanVerificationResult(
                    panValid=pan_valid,
                    panStatus=pan_status,
                    nameMatch=name_match
                )
            
            elif response.status_code == 404:
                logger.warning(f"PAN not found: {pan_number}")
                return PanVerificationResult(
                    panValid=False,
                    panStatus="INVALID",
                    nameMatch=False
                )
            
            else:
                logger.error(f"PAN verification API error: {response.status_code}")
                return PanVerificationResult(
                    panValid=False,
                    panStatus="INVALID",
                    nameMatch=False
                )
                
        except requests.Timeout:
            logger.error(f"PAN verification timeout for: {pan_number}")
            return PanVerificationResult(
                panValid=False,
                panStatus="INVALID",
                nameMatch=False
            )
        
        except requests.RequestException as e:
            logger.error(f"PAN verification request error: {str(e)}")
            return PanVerificationResult(
                panValid=False,
                panStatus="INVALID",
                nameMatch=False
            )
        
        except Exception as e:
            logger.error(f"Unexpected error during PAN verification: {str(e)}")
            return PanVerificationResult(
                panValid=False,
                panStatus="INVALID",
                nameMatch=False
            )
    
    def verify_aadhaar(self, aadhaar_number: str, name: Optional[str] = None) -> AadhaarVerificationResult:
        """
        Verify Aadhaar number using Sandbox API
        
        Args:
            aadhaar_number: Aadhaar number to verify
            name: Name on Aadhaar card (optional, for matching)
            
        Returns:
            AadhaarVerificationResult with verification details
        """
        try:
            # Validate Aadhaar number format (12 digits)
            if not aadhaar_number or len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
                return AadhaarVerificationResult(
                    aadhaarValid=False,
                    aadhaarStatus="INVALID",
                    nameMatch=False
                )
            
            # Call Sandbox Aadhaar verification API
            url = f"{self.base_url}{settings.AADHAAR_VERIFICATION_ENDPOINT}"
            payload = {
                "aadhaar": aadhaar_number
            }
            
            logger.info(f"Verifying Aadhaar: {aadhaar_number}")
            
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract verification results from API response
                # Note: Actual response structure depends on Sandbox API
                aadhaar_valid = data.get("valid", False)
                aadhaar_status = data.get("status", "INVALID").upper()
                
                # Check name match if API returns name
                api_name = data.get("name", "")
                name_match = False
                
                if name and api_name:
                    similarity = self.calculate_name_similarity(name, api_name)
                    name_match = similarity >= settings.NAME_SIMILARITY_THRESHOLD
                elif not name:
                    # If no name provided, consider it a match
                    name_match = True
                
                return AadhaarVerificationResult(
                    aadhaarValid=aadhaar_valid,
                    aadhaarStatus=aadhaar_status,
                    nameMatch=name_match
                )
            
            elif response.status_code == 404:
                logger.warning(f"Aadhaar not found: {aadhaar_number}")
                return AadhaarVerificationResult(
                    aadhaarValid=False,
                    aadhaarStatus="INVALID",
                    nameMatch=False
                )
            
            else:
                logger.error(f"Aadhaar verification API error: {response.status_code}")
                return AadhaarVerificationResult(
                    aadhaarValid=False,
                    aadhaarStatus="INVALID",
                    nameMatch=False
                )
                
        except requests.Timeout:
            logger.error(f"Aadhaar verification timeout for: {aadhaar_number}")
            return AadhaarVerificationResult(
                aadhaarValid=False,
                aadhaarStatus="INVALID",
                nameMatch=False
            )
        
        except requests.RequestException as e:
            logger.error(f"Aadhaar verification request error: {str(e)}")
            return AadhaarVerificationResult(
                aadhaarValid=False,
                aadhaarStatus="INVALID",
                nameMatch=False
            )
        
        except Exception as e:
            logger.error(f"Unexpected error during Aadhaar verification: {str(e)}")
            return AadhaarVerificationResult(
                aadhaarValid=False,
                aadhaarStatus="INVALID",
                nameMatch=False
            )
    
    def verify_identity_match(
        self, 
        pan_name: Optional[str], 
        aadhaar_name: Optional[str]
    ) -> bool:
        """
        Verify if PAN and Aadhaar names match
        
        Args:
            pan_name: Name from PAN card
            aadhaar_name: Name from Aadhaar card
            
        Returns:
            True if names match, False otherwise
        """
        if not pan_name or not aadhaar_name:
            return False
        
        similarity = self.calculate_name_similarity(pan_name, aadhaar_name)
        return similarity >= settings.NAME_SIMILARITY_THRESHOLD
    
    def determine_verification_status(
        self,
        pan_result: PanVerificationResult,
        aadhaar_result: AadhaarVerificationResult,
        identity_match: bool
    ) -> VerificationStatus:
        """
        Determine overall verification status
        
        Args:
            pan_result: PAN verification result
            aadhaar_result: Aadhaar verification result
            identity_match: Whether identities match
            
        Returns:
            Overall verification status
        """
        pan_valid = pan_result.panValid and pan_result.panStatus == "ACTIVE"
        aadhaar_valid = aadhaar_result.aadhaarValid and aadhaar_result.aadhaarStatus in ["VALID", "ACTIVE"]
        
        if pan_valid and aadhaar_valid and identity_match:
            return VerificationStatus.VERIFIED
        elif pan_valid or aadhaar_valid:
            return VerificationStatus.PARTIALLY_VERIFIED
        else:
            return VerificationStatus.FAILED
    
    def verify_kyc(
        self,
        pan_data: PanCardData,
        aadhaar_data: AadhaarCardData
    ) -> Tuple[VerificationStatus, PanVerificationResult, AadhaarVerificationResult, bool]:
        """
        Perform complete KYC verification
        
        Args:
            pan_data: PAN card details
            aadhaar_data: Aadhaar card details
            
        Returns:
            Tuple of (verification_status, pan_result, aadhaar_result, identity_match)
        """
        # Verify PAN
        pan_result = self.verify_pan(
            pan_number=pan_data.panNumber,
            name=pan_data.name
        )
        
        # Verify Aadhaar
        aadhaar_result = self.verify_aadhaar(
            aadhaar_number=aadhaar_data.aadhaarNumber,
            name=aadhaar_data.name
        )
        
        # Verify identity match
        identity_match = self.verify_identity_match(
            pan_name=pan_data.name,
            aadhaar_name=aadhaar_data.name
        )
        
        # Determine overall status
        verification_status = self.determine_verification_status(
            pan_result=pan_result,
            aadhaar_result=aadhaar_result,
            identity_match=identity_match
        )
        
        return verification_status, pan_result, aadhaar_result, identity_match


# Create singleton instance
verification_service = VerificationService()
