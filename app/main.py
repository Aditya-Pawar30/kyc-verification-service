from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.routes.fraud import router as fraud_router
from app.routes.process_and_detect import router as process_router
from app.routes.verification import router as verification_router

app = FastAPI(
    title="Offline KYC Fraud Detection API",
    description="Standalone fraud detection engine for PAN and Aadhaar comparison",
    version="1.0.0"
)

app.include_router(fraud_router)
app.include_router(process_router)
app.include_router(verification_router)

# Mount static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
async def root():
    # Serve the frontend HTML file
    frontend_file = frontend_path / "index.html"
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    return RedirectResponse(url="/docs")