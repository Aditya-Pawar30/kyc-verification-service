"""
Response models for KYC Verification Service
"""
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class VerificationStatus(str, Enum):
    """Verification status enum"""
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    FAILED = "FAILED"


class PanVerificationResult(BaseModel):
    """PAN verification result"""
    panValid: bool = Field(..., description="Whether PAN is valid")
    panStatus: str = Field(..., description="PAN status (ACTIVE/INACTIVE/INVALID)")
    nameMatch: bool = Field(..., description="Whether name matches")


class AadhaarVerificationResult(BaseModel):
    """Aadhaar verification result"""
    aadhaarValid: bool = Field(..., description="Whether Aadhaar is valid")
    aadhaarStatus: str = Field(..., description="Aadhaar status")
    nameMatch: bool = Field(..., description="Whether name matches")


class KYCVerificationResponse(BaseModel):
    """Complete KYC verification response"""
    verificationStatus: VerificationStatus = Field(
        ..., 
        description="Overall verification status"
    )
    panVerification: PanVerificationResult = Field(
        ..., 
        description="PAN verification details"
    )
    aadhaarVerification: AadhaarVerificationResult = Field(
        ..., 
        description="Aadhaar verification details"
    )
    identityMatch: bool = Field(
        ..., 
        description="Whether PAN and Aadhaar names match"
    )
    errorMessage: Optional[str] = Field(
        default=None, 
        description="Error message if verification failed"
    )
