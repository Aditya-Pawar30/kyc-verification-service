from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.orchestration.process_and_detect_service import ProcessAndDetectService

router = APIRouter()


@router.post("/process-and-detect")
async def process_and_detect(
    panFile: UploadFile = File(...),
    aadhaarFile: UploadFile = File(...)
):
    allowed_extensions = (".png", ".jpg", ".jpeg", ".pdf")

    if not panFile.filename or not panFile.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Invalid PAN file type")

    if not aadhaarFile.filename or not aadhaarFile.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Invalid Aadhaar file type")

    return await ProcessAndDetectService.process_files(panFile, aadhaarFile)