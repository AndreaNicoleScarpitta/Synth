import json
import jsonschema

# Config schema for validation
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "max_retries": {"type": "integer", "minimum": 1},
        "backoff_factor": {"type": "number", "minimum": 1},
        "initial_backoff": {"type": "number", "minimum": 0},
        "realism_threshold": {"type": "number", "minimum": 0, "maximum": 1},
        "privacy_threshold": {"type": "number", "minimum": 0, "maximum": 1},
        "bias_threshold": {"type": "number", "minimum": 0, "maximum": 1},
        "max_loops": {"type": "integer", "minimum": 1},
        "log_file": {"type": "string"},
        "output_path": {"type": "string"},
        "max_workers": {"type": "integer", "minimum": 1}
    },
    "required": ["output_path"]
}

def load_config(path: str) -> dict:
    """Load and validate pipeline configuration."""
    with open(path) as f:
        cfg = json.load(f)
    jsonschema.validate(cfg, CONFIG_SCHEMA)
    return cfg
