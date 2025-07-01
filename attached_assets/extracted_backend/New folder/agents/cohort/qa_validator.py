from typing import Dict, Any
import logging
from utils.base_agent import BaseAgent

class QAValidator(BaseAgent):
    def __init__(self, llm=None):
        self.llm = llm

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[QAValidator] Running final QA checks...")

        errors = []
        warnings = []

        # Check: every procedure must have a linked encounter
        for proc in input_data.get("procedures", []):
            if not proc.get("linked_encounter"):
                errors.append(f"Procedure {proc.get('procedure_code')} missing linked encounter.")

        # Check: conditions and procedures must be consistent
        if not input_data.get("conditions"):
            warnings.append("No conditions found.")
        if not input_data.get("procedures"):
            warnings.append("No procedures found.")

        # Optional LLM plausibility check
        if self.llm:
            try:
                context = {
                    "conditions": input_data.get("conditions"),
                    "procedures": input_data.get("procedures"),
                    "medications": input_data.get("medications"),
                    "timeline": input_data.get("timeline_summary", "")
                }
                prompt = f"Does this patient summary contain any medical inconsistencies? Be critical:\n{context}"
                critique = self.llm.invoke(prompt)
                input_data["llm_qa_feedback"] = str(critique)
            except Exception as e:
                logging.warning(f"[QAValidator] LLM check failed: {e}")
                input_data["llm_qa_feedback"] = "LLM QA failed"

        input_data["qa_errors"] = errors
        input_data["qa_warnings"] = warnings

        return {
            "output": input_data,
            "log": f"QA completed with {len(errors)} errors and {len(warnings)} warnings."
        }