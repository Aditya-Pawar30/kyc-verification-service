"""
Scoring Service for KYC Verification
"""
from typing import List, Dict, Any
from app.config.settings import settings


class ScoringService:
    """Service for calculating verification scores"""
    
    def calculate_verification_score(
        self,
        pan_valid: bool,
        pan_name_match: bool,
        pan_dob_match: bool,
        aadhaar_valid: bool,
        aadhaar_name_match: bool,
        aadhaar_dob_match: bool
    ) -> int:
        """
        Calculate verification score based on verification results
        
        Args:
            pan_valid: Whether PAN is valid
            pan_name_match: Whether PAN name matches
            pan_dob_match: Whether PAN DOB matches
            aadhaar_valid: Whether Aadhaar is valid
            aadhaar_name_match: Whether Aadhaar name matches
            aadhaar_dob_match: Whether Aadhaar DOB matches
            
        Returns:
            Verification score (0-100)
        """
        score = 0
        
        # PAN verification score
        if pan_valid:
            score += settings.PAN_VERIFIED_SCORE
            
            # PAN name match bonus
            if pan_name_match:
                score += settings.PAN_NAME_MATCH_SCORE
            
            # PAN DOB match bonus (if DOB is provided)
            if pan_dob_match:
                score += 5  # Small bonus for DOB match
        
        # Aadhaar verification score
        if aadhaar_valid:
            score += settings.AADHAAR_VERIFIED_SCORE
            
            # Aadhaar name match bonus
            if aadhaar_name_match:
                score += settings.AADHAAR_NAME_MATCH_SCORE
            
            # Aadhaar DOB match bonus (if DOB is provided)
            if aadhaar_dob_match:
                score += 5  # Small bonus for DOB match
        
        # Cap score at 100
        return min(score, 100)
    
    def determine_verification_status(self, score: int) -> str:
        """
        Determine verification status based on score
        
        Args:
            score: Verification score
            
        Returns:
            Verification status string
        """
        if score >= settings.VERIFIED_THRESHOLD:
            return "VERIFIED"
        elif score >= settings.PARTIALLY_VERIFIED_THRESHOLD:
            return "PARTIALLY_VERIFIED"
        else:
            return "NOT_VERIFIED"
    
    def is_valid_identity(self, status: str) -> bool:
        """
        Determine if identity is valid based on status
        
        Args:
            status: Verification status
            
        Returns:
            True if identity is valid
        """
        return status == "VERIFIED"
    
    def generate_verification_flags(
        self,
        pan_valid: bool,
        pan_name_match: bool,
        pan_dob_match: bool,
        aadhaar_valid: bool,
        aadhaar_name_match: bool,
        aadhaar_dob_match: bool,
        pan_api_error: bool,
        aadhaar_api_error: bool,
        cross_name_match: bool,
        cross_dob_match: bool,
        has_pan_dob: bool,
        has_aadhaar_dob: bool
    ) -> List[str]:
        """
        Generate verification flags based on results
        
        Args:
            pan_valid: Whether PAN is valid
            pan_name_match: Whether PAN name matches
            pan_dob_match: Whether PAN DOB matches
            aadhaar_valid: Whether Aadhaar is valid
            aadhaar_name_match: Whether Aadhaar name matches
            aadhaar_dob_match: Whether Aadhaar DOB matches
            pan_api_error: Whether PAN API call failed
            aadhaar_api_error: Whether Aadhaar API call failed
            cross_name_match: Whether PAN and Aadhaar names match
            cross_dob_match: Whether PAN and Aadhaar DOBs match
            has_pan_dob: Whether PAN DOB was provided
            has_aadhaar_dob: Whether Aadhaar DOB was provided
            
        Returns:
            List of verification flags
        """
        flags = []
        
        # PAN flags
        if not pan_valid:
            flags.append("invalid_pan")
        elif pan_api_error:
            flags.append("pan_api_error")
        elif not pan_name_match:
            flags.append("pan_name_mismatch")
        elif has_pan_dob and not pan_dob_match:
            flags.append("pan_dob_mismatch")
        
        # Aadhaar flags
        if not aadhaar_valid:
            flags.append("invalid_aadhaar")
        elif aadhaar_api_error:
            flags.append("aadhaar_api_error")
        elif not aadhaar_name_match:
            flags.append("aadhaar_name_mismatch")
        elif has_aadhaar_dob and not aadhaar_dob_match:
            flags.append("aadhaar_dob_mismatch")
        
        # Cross-match flags
        if pan_valid and aadhaar_valid:
            if not cross_name_match:
                flags.append("cross_name_mismatch")
            if not cross_dob_match:
                flags.append("cross_dob_mismatch")
        
        # Incomplete input flags
        if not has_pan_dob:
            flags.append("pan_dob_unavailable")
        if not has_aadhaar_dob:
            flags.append("aadhaar_dob_unavailable")
        
        return flags


# Create singleton instance
scoring_service = ScoringService()
