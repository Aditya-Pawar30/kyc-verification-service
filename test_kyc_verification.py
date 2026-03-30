"""
Test script for KYC Verification Service
"""
import asyncio
import json
from app.models.request_models import KYCVerificationRequest, PanCardData, AadhaarCardData
from app.services.verification_service import verification_service


def test_name_normalization():
    """Test name normalization functionality"""
    print("Testing name normalization...")
    
    test_cases = [
        ("Mr. Rahul Sharma", "RAHUL SHARMA"),
        ("DR. PRIYA PATEL", "PRIYA PATEL"),
        ("Shri Amit Kumar", "AMIT KUMAR"),
        ("  RAHUL   SHARMA  ", "RAHUL SHARMA"),
        ("Smt. Sunita Devi", "SUNITA DEVI"),
    ]
    
    for input_name, expected in test_cases:
        result = verification_service.normalize_name(input_name)
        status = "[OK]" if result == expected else "[FAIL]"
        print(f"  {status} '{input_name}' -> '{result}' (expected: '{expected}')")


def test_name_similarity():
    """Test name similarity calculation"""
    print("\nTesting name similarity...")
    
    test_cases = [
        ("RAHUL SHARMA", "RAHUL SHARMA", 1.0),
        ("RAHUL SHARMA", "RAHUL KUMAR", 0.5),
        ("RAHUL SHARMA", "RAHUL SHARMA", 1.0),
        ("", "RAHUL SHARMA", 0.0),
        ("RAHUL SHARMA", "", 0.0),
    ]
    
    for name1, name2, expected_min in test_cases:
        result = verification_service.calculate_name_similarity(name1, name2)
        status = "[OK]" if result >= expected_min else "[FAIL]"
        print(f"  {status} '{name1}' vs '{name2}' -> {result:.2f} (min: {expected_min})")


def test_pan_verification():
    """Test PAN verification"""
    print("\nTesting PAN verification...")
    
    # Test with valid PAN format
    result = verification_service.verify_pan("ABCDE1234F", "RAHUL SHARMA")
    print(f"  PAN ABCDE1234F: Valid={result.panValid}, Status={result.panStatus}, NameMatch={result.nameMatch}")
    
    # Test with invalid PAN format
    result = verification_service.verify_pan("INVALID", "RAHUL SHARMA")
    print(f"  PAN INVALID: Valid={result.panValid}, Status={result.panStatus}, NameMatch={result.nameMatch}")


def test_aadhaar_verification():
    """Test Aadhaar verification"""
    print("\nTesting Aadhaar verification...")
    
    # Test with valid Aadhaar format
    result = verification_service.verify_aadhaar("123412341234", "RAHUL SHARMA")
    print(f"  Aadhaar 123412341234: Valid={result.aadhaarValid}, Status={result.aadhaarStatus}, NameMatch={result.nameMatch}")
    
    # Test with invalid Aadhaar format
    result = verification_service.verify_aadhaar("12345", "RAHUL SHARMA")
    print(f"  Aadhaar 12345: Valid={result.aadhaarValid}, Status={result.aadhaarStatus}, NameMatch={result.nameMatch}")


def test_identity_match():
    """Test identity matching"""
    print("\nTesting identity matching...")
    
    test_cases = [
        ("RAHUL SHARMA", "RAHUL SHARMA", True),
        ("RAHUL SHARMA", "RAHUL KUMAR", False),
        ("", "RAHUL SHARMA", False),
        ("RAHUL SHARMA", "", False),
    ]
    
    for pan_name, aadhaar_name, expected in test_cases:
        result = verification_service.verify_identity_match(pan_name, aadhaar_name)
        status = "[OK]" if result == expected else "[FAIL]"
        print(f"  {status} '{pan_name}' vs '{aadhaar_name}' -> {result} (expected: {expected})")


def test_full_kyc_verification():
    """Test full KYC verification"""
    print("\nTesting full KYC verification...")
    
    # Create test request
    request = KYCVerificationRequest(
        panCard=PanCardData(
            name="RAHUL SHARMA",
            dob="01/01/1998",
            panNumber="ABCDE1234F"
        ),
        aadhaarCard=AadhaarCardData(
            name="RAHUL SHARMA",
            aadhaarNumber="123412341234"
        )
    )
    
    # Perform verification
    status, pan_result, aadhaar_result, identity_match = verification_service.verify_kyc(
        pan_data=request.panCard,
        aadhaar_data=request.aadhaarCard
    )
    
    print(f"  Verification Status: {status}")
    print(f"  PAN Valid: {pan_result.panValid}, Status: {pan_result.panStatus}, NameMatch: {pan_result.nameMatch}")
    print(f"  Aadhaar Valid: {aadhaar_result.aadhaarValid}, Status: {aadhaar_result.aadhaarStatus}, NameMatch: {aadhaar_result.nameMatch}")
    print(f"  Identity Match: {identity_match}")


def test_request_models():
    """Test request models"""
    print("\nTesting request models...")
    
    # Test valid request
    try:
        request = KYCVerificationRequest(
            panCard=PanCardData(
                name="RAHUL SHARMA",
                dob="01/01/1998",
                panNumber="ABCDE1234F"
            ),
            aadhaarCard=AadhaarCardData(
                name="RAHUL SHARMA",
                aadhaarNumber="123412341234"
            )
        )
        print("  [OK] Valid request created successfully")
        print(f"    PAN Number: {request.panCard.panNumber}")
        print(f"    Aadhaar Number: {request.aadhaarCard.aadhaarNumber}")
    except Exception as e:
        print(f"  [FAIL] Error creating request: {e}")


def main():
    """Run all tests"""
    print("=" * 60)
    print("KYC Verification Service Tests")
    print("=" * 60)
    
    test_name_normalization()
    test_name_similarity()
    test_pan_verification()
    test_aadhaar_verification()
    test_identity_match()
    test_request_models()
    test_full_kyc_verification()
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
