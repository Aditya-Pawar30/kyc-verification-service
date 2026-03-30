# KYC Verification System

A standalone KYC identity verification system using Python and FastAPI that integrates with Sandbox.co.in APIs to verify PAN and Aadhaar details.

## Overview

This system verifies a person's PAN card and Aadhaar card using Sandbox.co.in APIs. It compares returned details with user-provided details, generates a verification score, and returns a final status indicating whether the identity is valid or suspicious.

## Project Structure

```
kyc_verification_project/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── routes/
│   │   └── verification.py        # API endpoints
│   ├── services/
│   │   ├── sandbox_service.py     # Sandbox API client
│   │   ├── verification_service.py # Verification orchestration
│   │   ├── comparison_service.py  # Name/DOB comparison
│   │   └── scoring_service.py     # Score calculation
│   ├── models/
│   │   ├── request_models.py      # Request validation models
│   │   └── response_models.py     # Response models
│   ├── config/
│   │   └── settings.py            # Configuration settings
│   └── utils/
│       └── helpers.py             # Utility functions
├── .env                           # Environment variables
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Features

### PAN Verification
- Validates PAN number format (5 letters + 4 digits + 1 letter)
- Calls Sandbox PAN verification API
- Checks PAN status (ACTIVE/INACTIVE/INVALID)
- Compares name and DOB with API returned data

### Aadhaar Verification
- Validates Aadhaar number format (12 digits)
- Calls Sandbox Aadhaar verification API
- Checks Aadhaar status
- Compares name and DOB with API returned data

### Name Matching
- Normalizes names (removes prefixes, extra spaces)
- Uses fuzzy matching with configurable threshold (default: 75%)
- Compares input names with API returned names

### DOB Matching
- Normalizes date formats (DD/MM/YYYY, DD-MM-YYYY, etc.)
- Compares input DOB with API returned DOB

### Verification Score
- Calculates score from 0 to 100
- PAN verified: +40 points
- Aadhaar verified: +40 points
- PAN name match: +10 points
- Aadhaar name match: +10 points
- DOB matches: +5 points each

### Verification Status
- **VERIFIED**: Score 80-100 (isValid = true)
- **PARTIALLY_VERIFIED**: Score 50-79 (isValid = false)
- **NOT_VERIFIED**: Score 0-49 (isValid = false)

### Verification Flags
- `invalid_pan` - PAN number is invalid
- `invalid_aadhaar` - Aadhaar number is invalid
- `pan_name_mismatch` - PAN name doesn't match API
- `aadhaar_name_mismatch` - Aadhaar name doesn't match API
- `pan_dob_mismatch` - PAN DOB doesn't match API
- `aadhaar_dob_mismatch` - Aadhaar DOB doesn't match API
- `pan_api_error` - PAN API call failed
- `aadhaar_api_error` - Aadhaar API call failed
- `cross_name_mismatch` - PAN and Aadhaar names don't match
- `cross_dob_mismatch` - PAN and Aadhaar DOBs don't match
- `pan_dob_unavailable` - PAN DOB not provided
- `aadhaar_dadhaar_dob_unavailable` - Aadhaar DOB not provided

## API Endpoints

### POST /verify/identity

Verify identity using PAN and Aadhaar details (JSON input)

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
    "dob": "01/01/1998",
    "aadhaarNumber": "123412341234"
  }
}
```

**Response:**
```json
{
  "verificationStatus": "VERIFIED",
  "isValid": true,
  "verificationScore": 92,
  "verificationFlags": [],
  "panVerification": {
    "panValid": true,
    "panStatus": "ACTIVE",
    "nameMatch": true,
    "dobMatch": true,
    "apiName": "RAHUL SHARMA",
    "apiDob": "01/01/1998"
  },
  "aadhaarVerification": {
    "aadhaarValid": true,
    "aadhaarStatus": "VALID",
    "nameMatch": true,
    "dobMatch": true,
    "apiName": "RAHUL SHARMA",
    "apiDob": "01/01/1998"
  },
  "crossMatch": {
    "panVsAadhaarNameMatch": true,
    "panVsAadhaarDobMatch": true
  }
}
```

### POST /verify/identity/upload

Verify identity using uploaded PAN and Aadhaar images

**Request (multipart/form-data):**
- `panImage`: PAN card image file
- `aadhaarImage`: Aadhaar card image file
- `panName`: Name on PAN card (optional)
- `panDob`: DOB on PAN card (optional)
- `panNumber`: PAN number (optional)
- `aadhaarName`: Name on Aadhaar card (optional)
- `aadhaarDob`: DOB on Aadhaar card (optional)
- `aadhaarNumber`: Aadhaar number (optional)

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/verify/identity/upload" \
  -F "panImage=@/path/to/pan_card.jpg" \
  -F "aadhaarImage=@/path/to/aadhaar_card.jpg"
```

**Example using Python requests:**
```python
import requests

url = "http://localhost:8000/verify/identity/upload"
files = {
    'panImage': open('pan_card.jpg', 'rb'),
    'aadhaarImage': open('aadhaar_card.jpg', 'rb')
}

response = requests.post(url, files=files)
print(response.json())
```

**Response:** Same as POST /verify/identity

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

Set the following environment variables in `.env` file:

```bash
SANDBOX_API_KEY=key_live_8451e4a94072438a95712f2364df411d
SANDBOX_API_SECRET=secret_live_478ab0e0c04c453d96976e93d5af535b
```

### Settings

Configuration is managed in `app/config/settings.py`:

- `SANDBOX_API_KEY`: API key for Sandbox.co.in
- `SANDBOX_API_SECRET`: API secret for Sandbox.co.in
- `SANDBOX_BASE_URL`: Base URL for Sandbox API
- `API_TIMEOUT`: Request timeout in seconds (default: 30)
- `NAME_SIMILARITY_THRESHOLD`: Minimum similarity score for name matching (default: 0.75)
- `PAN_VERIFIED_SCORE`: Score for PAN verification (default: 40)
- `AADHAAR_VERIFIED_SCORE`: Score for Aadhaar verification (default: 40)
- `PAN_NAME_MATCH_SCORE`: Score for PAN name match (default: 10)
- `AADHAAR_NAME_MATCH_SCORE`: Score for Aadhaar name match (default: 10)
- `VERIFIED_THRESHOLD`: Minimum score for VERIFIED status (default: 80)
- `PARTIALLY_VERIFIED_THRESHOLD`: Minimum score for PARTIALLY_VERIFIED status (default: 50)

## Installation

1. Navigate to project directory:
```bash
cd kyc_verification_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/verify/identity" \
  -H "Content-Type: application/json" \
  -d '{
    "panCard": {
      "name": "RAHUL SHARMA",
      "dob": "01/01/1998",
      "panNumber": "ABCDE1234F"
    },
    "aadhaarCard": {
      "name": "RAHUL SHARMA",
      "dob": "01/01/1998",
      "aadhaarNumber": "123412341234"
    }
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/verify/identity"
payload = {
    "panCard": {
        "name": "RAHUL SHARMA",
        "dob": "01/01/1998",
        "panNumber": "ABCDE1234F"
    },
    "aadhaarCard": {
        "name": "RAHUL SHARMA",
        "dob": "01/01/1998",
        "aadhaarNumber": "123412341234"
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

## Error Handling

The system handles the following error scenarios:

- **Invalid PAN format**: Returns INVALID status
- **Invalid Aadhaar format**: Returns INVALID status
- **API timeout**: Returns INVALID status with error logging
- **API errors**: Returns INVALID status with error logging
- **Missing required fields**: Returns 400 Bad Request
- **Internal errors**: Returns 500 Internal Server Error

## Dependencies

- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **Requests**: HTTP client for API calls
- **Uvicorn**: ASGI server
- **python-dotenv**: Environment variable management

## Notes

- This is a standalone verification system
- No OCR or fraud detection logic included
- API credentials are stored in environment variables
- All API calls include proper error handling
- Names are normalized before comparison
- DOB formats are normalized for comparison

## License

Part of the fraud detection project.
