def convert_unit(param: str, value: float, unit: str):
    if not unit:
        return value
    u = unit.lower()
    # Example: glucose mmol/L -> mg/dL
    if param.lower() == "glucose" and ("mmol" in u):
        return value * 18.0182
    # more conversions can be added as needed
    return value
