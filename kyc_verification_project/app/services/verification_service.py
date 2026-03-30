"""
Verification Service for KYC Verification System
"""
import logging
from typing import Tuple, Dict, Any
from app.models.request_models import PanCardData, AadhaarCardData
from app.models.response_models import (
    PanVerificationResult,
    AadhaarVerificationResult,
    CrossMatchResult,
    VerificationStatus
)
from app.services.sandbox_service import sandbox_service
from app.services.comparison_service import comparison_service
from app.services.scoring_service import scoring_service
from app.utils.helpers import validate_pan_format, validate_aadhaar_format

logger = logging.getLogger(__name__)


class VerificationService:
    """Service for KYC verification"""
    
    def verify_pan(
        self,
        pan_data: PanCardData
    ) -> Tuple[PanVerificationResult, bool]:
        """
        Verify PAN card details
        
        Args:
            pan_data: PAN card data
            
        Returns:
            Tuple of (PanVerificationResult, api_error_flag)
        """
        api_error = False
        
        # Validate PAN format
        if not validate_pan_format(pan_data.panNumber):
            return PanVerificationResult(
                panValid=False,
                panStatus="INVALID",
                nameMatch=False,
                dobMatch=False,
                apiName=None,
                apiDob=None
            ), api_error
        
        # Call Sandbox API
        result = sandbox_service.verify_pan(pan_data.panNumber)
        
        if not result["success"]:
            api_error = True
            return PanVerificationResult(
                panValid=False,
                panStatus="INVALID",
                nameMatch=False,
                dobMatch=False,
                apiName=None,
                apiDob=None
            ), api_error
        
        # Extract API data
        api_data = result["data"]
        api_name = api_data.get("name", "")
        api_dob = api_data.get("dob", "")
        api_status = api_data.get("status", "INVALID").upper()
        
        # Compare details
        comparison = comparison_service.compare_pan_details(
            input_name=pan_data.name,
            input_dob=pan_data.dob,
            api_name=api_name,
            api_dob=api_dob
        )
        
        return PanVerificationResult(
            panValid=True,
            panStatus=api_status,
            nameMatch=comparison["nameMatch"],
            dobMatch=comparison["dobMatch"],
            apiName=api_name,
            apiDob=api_dob
        ), api_error
    
    def verify_aadhaar(
        self,
        aadhaar_data: AadhaarCardData
    ) -> Tuple[AadhaarVerificationResult, bool]:
        """
        Verify Aadhaar card details
        
        Args:
            aadhaar_data: Aadhaar card data
            
        Returns:
            Tuple of (AadhaarVerificationResult, api_error_flag)
        """
        api_error = False
        
        # Validate Aadhaar format
        if not validate_aadhaar_format(aadhaar_data.aadhaarNumber):
            return AadhaarVerificationResult(
                aadhaarValid=False,
                aadhaarStatus="INVALID",
                nameMatch=False,
                dobMatch=False,
                apiName=None,
                apiDob=None
            ), api_error
        
        # Call Sandbox API
        result = sandbox_service.verify_aadhaar(aadhaar_data.aadhaarNumber)
        
        if not result["success"]:
            api_error = True
            return AadhaarVerificationResult(
                aadhaarValid=False,
                aadhaarStatus="INVALID",
                nameMatch=False,
                dobMatch=False,
                apiName=None,
                apiDob=None
            ), api_error
        
        # Extract API data
        api_data = result["data"]
        api_name = api_data.get("name", "")
        api_dob = api_data.get("dob", "")
        api_status = api_data.get("status", "INVALID").upper()
        
        # Compare details
        comparison = comparison_service.compare_aadhaar_details(
            input_name=aadhaar_data.name,
            input_dob=aadhaar_data.dob,
            api_name=api_name,
            api_dob=api_dob
        )
        
        return AadhaarVerificationResult(
            aadhaarValid=True,
            aadhaarStatus=api_status,
            nameMatch=comparison["nameMatch"],
            dobMatch=comparison["dobMatch"],
            apiName=api_name,
            apiDob=api_dob
        ), api_error
    
    def verify_kyc(
        self,
        pan_data: PanCardData,
        aadhaar_data: AadhaarCardData
    ) -> Dict[str, Any]:
        """
        Perform complete KYC verification
        
        Args:
            pan_data: PAN card details
            aadhaar_data: Aadhaar card details
            
        Returns:
            Dictionary with complete verification results
        """
        # Verify PAN
        pan_result, pan_api_error = self.verify_pan(pan_data)
        
        # Verify Aadhaar
        aadhaar_result, aadhaar_api_error = self.verify_aadhaar(aadhaar_data)
        
        # Cross-match PAN and Aadhaar
        cross_match_data = comparison_service.cross_match_details(
            pan_name=pan_data.name,
            pan_dob=pan_data.dob,
            aadhaar_name=aadhaar_data.name,
            aadhaar_dob=aadhaar_data.dob
        )
        cross_match = CrossMatchResult(**cross_match_data)
        
        # Calculate verification score
        score = scoring_service.calculate_verification_score(
            pan_valid=pan_result.panValid,
            pan_name_match=pan_result.nameMatch,
            pan_dob_match=pan_result.dobMatch,
            aadhaar_valid=aadhaar_result.aadhaarValid,
            aadhaar_name_match=aadhaar_result.nameMatch,
            aadhaar_dob_match=aadhaar_result.dobMatch
        )
        
        # Determine verification status
        status = scoring_service.determine_verification_status(score)
        
        # Determine if identity is valid
        is_valid = scoring_service.is_valid_identity(status)
        
        # Generate verification flags
        flags = scoring_service.generate_verification_flags(
            pan_valid=pan_result.panValid,
            pan_name_match=pan_result.nameMatch,
            pan_dob_match=pan_result.dobMatch,
            aadhaar_valid=aadhaar_result.aadhaarValid,
            aadhaar_name_match=aadhaar_result.nameMatch,
            aadhaar_dob_match=aadhaar_result.dobMatch,
            pan_api_error=pan_api_error,
            aadhaar_api_error=aadhaar_api_error,
            cross_name_match=cross_match.panVsAadhaarNameMatch,
            cross_dob_match=cross_match.panVsAadhaarDobMatch,
            has_pan_dob=bool(pan_data.dob),
            has_aadhaar_dob=bool(aadhaar_data.dob)
        )
        
        return {
            "verificationStatus": status,
            "isValid": is_valid,
            "verificationScore": score,
            "verificationFlags": flags,
            "panVerification": pan_result.dict(),
            "aadhaarVerification": aadhaar_result.dict(),
            "crossMatch": cross_match.dict()
        }


# Create singleton instance
verification_service = VerificationService()
