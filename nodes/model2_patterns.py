from typing import List
from pydantic import BaseModel, Field
from utils.llm_utils import get_llm

class PatternOutput(BaseModel):
    patterns: List[str] = Field(description="List of identified clinical patterns (e.g., 'Microcytic Anemia', 'Leukocytosis')")
    risk_score: int = Field(description="Risk score from 1-10 (10 being highest risk)")
    risk_rationale: str = Field(description="Brief explanation of the risk score")

def model2_patterns_node(state):
    """
    Analyzes validated parameters to identify patterns and assess risk.
    """
    validated = state.validated_params
    patient_info = state.patient_info or {}
    
    if not validated:
        return {"patterns": [], "risk_assessment": {}}

    llm = get_llm()
    structured_llm = llm.with_structured_output(PatternOutput)

    # Format input for LLM
    data_str = "\n".join([f"{k}: {v['value']} {v.get('unit','')}" for k, v in validated.items()])
    
    # Explicitly calculate basic flags to guide the LLM
    hb = validated.get("Hemoglobin", {}).get("value")
    mcv = validated.get("MCV", {}).get("value")
    pcv = validated.get("Packed Cell Volume", {}).get("value")
    
    # Prompt Augmentation
    prompt = f"""
    You are an expert medical AI assistant specialized in hematology.
    
    Patient Info:
    Name: {patient_info.get('Name', 'Unknown')}
    Age: {patient_info.get('Age', 'Unknown')}
    Gender: {patient_info.get('Gender', 'Unknown')}

    Analyze the following CBC blood test results:
    {data_str}
    
    CRITICAL RULES:
    1. TRUST the reference ranges implicitly. If a value is within range, it is NORMAL. Do NOT call it "Slightly Elevated" or "Borderline" unless it is actually outside or right at the edge.
    2. CHECK FOR:
       - Normocytic Anemia: Low Hemoglobin AND Normal MCV.
       - Dehydration/Polycythemia: High PCV (Packed Cell Volume).
       - Leukocytosis/Leukopenia: High/Low WBC.
       - Thrombocytopenia/Thrombocytosis: Low/High Platelets.
    3. SPECIFIC CHECKS:
       - If PCV is > 50% (and Male) or > 45% (Female), flag it as High PCV/Hematocrit.
       - If RBC is within 4.5-5.5, it is NORMAL.
       
    Identify specific clinical patterns.
    Assess the overall health risk score (1-10).
    Provide a rationale.
    
    Return the output in the specified JSON format.
    """

    try:
        response = structured_llm.invoke(prompt)
        return {
            "patterns": response.patterns,
            "risk_assessment": {
                "score": response.risk_score,
                "rationale": response.risk_rationale
            }
        }
    except Exception as e:
        return {"errors": state.errors + [f"Model 2 (Patterns) failed: {str(e)}"]}
