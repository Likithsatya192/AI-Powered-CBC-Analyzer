from heuristic.graph_builder_heuristic import build_graph
from app.graph_state import ReportState

def run_full_pipeline(file_path):
    app = build_graph()
    initial_state = ReportState(raw_file_path=file_path)
    # Recursion limit might need adjustment but default usually fine
    result = app.invoke(initial_state)
    
    # LangGraph returns a dict; convert back to object for UI compatibility
    if isinstance(result, dict):
        result = ReportState(**result)
        
    return result
