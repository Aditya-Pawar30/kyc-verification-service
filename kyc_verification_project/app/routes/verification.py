"""
Verification Routes for KYC Verification System
"""
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
import logging
from typing import Optional

from app.models.request_models import KYCVerificationRequest, PanCardData, AadhaarCardData
from app.models.response_models import KYCVerificationResponse
from app.services.verification_service import verification_service
from app.services.ocr_service import ocr_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/verify", tags=["KYC Verification"])


@router.post(
    "/identity",
    response_model=KYCVerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify identity",
    description="Verify PAN and Aadhaar details using Sandbox.co.in APIs"
)
async def verify_identity(request: KYCVerificationRequest) -> KYCVerificationResponse:
    """
    Verify identity using PAN and Aadhaar details
    
    - **panCard**: PAN card details (name, dob, panNumber)
    - **aadhaarCard**: Aadhaar card details (name, dob, aadhaarNumber)
    
    Returns verification status, score, and detailed results.
    """
    try:
        logger.info("Received KYC verification request")
        
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
        result = verification_service.verify_kyc(
            pan_data=request.panCard,
            aadhaar_data=request.aadhaarCard
        )
        
        # Build response
        response = KYCVerificationResponse(**result)
        
        logger.info(f"KYC verification completed: {result['verificationStatus']}")
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


@router.post(
    "/identity/upload",
    response_model=KYCVerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify identity with image uploads",
    description="Verify PAN and Aadhaar using uploaded images"
)
async def verify_identity_with_upload(
    panImage: Optional[UploadFile] = File(default=None, description="PAN card image file"),
    aadhaarImage: Optional[UploadFile] = File(default=None, description="Aadhaar card image file"),
    panName: Optional[str] = Form(default=None, description="Name on PAN card"),
    panDob: Optional[str] = Form(default=None, description="DOB on PAN card (DD/MM/YYYY)"),
    panNumber: Optional[str] = Form(default=None, description="PAN number"),
    aadhaarName: Optional[str] = Form(default=None, description="Name on Aadhaar card"),
    aadhaarDob: Optional[str] = Form(default=None, description="DOB on Aadhaar card (DD/MM/YYYY)"),
    aadhaarNumber: Optional[str] = Form(default=None, description="Aadhaar number")
) -> KYCVerificationResponse:
    """
    Verify identity using uploaded PAN and Aadhaar images
    
    - **panImage**: PAN card image file
    - **aadhaarImage**: Aadhaar card image file
    - **panName**: Name on PAN card (optional if uploading image)
    - **panDob**: DOB on PAN card (optional if uploading image)
    - **panNumber**: PAN number (optional if uploading image)
    - **aadhaarName**: Name on Aadhaar card (optional if uploading image)
    - **aadhaarDob**: DOB on Aadhaar card (optional if uploading image)
    - **aadhaarNumber**: Aadhaar number (optional if uploading image)
    
    Returns verification status, score, and detailed results.
    """
    try:
        logger.info("Received KYC verification request with file uploads")
        
        # Extract PAN details from image if provided
        pan_data = None
        if panImage:
            pan_bytes = await panImage.read()
            pan_result = ocr_service.process_pan_image(pan_bytes)
            
            if pan_result["success"]:
                extracted = pan_result["data"]
                pan_data = PanCardData(
                    name=panName or extracted.get("name"),
                    dob=panDob or extracted.get("dob"),
                    panNumber=panNumber or extracted.get("panNumber")
                )
            else:
                logger.warning(f"Failed to extract PAN details: {pan_result.get('error')}")
                pan_data = PanCardData(
                    name=panName,
                    dob=panDob,
                    panNumber=panNumber
                )
        else:
            pan_data = PanCardData(
                name=panName,
                dob=panDob,
                panNumber=panNumber
            )
        
        # Extract Aadhaar details from image if provided
        aadhaar_data = None
        if aadhaarImage:
            aadhaar_bytes = await aadhaarImage.read()
            aadhaar_result = ocr_service.process_aadhaar_image(aadhaar_bytes)
            
            if aadhaar_result["success"]:
                extracted = aadhaar_result["data"]
                aadhaar_data = AadhaarCardData(
                    name=aadhaarName or extracted.get("name"),
                    dob=aadhaarDob or extracted.get("dob"),
                    aadhaarNumber=aadhaarNumber or extracted.get("aadhaarNumber")
                )
            else:
                logger.warning(f"Failed to extract Aadhaar details: {aadhaar_result.get('error')}")
                aadhaar_data = AadhaarCardData(
                    name=aadhaarName,
                    dob=aadhaarDob,
                    aadhaarNumber=aadhaarNumber
                )
        else:
            aadhaar_data = AadhaarCardData(
                name=aadhaarName,
                dob=aadhaarDob,
                aadhaarNumber=aadhaarNumber
            )
        
        # Validate required fields
        if not pan_data.panNumber:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PAN number is required (either provide it or upload PAN image)"
            )
        
        if not aadhaar_data.aadhaarNumber:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aadhaar number is required (either provide it or upload Aadhaar image)"
            )
        
        # Perform KYC verification
        result = verification_service.verify_kyc(
            pan_data=pan_data,
            aadhaar_data=aadhaar_data
        )
        
        # Build response
        response = KYCVerificationResponse(**result)
        
        logger.info(f"KYC verification completed: {result['verificationStatus']}")
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
