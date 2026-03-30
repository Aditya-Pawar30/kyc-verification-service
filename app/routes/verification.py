"""
KYC Verification Routes
"""
from fastapi import APIRouter, HTTPException, status
import logging

from app.models.request_models import KYCVerificationRequest
from app.models.verification_response_models import KYCVerificationResponse
from app.services.verification_service import verification_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/verify", tags=["KYC Verification"])


@router.post(
    "/kyc",
    response_model=KYCVerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify KYC details",
    description="Verify PAN and Aadhaar details using Sandbox.co.in APIs"
)
async def verify_kyc(request: KYCVerificationRequest) -> KYCVerificationResponse:
    """
    Verify KYC details (PAN and Aadhaar)
    
    - **panCard**: PAN card details (name, dob, panNumber)
    - **aadhaarCard**: Aadhaar card details (name, aadhaarNumber)
    
    Returns verification status and details for both PAN and Aadhaar.
    """
    try:
        logger.info(f"Received KYC verification request")
        
        # Validate required fields
        if not request.panCard.panNumber:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PAN number is required"
            )
        
        if not request.aadhaarCard.aadhaarNumber:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aadhaar number is required"
            )
        
        # Perform KYC verification
        verification_status, pan_result, aadhaar_result, identity_match = (
            verification_service.verify_kyc(
                pan_data=request.panCard,
                aadhaar_data=request.aadhaarCard
            )
        )
        
        # Build response
        response = KYCVerificationResponse(
            verificationStatus=verification_status,
            panVerification=pan_result,
            aadhaarVerification=aadhaar_result,
            identityMatch=identity_match
        )
        
        logger.info(f"KYC verification completed: {verification_status}")
        return response
        
    except HTTPException:
        raise
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        logger.error(f"Unexpected error during KYC verification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during KYC verification"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if verification service is running"
)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "KYC Verification"}
