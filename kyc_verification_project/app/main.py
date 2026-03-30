"""
KYC Verification System - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes.verification import router as verification_router

app = FastAPI(
    title="KYC Verification System",
    description="Standalone KYC identity verification system using Sandbox.co.in APIs",
    version="1.0.0"
)

app.include_router(verification_router)


@app.get("/")
async def root():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs")
