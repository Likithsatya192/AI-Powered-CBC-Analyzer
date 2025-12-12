_mapping = {
    "Hb": "Hemoglobin",
    "Hgb": "Hemoglobin",
    "Hemoglobin": "Hemoglobin",
    "WBC": "WBC",
    "White Blood Cells": "WBC",
    "Platelets": "Platelets",
    "PLT": "Platelets",
    "Glucose": "Glucose"
}

def normalize_name(name: str) -> str:
    key = name.strip()
    return _mapping.get(key, key)
