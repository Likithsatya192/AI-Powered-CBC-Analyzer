from typing import List
from pydantic import BaseModel, Field
from utils.llm_utils import get_llm

class RecsOutput(BaseModel):
    recommendations: List[str] = Field(description="List of actionable health recommendations")

def recommendations_node(state):
    """
    Generates personalized recommendations based on the synthesized findings.
    """
    synthesis = state.synthesis_report
    if not synthesis:
        return {"recommendations": []}

    llm = get_llm()
    structured_llm = llm.with_structured_output(RecsOutput)
    
    prompt = f"""
    Based on the following medical report summary:
    
    "{synthesis}"
    
    Provide 3-5 actionable health, diet, or lifestyle recommendations.
    Be specific but safe (always advise consulting a doctor).
    """
    
    try:
        response = structured_llm.invoke(prompt)
        return {"recommendations": response.recommendations}
    except Exception as e:
        return {"errors": state.errors + [f"Recommendations Node failed: {str(e)}"]}
