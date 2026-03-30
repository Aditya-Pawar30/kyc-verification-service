from typing import List, Optional
from pydantic import BaseModel


class MatchSummary(BaseModel):
    nameMatch: bool
    fatherNameConsistency: bool
    dobMatch: bool
    panFormatValid: bool
    aadhaarFormatValid: bool


class FraudDetectionResponse(BaseModel):
    fraudStatus: str
    fraudScore: int
    fraudFlags: List[str]
    fraudType: List[str]
    matchSummary: MatchSummary


class ExtractedData(BaseModel):
    """Extracted data from PAN/Aadhaar cards"""
    name: Optional[str] = None
    fatherName: Optional[str] = None
    dob: Optional[str] = None
    panNumber: Optional[str] = None
    aadhaarNumber: Optional[str] = None


class ProcessAndDetectResponse(BaseModel):
    """Response for process-and-detect endpoint"""
    extractedPan: ExtractedData
    extractedAadhaar: ExtractedData
    fraudResult: FraudDetectionResponse