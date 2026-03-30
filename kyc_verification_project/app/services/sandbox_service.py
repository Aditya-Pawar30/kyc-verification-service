"""
Sandbox API Service for KYC Verification
"""
import requests
import logging
from typing import Optional, Dict, Any
from app.config.settings import settings

logger = logging.getLogger(__name__)


class SandboxService:
    """Service for interacting with Sandbox.co.in APIs"""
    
    def __init__(self):
        """Initialize Sandbox service"""
        self.api_key = settings.SANDBOX_API_KEY
        self.api_secret = settings.SANDBOX_API_SECRET
        self.base_url = settings.SANDBOX_BASE_URL
        self.timeout = settings.API_TIMEOUT
        self.headers = {
            "x-api-key": self.api_key,
            "x-api-secret": self.api_secret,
            "Content-Type": "application/json"
        }
    
    def verify_pan(self, pan_number: str) -> Dict[str, Any]:
        """
        Verify PAN number using Sandbox API
        
        Args:
            pan_number: PAN number to verify
            
        Returns:
            Dictionary with verification results
        """
        try:
            url = f"{self.base_url}{settings.PAN_VERIFICATION_ENDPOINT}"
            payload = {"pan": pan_number}
            
            logger.info(f"Verifying PAN: {pan_number}")
            
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"PAN verification successful for: {pan_number}")
                return {
                    "success": True,
                    "data": data,
                    "error": None
                }
            
            elif response.status_code == 404:
                logger.warning(f"PAN not found: {pan_number}")
                return {
                    "success": False,
                    "data": None,
                    "error": "PAN not found"
                }
            
            else:
                logger.error(f"PAN verification API error: {response.status_code}")
                return {
                    "success": False,
                    "data": None,
                    "error": f"API error: {response.status_code}"
                }
                
        except requests.Timeout:
            logger.error(f"PAN verification timeout for: {pan_number}")
            return {
                "success": False,
                "data": None,
                "error": "Request timeout"
            }
        
        except requests.RequestException as e:
            logger.error(f"PAN verification request error: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": f"Request error: {str(e)}"
            }
        
        except Exception as e:
            logger.error(f"Unexpected error during PAN verification: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def verify_aadhaar(self, aadhaar_number: str) -> Dict[str, Any]:
        """
        Verify Aadhaar number using Sandbox API
        
        Args:
            aadhaar_number: Aadhaar number to verify
            
        Returns:
            Dictionary with verification results
        """
        try:
            url = f"{self.base_url}{settings.AADHAAR_VERIFICATION_ENDPOINT}"
            payload = {"aadhaar": aadhaar_number}
            
            logger.info(f"Verifying Aadhaar: {aadhaar_number}")
            
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Aadhaar verification successful for: {aadhaar_number}")
                return {
                    "success": True,
                    "data": data,
                    "error": None
                }
            
            elif response.status_code == 404:
                logger.warning(f"Aadhaar not found: {aadhaar_number}")
                return {
                    "success": False,
                    "data": None,
                    "error": "Aadhaar not found"
                }
            
            else:
                logger.error(f"Aadhaar verification API error: {response.status_code}")
                return {
                    "success": False,
                    "data": None,
                    "error": f"API error: {response.status_code}"
                }
                
        except requests.Timeout:
            logger.error(f"Aadhaar verification timeout for: {aadhaar_number}")
            return {
                "success": False,
                "data": None,
                "error": "Request timeout"
            }
        
        except requests.RequestException as e:
            logger.error(f"Aadhaar verification request error: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": f"Request error: {str(e)}"
            }
        
        except Exception as e:
            logger.error(f"Unexpected error during Aadhaar verification: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": f"Unexpected error: {str(e)}"
            }


# Create singleton instance
sandbox_service = SandboxService()
