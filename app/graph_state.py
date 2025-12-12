from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class ReportState(BaseModel):
    raw_file_path: Optional[str] = None
    raw_text: Optional[str] = None
    extracted_params: Dict[str, Dict[str, Any]] = {}
    validated_params: Dict[str, Dict[str, Any]] = {}
    param_interpretation: Dict[str, Dict[str, Any]] = {}
    errors: List[str] = []