from fastapi import APIRouter
from app.models.request_models import FraudDetectionRequest
from app.models.response_models import FraudDetectionResponse
from app.services.fraud_detection.fraud_detection_service import FraudDetectionService

router = APIRouter()


@router.post("/detect-fraud", response_model=FraudDetectionResponse)
def detect_fraud(request_data: FraudDetectionRequest):
    return FraudDetectionService.detect_fraud(request_data)