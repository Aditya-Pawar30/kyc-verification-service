from app.models.request_models import FraudDetectionRequest
from app.models.response_models import FraudDetectionResponse, MatchSummary
from app.services.validation_service import (
    validate_pan_number,
    validate_aadhaar_number,
)

from app.services.comparison_service import (
    compare_names,
    compare_surname_consistency,
    compare_dob,
)


class FraudDetectionService:
    @staticmethod
    def map_fraud_status(score: int) -> str:
        if 0 <= score <= 19:
            return "NO_FRAUD_DETECTED"
        elif 20 <= score <= 49:
            return "SUSPICIOUS"
        return "POSSIBLE_FRAUD"

    @staticmethod
    def generate_fraud_types(flags: list[str]) -> list[str]:
        fraud_types = []

        if "invalid_pan_format" in flags or "invalid_aadhaar_format" in flags:
            fraud_types.append("FORMAT_FRAUD")

        if "name_mismatch" in flags:
            fraud_types.append("IDENTITY_MISMATCH")

        if "dob_mismatch" in flags:
            fraud_types.append("DOB_MISMATCH_FRAUD")

        if "surname_inconsistency" in flags:
            fraud_types.append("FAMILY_NAME_INCONSISTENCY")

        if len(flags) > 1:
            fraud_types.append("MULTIPLE_SUSPICIOUS_SIGNALS")

        if not fraud_types:
            fraud_types.append("NO_FRAUD")

        return list(dict.fromkeys(fraud_types))

    @staticmethod
    def detect_fraud(request_data: FraudDetectionRequest) -> FraudDetectionResponse:
        fraud_score = 0
        fraud_flags = []

        pan_data = request_data.panCard
        aadhaar_data = request_data.aadhaarCard

        pan_valid = validate_pan_number(pan_data.panNumber or "")
        aadhaar_valid = validate_aadhaar_number(aadhaar_data.aadhaarNumber or "")

        if not pan_valid:
            fraud_score += 40
            fraud_flags.append("invalid_pan_format")

        if not aadhaar_valid:
            fraud_score += 40
            fraud_flags.append("invalid_aadhaar_format")

        name_result = compare_names(pan_data.name or "", aadhaar_data.name or "")
        if name_result["match_type"] == "minor_mismatch":
            fraud_score += 15
            fraud_flags.append("name_mismatch")
        elif name_result["match_type"] == "moderate_mismatch":
            fraud_score += 30
            fraud_flags.append("name_mismatch")
        elif name_result["match_type"] == "major_mismatch":
            fraud_score += 50
            fraud_flags.append("name_mismatch")

        surname_result = compare_surname_consistency(
            pan_data.name or "",
            pan_data.fatherName or "",
            aadhaar_data.name or "",
        )

        if surname_result["consistency_type"] == "weak_inconsistency":
            fraud_score += 10
            fraud_flags.append("surname_inconsistency")
        elif surname_result["consistency_type"] == "strong_inconsistency":
            fraud_score += 20
            fraud_flags.append("surname_inconsistency")

        dob_result = compare_dob(pan_data.dob or "", aadhaar_data.dob or "")
        if dob_result["match_type"] == "partial_match":
            fraud_score += 20
            fraud_flags.append("dob_mismatch")
        elif dob_result["match_type"] == "complete_mismatch":
            fraud_score += 40
            fraud_flags.append("dob_mismatch")

        fraud_score = min(fraud_score, 100)
        fraud_flags = list(dict.fromkeys(fraud_flags))
        fraud_types = FraudDetectionService.generate_fraud_types(fraud_flags)

        return FraudDetectionResponse(
            fraudStatus=FraudDetectionService.map_fraud_status(fraud_score),
            fraudScore=fraud_score,
            fraudFlags=fraud_flags,
            fraudType=fraud_types,
            matchSummary=MatchSummary(
                nameMatch=name_result["name_match"],
                fatherNameConsistency=surname_result["consistent"],
                dobMatch=dob_result["dob_match"],
                panFormatValid=pan_valid,
                aadhaarFormatValid=aadhaar_valid,
            )
        )