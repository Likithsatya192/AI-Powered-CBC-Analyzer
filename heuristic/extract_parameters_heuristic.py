import re
from typing import Dict, Any, Optional, Tuple, List
from rapidfuzz import process, fuzz

# Canonical CBC parameters with rich synonym lists to improve matching across labs.
CBC_PARAMS = {
    "Hemoglobin": ["hemoglobin", "hb", "hgb", "heme"],
    "Total RBC count": ["total rbc", "rbc count", "rbc"],
    "Packed Cell Volume": ["pcv", "packed cell volume", "hematocrit", "hct"],
    "MCV": ["mcv", "mean corpuscular volume"],
    "MCH": ["mch", "mean corpuscular hemoglobin"],
    "MCHC": ["mchc", "mean corpuscular hemoglobin concentration"],
    "RDW": ["rdw", "red cell dist", "red cell distribution width"],
    "Total WBC count": ["total wbc", "wbc count", "wbc", "white blood cell"],
    "Neutrophils": ["neutrophil", "neutro"],
    "Lymphocytes": ["lymphocytes", "lympho"],
    "Eosinophils": ["eosinophils", "eosino", "eos"],
    "Monocytes": ["monocytes", "mono"],
    "Basophils": ["basophils", "baso"],
    "Platelet Count": ["platelet", "platelet count", "plt"],
    "ESR": ["esr", "erythrocyte sedimentation rate"],
    "MPV": ["mpv", "mean platelet volume"],
    "PDW": ["pdw", "platelet distribution width"],
    "PCT": ["pct", "plateletcrit"],
    "Absolute Neutrophils": ["absolute neutrophils", "abs neut", "neutrophils abs"],
    "Absolute Lymphocytes": ["absolute lymphocytes", "abs lymph", "lymphocytes abs"],
    "Absolute Eosinophils": ["absolute eosinophils", "abs eos", "eosinophils abs"],
    "Absolute Monocytes": ["absolute monocytes", "abs mono", "monocytes abs"],
    "Absolute Basophils": ["absolute basophils", "abs baso", "basophils abs"],
}

# Expected units for display fallback
DEFAULT_UNITS = {
    "Hemoglobin": "g/dL",
    "Total RBC count": "mill/cumm",
    "Packed Cell Volume": "%",
    "MCV": "fL",
    "MCH": "pg",
    "MCHC": "g/dL",
    "RDW": "%",
    "Total WBC count": "cumm",
    "Neutrophils": "%",
    "Lymphocytes": "%",
    "Eosinophils": "%",
    "Monocytes": "%",
    "Basophils": "%",
    "Platelet Count": "cumm",
    "ESR": "mm/hr",
    "MPV": "fL",
    "PDW": "%",
    "PCT": "%",
    "Absolute Neutrophils": "cumm",
    "Absolute Lymphocytes": "cumm",
    "Absolute Eosinophils": "cumm",
    "Absolute Monocytes": "cumm",
    "Absolute Basophils": "cumm",
}

# Accept comma-separated numbers like 10,000 or 150,000
NUM = re.compile(r"([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]+)?|[0-9]{1,7}(?:\.[0-9]+)?)")


def _best_param_match(clean_line: str) -> Optional[str]:
    """
    Choose the best matching parameter name for a cleaned line of text.
    Uses fuzzy matching across the synonym lists.
    """
    candidates = []
    for pname, tokens in CBC_PARAMS.items():
        for token in tokens:
            score = fuzz.partial_ratio(token, clean_line)
            candidates.append((score, pname))
    if not candidates:
        return None
    best = max(candidates, key=lambda x: x[0])
    return best[1] if best[0] >= 70 else None


def extract_parameters_node_heuristic(state):
    """
    Parse OCR/text output from CBC reports and extract parameter values.
    The logic tolerates noisy OCR and flexible table layouts by:
      - fuzzy matching known parameter synonyms
      - grabbing the first numeric token as the result column
      - applying unit/scale fallbacks
    """
    text = state.raw_text or ""
    lines = text.splitlines()

    extracted = {}

    for line in lines:
        clean = re.sub(r"[^\w.%/\- ]", " ", line).strip().lower()
        if len(clean) < 3:
            continue

        matched_param = _best_param_match(clean)
        if not matched_param:
            continue

        # Extract all numeric tokens on the line
        nums = []
        for m in NUM.finditer(clean):
            token = m.group(1).replace(",", "")
            try:
                nums.append(float(token))
            except ValueError:
                continue
        if not nums:
            continue

        # Heuristic: the FIRST number is the result column
        result_value = nums[0]

        scale_note = None
        # Adjust RBC scale if OCR returns 500 instead of 5.00
        if matched_param == "Total RBC count" and result_value > 20:
            scale_note = "Scaled down by /100 to match millions/cumm"
            result_value = result_value / 100

        # Adjust Platelet count if OCR returns in lakhs
        if matched_param == "Platelet Count" and result_value < 1000:
            scale_note = "Scaled up by *1000 to match cumm"
            result_value = result_value * 1000

        extracted[matched_param] = {
            "raw_value": nums[0],
            "value": result_value,
            "unit": DEFAULT_UNITS.get(matched_param),
            "scale_note": scale_note,
        }

    
    # Extract Patient Info (Heuristic)
    patient_info = {}
    
    # Age
    age_match = re.search(r"(?:Age|Yrs|Years?)\s*[:\.]?\s*(\d{1,3})", text, re.IGNORECASE)
    if age_match:
        patient_info["Age"] = age_match.group(1)
        
    # Sex
    sex_match = re.search(r"(?:Sex|Gender)\s*[:\.]?\s*(Male|Female|M|F)", text, re.IGNORECASE)
    if sex_match:
        s = sex_match.group(1).upper()
        patient_info["Gender"] = "Male" if s.startswith("M") else "Female" if s.startswith("F") else s

    # Name (Very rough heuristic, looks for 'Name:' or 'Patient:')
    name_match = re.search(r"(?:Patient\s*Name|Name)\s*[:\.]?\s*([A-Za-z. ]+)", text, re.IGNORECASE)
    if name_match:
        patient_info["Name"] = name_match.group(1).strip()

    return {"extracted_params": extracted, "patient_info": patient_info}
