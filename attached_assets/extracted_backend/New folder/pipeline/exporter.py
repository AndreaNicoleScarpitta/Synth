import json

class JSONLinesExporter:
    def __init__(self, path: str):
        self.path = path

    def write(self, records: list):
        """Write each record as a separate JSON line."""
        with open(self.path, "w") as f:
            for rec in records:
                f.write(json.dumps(rec, default=str) + "\n")
