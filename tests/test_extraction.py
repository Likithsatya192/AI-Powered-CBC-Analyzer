"""Tests for extraction utilities (very small smoke tests)."""
from nodes.extract_parameters import run as extract_run


def test_extract_basic():
    txt = "Hemoglobin: 13.2 g/dL\nGlucose: 92 mg/dL"
    out = extract_run(txt)
    assert "parameters" in out
    assert out["parameters"].get("Hemoglobin") == "13.2 g/dL"
