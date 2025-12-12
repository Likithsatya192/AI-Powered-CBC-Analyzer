import json
from pathlib import Path

def load_reference_ranges():
    p = Path(__file__).resolve().parents[1] / "configs" / "reference_ranges.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text())
