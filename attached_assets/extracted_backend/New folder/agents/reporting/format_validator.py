from .base_agent import BaseReportingAgent
from typing import Dict, Any, List

class FormatValidator(BaseReportingAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the format of output records (e.g., for CSV, JSON, FHIR export).
        Checks for required fields, consistent columns, and non-empty output.
        """
        records = input_data.get("records", [])
        required_fields = input_data.get("required_fields", [])

        passed = True
        issues: List[str] = []

        if not isinstance(records, list) or not records:
            passed = False
            issues.append("No records found or records not a list.")

        if required_fields:
            for field in required_fields:
                if not all(field in r for r in records):
                    passed = False
                    issues.append(f"Missing required field in one or more records: {field}")

        # Optional: Check for consistent keys
        if records:
            first_keys = set(records[0].keys())
            for idx, r in enumerate(records):
                if set(r.keys()) != first_keys:
                    passed = False
                    issues.append(f"Record {idx} has inconsistent columns.")

        output = {
            "format_validation_passed": passed,
            "issues": issues,
            "checked_fields": required_fields,
            "record_count": len(records)
        }

        log = (
            "FormatValidator: "
            + ("PASSED" if passed else f"FAILED with {len(issues)} issue(s).")
        )

        return self.standard_response(
            output=output,
            log=log
        )
