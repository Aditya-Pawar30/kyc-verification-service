"""
Comparison Service for KYC Verification
"""
from typing import Optional, Dict, Any
from app.utils.helpers import compare_names, compare_dobs
from app.config.settings import settings


class ComparisonService:
    """Service for comparing PAN and Aadhaar details"""
    
    def compare_pan_details(
        self,
        input_name: Optional[str],
        input_dob: Optional[str],
        api_name: Optional[str],
        api_dob: Optional[str]
    ) -> Dict[str, Any]:
        """
        Compare PAN input details with API returned details
        
        Args:
            input_name: Name from input
            input_dob: DOB from input
            api_name: Name from API
            api_dob: DOB from API
            
        Returns:
            Dictionary with comparison results
        """
        name_match = compare_names(input_name, api_name, settings.NAME_SIMILARITY_THRESHOLD)
        dob_match = compare_dobs(input_dob, api_dob)
        
        return {
            "nameMatch": name_match,
            "dobMatch": dob_match,
            "apiName": api_name,
            "apiDob": api_dob
        }
    
    def compare_aadhaar_details(
        self,
        input_name: Optional[str],
        input_dob: Optional[str],
        api_name: Optional[str],
        api_dob: Optional[str]
    ) -> Dict[str, Any]:
        """
        Compare Aadhaar input details with API returned details
        
        Args:
            input_name: Name from input
            input_dob: DOB from input
            api_name: Name from API
            api_dob: DOB from API
            
        Returns:
            Dictionary with comparison results
        """
        name_match = compare_names(input_name, api_name, settings.NAME_SIMILARITY_THRESHOLD)
        dob_match = compare_dobs(input_dob, api_dob)
        
        return {
            "nameMatch": name_match,
            "dobMatch": dob_match,
            "apiName": api_name,
            "apiDob": api_dob
        }
    
    def cross_match_details(
        self,
        pan_name: Optional[str],
        pan_dob: Optional[str],
        aadhaar_name: Optional[str],
        aadhaar_dob: Optional[str]
    ) -> Dict[str, Any]:
        """
        Cross-match PAN and Aadhaar details
        
        Args:
            pan_name: Name from PAN
            pan_dob: DOB from PAN
            aadhaar_name: Name from Aadhaar
            aadhaar_dob: DOB from Aadhaar
            
        Returns:
            Dictionary with cross-match results
        """
        name_match = compare_names(pan_name, aadhaar_name, settings.NAME_SIMILARITY_THRESHOLD)
        dob_match = compare_dobs(pan_dob, aadhaar_dob)
        
        return {
            "panVsAadhaarNameMatch": name_match,
            "panVsAadhaarDobMatch": dob_match
        }


# Create singleton instance
comparison_service = ComparisonService()
