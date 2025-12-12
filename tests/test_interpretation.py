"""Tests for interpretation node (very small smoke tests)."""
from nodes.model1_interpretation import run as interpret_run


def test_interpret_basic():
    params = {"Hemoglobin": 13.2, "Glucose": {"value_mg/dL": 92}}
    out = interpret_run(params)
    assert "interpretation" in out
    assert "Hemoglobin" in out["interpretation"]
