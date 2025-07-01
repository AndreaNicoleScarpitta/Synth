from datetime import datetime

class QASummaryReporter:
    def summarize(self, qa_results: dict) -> dict:
        summary = {
            "total_agents_run": len(qa_results),
            "timestamp": datetime.utcnow().isoformat(),
            "issues_detected": [],
            "recommendations": [],
            "scorecard": {},
            "fhir_bundle": {},
            "langchain_notes": [],
            "logs": {}
        }

        for agent_name, result in qa_results.items():
            if "error" in result:
                summary["logs"][agent_name] = result["log"]
                continue

            # Collect issues
            if agent_name in ["bias_auditor", "label_verifier", "outlier_detector", "realism_checker", "schema_validator", "statistical_validator"]:
                issues = result.get("output", result).get("flags", []) or result.get("flags", [])
                summary["issues_detected"].extend(issues)

            # Add recommendations
            if agent_name == "fix_recommender":
                summary["recommendations"].extend(result.get("fixes", []))

            # Add patient scorecard
            if agent_name == "patient_scorecard":
                summary["scorecard"] = {
                    "patient_id": result.get("patient_id"),
                    "score": result.get("score"),
                    "issues": result.get("issues")
                }

            # Exported FHIR content
            if agent_name == "fhir_exporter":
                summary["fhir_bundle"] = result.get("bundle", {})

            # Langchain probe notes
            if agent_name == "langchain_probe":
                summary["langchain_notes"] = result.get("notes", [])

            # Log any general log output
            if "log" in result:
                summary["logs"][agent_name] = result["log"]

        return summary
