"""
Configuration settings for KYC Verification System
"""
import os
from typing import Optional


class Settings:
    """Application settings and configuration"""
    
    # Sandbox API Configuration
    SANDBOX_API_KEY: str = os.getenv("SANDBOX_API_KEY", "key_live_8451e4a94072438a95712f2364df411d")
    SANDBOX_API_SECRET: str = os.getenv("SANDBOX_API_SECRET", "secret_live_478ab0e0c04c453d96976e93d5af535b")
    SANDBOX_BASE_URL: str = "https://sandbox.co.in"
    
    # API Endpoints
    PAN_VERIFICATION_ENDPOINT: str = "/api/v1/pan/verify"
    AADHAAR_VERIFICATION_ENDPOINT: str = "/api/v1/aadhaar/verify"
    
    # Request Configuration
    API_TIMEOUT: int = 30  # seconds
    MAX_RETRIES: int = 3
    
    # Name Matching Configuration
    NAME_SIMILARITY_THRESHOLD: float = 0.75  # 75% similarity required
    
    # Scoring Configuration
    PAN_VERIFIED_SCORE: int = 40
    AADHAAR_VERIFIED_SCORE: int = 40
    PAN_NAME_MATCH_SCORE: int = 10
    AADHAAR_NAME_MATCH_SCORE: int = 10
    
    # Status Thresholds
    VERIFIED_THRESHOLD: int = 80
    PARTIALLY_VERIFIED_THRESHOLD: int = 50
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required settings are present"""
        if not cls.SANDBOX_API_KEY:
            raise ValueError(
                "SANDBOX_API_KEY environment variable is not set. "
                "Please set it before running the application."
            )
        if not cls.SANDBOX_API_SECRET:
            raise ValueError(
                "SANDBOX_API_SECRET environment variable is not set. "
                "Please set it before running the application."
            )
        return True


settings = Settings()
