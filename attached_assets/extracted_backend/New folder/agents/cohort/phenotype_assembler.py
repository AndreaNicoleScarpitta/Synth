from typing import Dict, Any
import random
import logging
from langchain_core.runnables import Runnable
from langchain_core.callbacks import CallbackManagerForToolRun

# Optionally use LLM for validation or explanation
class PhenotypeAssembler(Runnable):
    def __init__(self, llm=None, config: Dict[str, Any] = None):
        self.llm = llm
        self.config = config or {
            "primary_conditions": ["CKD", "Diabetes", "Hypertension", "COPD"],
            "condition_weights": [0.3, 0.3, 0.2, 0.2],
            "max_conditions": 2
        }

    def invoke(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        logging.info("[PhenotypeAssembler] Generating condition profile...")

        # Sample from weighted list
        phenotypes = random.choices(
            self.config["primary_conditions"],
            weights=self.config["condition_weights"],
            k=self.config["max_conditions"]
        )

        # Deduplicate
        phenotypes = list(set(phenotypes))
        input_data["phenotypes"] = phenotypes

        # Optional LLM call for validation or commentary
        explanation = ""
        if self.llm:
            prompt = f"Given the conditions {phenotypes}, is this clinically realistic?"
            try:
                explanation = self.llm.invoke(prompt)
                input_data["phenotype_validation"] = str(explanation)
            except Exception as e:
                logging.warning(f"[PhenotypeAssembler] LLM validation failed: {e}")
                input_data["phenotype_validation"] = "LLM validation failed"

        return {
            "output": input_data,
            "log": f"Phenotypes assigned: {phenotypes}"
        }
