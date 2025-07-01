from .base_agent import BaseQAAgent
from typing import Dict, Any, List
from datetime import datetime
import logging

class QALangchainProbe(BaseQAAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"[{self.agent_name}] Running lightweight LLM probing...")

        notes = input_data.get("clinical_notes", [])
        probe_results: List[Dict[str, Any]] = []

        if not notes:
            logging.warning(f"[{self.agent_name}] No notes provided for probing.")
            return self.standard_response(
                output={"probes": [], "passed": False},
                log=f"[{self.agent_name}] No notes to probe."
            )

        for idx, note in enumerate(notes):
            note_text = note.get("text", "")
            probe_pass = "error" not in note_text.lower() and len(note_text.split()) > 20

            probe_results.append({
                "note_id": note.get("note_id", f"note_{idx}"),
                "pass": probe_pass,
                "comment": "Passes length and error-check heuristics" if probe_pass else "Failed simple probe",
                "timestamp": datetime.utcnow().isoformat()
            })

        passed_all = all(p["pass"] for p in probe_results)

        output = {
            "probes": probe_results,
            "passed": passed_all
        }

        return self.standard_response(
            output=output,
            log=f"[{self.agent_name}] Probed {len(probe_results)} notes. All passed: {passed_all}."
        )
