def model1_interpretation_node(state):
    validated = state.validated_params or {}
    interpreted = {}

    for name, info in validated.items():
        v = info["value"]
        ref = info["reference"]
        low = ref.get("low")
        high = ref.get("high")
        status = "unknown"
        if low is not None and high is not None:
            if v < low:
                status = "low"
            elif v > high:
                status = "high"
            else:
                status = "normal"
        interpreted[name] = {
            "value": v,
            "unit": info.get("unit"),
            "reference": ref,
            "status": status
        }

    return {"param_interpretation": interpreted}