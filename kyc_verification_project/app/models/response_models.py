"""
Response models for KYC Verification System
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class VerificationStatus(str, Enum):
    """Verification status enum"""
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    NOT_VERIFIED = "NOT_VERIFIED"


class PanVerificationResult(BaseModel):
    """PAN verification result"""
    panValid: bool = Field(..., description="Whether PAN is valid")
    panStatus: str = Field(..., description="PAN status (ACTIVE/INACTIVE/INVALID)")
    nameMatch: bool = Field(..., description="Whether name matches")
    dobMatch: bool = Field(..., description="Whether DOB matches")
    apiName: Optional[str] = Field(default=None, description="Name returned by API")
    apiDob: Optional[str] = Field(default=None, description="DOB returned by API")


class AadhaarVerificationResult(BaseModel):
    """Aadhaar verification result"""
    aadhaarValid: bool = Field(..., description="Whether Aadhaar is valid")
    aadhaarStatus: str = Field(..., description="Aadhaar status")
    nameMatch: bool = Field(..., description="Whether name matches")
    dobMatch: bool = Field(..., description="Whether DOB matches")
    apiName: Optional[str] = Field(default=None, description="Name returned by API")
    apiDob: Optional[str] = Field(default=None, description="DOB returned by API")


class CrossMatchResult(BaseModel):
    """Cross-match result between PAN and Aadhaar"""
    panVsAadhaarNameMatch: bool = Field(..., description="Whether PAN and Aadhaar names match")
    panVsAadhaarDobMatch: bool = Field(..., description="Whether PAN and Aadhaar DOBs match")


class KYCVerificationResponse(BaseModel):
    """Complete KYC verification response"""
    verificationStatus: VerificationStatus = Field(
        ..., 
        description="Overall verification status"
    )
    isValid: bool = Field(
        ..., 
        description="Whether identity is valid"
    )
    verificationScore: int = Field(
        ..., 
        description="Verification score (0-100)",
        ge=0,
        le=100
    )
    verificationFlags: List[str] = Field(
        default_factory=list,
        description="List of verification flags"
    )
    panVerification: PanVerificationResult = Field(
        ..., 
        description="PAN verification details"
    )
    aadhaarVerification: AadhaarVerificationResult = Field(
        ..., 
        description="Aadhaar verification details"
    )
    crossMatch: CrossMatchResult = Field(
        ..., 
        description="Cross-match details"
    )
    errorMessage: Optional[str] = Field(
        default=None, 
        description="Error message if verification failed"
    )
