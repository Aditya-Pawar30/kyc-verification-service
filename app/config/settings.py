"""
Configuration settings for KYC Verification Service
"""
import os
from typing import Optional


class Settings:
    """Application settings and configuration"""
    
    # Sandbox API Configuration
    SANDBOX_API_KEY: str = os.getenv("SANDBOX_API_KEY", "Your sandox api key")
    SANDBOX_API_SECRET: str = os.getenv("SANDBOX_API_SECRET", "Your secret key")
    SANDBOX_BASE_URL: str = "https://sandbox.co.in"
    
    # API Endpoints
    PAN_VERIFICATION_ENDPOINT: str = "/api/v1/pan/verify"
    AADHAAR_VERIFICATION_ENDPOINT: str = "/api/v1/aadhaar/verify"
    
    # Request Configuration
    API_TIMEOUT: int = 30  # seconds
    MAX_RETRIES: int = 3
    
    # Name Matching Configuration
    NAME_SIMILARITY_THRESHOLD: float = 0.8  # 80% similarity required
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required settings are present"""
        if not cls.SANDBOX_API_KEY:
            raise ValueError(
                "SANDBOX_API_KEY environment variable is not set. "
                "Please set it before running the application."
            )
        return True


settings = Settings()
