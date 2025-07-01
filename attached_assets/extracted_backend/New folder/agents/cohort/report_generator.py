from typing import Dict, Any
import logging
from utils.base_agent import BaseAgent

class ReportGenerator(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[ReportGenerator] Generating human-readable report...")

        chart = input_data.get("synthetic_chart", {})
        demographics = chart.get("demographics", {})
        conditions = chart.get("conditions", [])
        procedures = chart.get("procedures", [])
        labs = chart.get("lab_results", [])
        vitals = chart.get("vital_signs", {})
        medications = chart.get("medications", [])
        notes = chart.get("clinical_notes", [])

        lines = []

        lines.append(f"📄 Synthetic Patient Summary Report")
        lines.append(f"Name: {demographics.get('name', 'N/A')}")
        lines.append(f"Age: {demographics.get('age', 'N/A')} | Sex: {demographics.get('sex', 'N/A')}")
        lines.append(f"\n🩺 Conditions:")
        lines.extend([f" - {cond}" for cond in conditions] or [" - None"])

        lines.append(f"\n💊 Medications:")
        lines.extend([f" - {med.get('name')} ({med.get('dosage')})" for med in medications] or [" - None"])

        lines.append(f"\n🏥 Procedures:")
        lines.extend([f" - {proc.get('name')} on {proc.get('date')}" for proc in procedures] or [" - None"])

        lines.append(f"\n🧪 Lab Results:")
        lines.extend([
            f" - {lab['name']}: {lab['value']} {lab['unit']}"
            for lab in labs
        ] or [" - None"])

        lines.append(f"\n🫁 Vital Signs:")
        for k, v in vitals.items():
            lines.append(f" - {k.replace('_', ' ').title()}: {v}")

        lines.append(f"\n📝 Notes:")
        lines.extend([f" - {note}" for note in notes] or [" - None"])

        report = "\n".join(lines)
        input_data["human_report"] = report

        return {
            "output": input_data,
            "log": "[ReportGenerator] Report generated successfully."
        }
