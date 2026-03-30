# KYC Verification Service

A standalone KYC Verification Service using Python and FastAPI that integrates with Sandbox.co.in APIs to verify PAN and Aadhaar details.

## Overview

This service acts as a verification layer that takes PAN and Aadhaar details (already extracted from documents), calls Sandbox APIs, and verifies whether the details are valid and authentic.

## Project Structure

```
app/
├── config/
│   └── settings.py              # API configuration and settings
├── models/
│   ├── request_models.py        # Request validation models
│   └── verification_response_models.py  # Response models
├── routes/
│   └── verification.py          # API endpoints
├── services/
│   └── verification_service.py  # Core verification logic
└── main.py                      # FastAPI application entry point
```

## Features

### PAN Verification
- Validates PAN number format (10 characters)
- Calls Sandbox PAN verification API
- Checks PAN status (ACTIVE/INACTIVE/INVALID)
- Verifies name matching with configurable similarity threshold

### Aadhaar Verification
- Validates Aadhaar number format (12 digits)
- Calls Sandbox Aadhaar verification API
- Checks Aadhaar status
- Verifies name matching

### Identity Matching
- Compares PAN and Aadhaar names
- Normalizes names (removes prefixes, extra spaces)
- Uses sequence matching for fuzzy comparison
- Configurable similarity threshold (default: 80%)

### Verification Status
- **VERIFIED**: Both PAN and Aadhaar valid and consistent
- **PARTIALLY_VERIFIED**: One valid, one invalid
- **FAILED**: Both invalid or mismatch

## API Endpoint

### POST /verify/kyc

Verify KYC details (PAN and Aadhaar)

**Request Body:**
```json
{
  "panCard": {
    "name": "RAHUL SHARMA",
    "dob": "01/01/1998",
    "panNumber": "ABCDE1234F"
  },
  "aadhaarCard": {
    "name": "RAHUL SHARMA",
    "aadhaarNumber": "123412341234"
  }
}
```

**Response:**
```json
{
  "verificationStatus": "VERIFIED",
  "panVerification": {
    "panValid": true,
    "panStatus": "ACTIVE",
    "nameMatch": true
  },
  "aadhaarVerification": {
    "aadhaarValid": true,
    "aadhaarStatus": "VALID",
    "nameMatch": true
  },
  "identityMatch": true
}
```

### GET /verify/health

Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "KYC Verification"
}
```

## Configuration

### Environment Variables

Set the following environment variable before running the application:

```bash
export SANDBOX_API_KEY="your_sandbox_api_key_here"
```

### Settings

Configuration is managed in `app/config/settings.py`:

- `SANDBOX_API_KEY`: API key for Sandbox.co.in
- `SANDBOX_BASE_URL`: Base URL for Sandbox API (default: https://sandbox.co.in)
- `API_TIMEOUT`: Request timeout in seconds (default: 30)
- `NAME_SIMILARITY_THRESHOLD`: Minimum similarity score for name matching (default: 0.8)

## Installation

1. Install dependencies:
```bash
pip install fastapi uvicorn requests pydantic
```

2. Set environment variable:
```bash
export SANDBOX_API_KEY="your_sandbox_api_key_here"
```

3. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/verify/kyc" \
  -H "Content-Type: application/json" \
  -d '{
    "panCard": {
      "name": "RAHUL SHARMA",
      "dob": "01/01/1998",
      "panNumber": "ABCDE1234F"
    },
    "aadhaarCard": {
      "name": "RAHUL SHARMA",
      "aadhaarNumber": "123412341234"
    }
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/verify/kyc"
payload = {
    "panCard": {
        "name": "RAHUL SHARMA",
        "dob": "01/01/1998",
        "panNumber": "ABCDE1234F"
    },
    "aadhaarCard": {
        "name": "RAHUL SHARMA",
        "aadhaarNumber": "123412341234"
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

## Error Handling

The service handles the following error scenarios:

- **Invalid PAN format**: Returns INVALID status
- **Invalid Aadhaar format**: Returns INVALID status
- **API timeout**: Returns INVALID status with error logging
- **API errors**: Returns INVALID status with error logging
- **Missing required fields**: Returns 400 Bad Request
- **Internal errors**: Returns 500 Internal Server Error

## Name Normalization

The service normalizes names before comparison:

1. Converts to uppercase
2. Removes extra spaces
3. Removes common prefixes (MR., MRS., MS., DR., SHRI, SMT., KUMARI)
4. Removes common suffixes (JR, SR, I, II, III)

## Testing

Run the test suite:

```bash
python test_kyc_verification.py
```

Tests cover:
- Name normalization
- Name similarity calculation
- PAN verification
- Aadhaar verification
- Identity matching
- Request models
- Full KYC verification flow

## Dependencies

- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **Requests**: HTTP client for API calls
- **Uvicorn**: ASGI server

## Notes

- This service is separate from the fraud detection engine
- It acts as a verification layer after fraud analysis
- API key must be set as environment variable
- SSL certificate verification may need to be configured for production
- The service uses Sandbox.co.in API format

## License

Part of the fraud detection project.
