from typing import List, Optional
from pydantic import BaseModel


class ExtractedPanCard(BaseModel):
    name: Optional[str] = None
    fatherName: Optional[str] = None
    dob: Optional[str] = None
    panNumber: Optional[str] = None
    rawText: Optional[str] = None


class ExtractedAadhaarCard(BaseModel):
    name: Optional[str] = None
    dob: Optional[str] = None
    aadhaarNumber: Optional[str] = None
    rawText: Optional[str] = None


class MissingFields(BaseModel):
    panCard: List[str]
    aadhaarCard: List[str]


class DocumentExtractionResult(BaseModel):
    panCard: ExtractedPanCard
    aadhaarCard: ExtractedAadhaarCard
    missingFields: MissingFields