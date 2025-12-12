from utils.reference_ranges import load_reference_ranges

def validate_standardize_node(state):
    ranges = load_reference_ranges()
    cleaned = {}
    errors = state.errors.copy() if state.errors else []

    for param, info in state.extracted_params.items():
        val = info.get("value")
        unit = info.get("unit") or (ranges.get(param) or {}).get("unit")
        if val is None:
            errors.append(f"No numeric value found for {param}. Skipping.")
            continue
        if param not in ranges:
            errors.append(f"No reference range config for {param}. Skipping.")
            continue
        cleaned[param] = {
            "value": val,
            "unit": unit,
            "reference": ranges[param]["reference"]
        }

    return {"validated_params": cleaned, "errors": errors}