from app.graph_builder import build_graph
from app.graph_state import ReportState

def run_full_pipeline(file_path):
    graph_app = build_graph()
    initial_state = ReportState(raw_file_path=file_path)
    final_state = graph_app.invoke(initial_state)

    # LangGraph may return a plain dict; normalize to ReportState so the
    # Streamlit UI can safely use attribute access.
    if isinstance(final_state, dict):
        final_state = ReportState(**final_state)

    return final_state
