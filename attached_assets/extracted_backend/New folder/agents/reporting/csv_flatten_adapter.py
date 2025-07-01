from agents.reporting.base_agent import BaseReportingAgent
import csv
import io
from typing import Dict, Any, List

class CSVFlattenAdapter(BaseReportingAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flattens a list of records into CSV format.
        Assumes input_data['records'] is a list of flat dicts.
        """
        records: List[Dict[str, Any]] = input_data.get("records", [])
        if not isinstance(records, list) or not records:
            return self.standard_response(
                output={"csv": "", "row_count": 0, "error": "No records to flatten"},
                log="No records found or records not a list."
            )

        headers = sorted({key for r in records for key in r})
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        for row in records:
            writer.writerow(row)

        csv_data = output.getvalue()
        log_msg = f"CSVFlattenAdapter: Flattened {len(records)} records with {len(headers)} columns."

        return self.standard_response(
            output={
                "csv": csv_data,
                "row_count": len(records),
                "columns": headers,
                "generated_by": "CSVFlattenAdapter"
            },
            log=log_msg
        )
