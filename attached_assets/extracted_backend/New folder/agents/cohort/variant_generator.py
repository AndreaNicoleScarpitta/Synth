from typing import Dict, Any, List
import random
from utils.base_agent import BaseAgent

VARIANT_LIBRARY = [
    {"gene": "APOE", "variant": "e4", "risk": "Alzheimer's disease"},
    {"gene": "SLCO1B1", "variant": "*5", "risk": "Statin-induced myopathy"},
    {"gene": "BRCA1", "variant": "185delAG", "risk": "Breast and ovarian cancer"},
    {"gene": "HLA-B", "variant": "1502", "risk": "Carbamazepine-induced SJS"},
    {"gene": "CYP2C19", "variant": "*2", "risk": "Poor clopidogrel metabolism"}
]

class VariantGenerator(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        selected = random.sample(VARIANT_LIBRARY, k=random.randint(1, 3))
        variants: List[Dict[str, Any]] = []

        for var in selected:
            variants.append({
                "gene": var["gene"],
                "variant": var["variant"],
                "risk_factor": var["risk"],
                "zygosity": random.choice(["heterozygous", "homozygous"])
            })

        input_data["genetic_variants"] = variants

        return {
            "output": input_data,
            "log": f"[VariantGenerator] Generated {len(variants)} genetic variants."
        }
