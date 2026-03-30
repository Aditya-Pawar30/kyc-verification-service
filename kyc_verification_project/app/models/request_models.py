"""
Request models for KYC Verification System
"""
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import UploadFile


class PanCardData(BaseModel):
    """PAN card data model"""
    name: Optional[str] = Field(default=None, description="Name on PAN card")
    dob: Optional[str] = Field(default=None, description="Date of birth on PAN card (DD/MM/YYYY)")
    panNumber: Optional[str] = Field(default=None, description="PAN number")


class AadhaarCardData(BaseModel):
    """Aadhaar card data model"""
    name: Optional[str] = Field(default=None, description="Name on Aadhaar card")
    dob: Optional[str] = Field(default=None, description="Date of birth on Aadhaar card (DD/MM/YYYY)")
    aadhaarNumber: Optional[str] = Field(default=None, description="Aadhaar number")


class KYCVerificationRequest(BaseModel):
    """KYC verification request model"""
    panCard: PanCardData = Field(..., description="PAN card details")
    aadhaarCard: AadhaarCardData = Field(..., description="Aadhaar card details")


class KYCVerificationWithFilesRequest(BaseModel):
    """KYC verification request with file uploads"""
    panCard: Optional[PanCardData] = Field(default=None, description="PAN card details (optional if uploading image)")
    aadhaarCard: Optional[AadhaarCardData] = Field(default=None, description="Aadhaar card details (optional if uploading image)")
    panImage: Optional[UploadFile] = Field(default=None, description="PAN card image file")
    aadhaarImage: Optional[UploadFile] = Field(default=None, description="Aadhaar card image file")
