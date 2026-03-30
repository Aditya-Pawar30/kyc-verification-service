from typing import Optional
from pydantic import BaseModel, Field


class PanCardData(BaseModel):
    name: Optional[str] = Field(default=None, description="Name on PAN card")
    fatherName: Optional[str] = Field(default=None, description="Father name on PAN card")
    dob: Optional[str] = Field(default=None, description="Date of birth on PAN card")
    panNumber: Optional[str] = Field(default=None, description="PAN number")


class AadhaarCardData(BaseModel):
    name: Optional[str] = Field(default=None, description="Name on Aadhaar card")
    dob: Optional[str] = Field(default=None, description="Date of birth on Aadhaar card")
    aadhaarNumber: Optional[str] = Field(default=None, description="Aadhaar number")


class FraudDetectionRequest(BaseModel):
    panCard: PanCardData
    aadhaarCard: AadhaarCardData


class KYCVerificationRequest(BaseModel):
    """Request model for KYC verification"""
    panCard: PanCardData = Field(..., description="PAN card details")
    aadhaarCard: AadhaarCardData = Field(..., description="Aadhaar card details")