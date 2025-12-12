from langgraph.graph import StateGraph, END
from app.graph_state import ReportState

from nodes.ingest_and_ocr import ingest_and_ocr_node
from nodes.extract_parameters import extract_parameters_node
from nodes.validate_standardize import validate_standardize_node
from nodes.model1_interpretation import model1_interpretation_node

def build_graph():
    workflow = StateGraph(ReportState)

    workflow.add_node("ingest_and_ocr", ingest_and_ocr_node)
    workflow.add_node("extract_parameters", extract_parameters_node)
    workflow.add_node("validate_standardize", validate_standardize_node)
    workflow.add_node("model1_interpretation", model1_interpretation_node)

    workflow.set_entry_point("ingest_and_ocr")
    workflow.add_edge("ingest_and_ocr", "extract_parameters")
    workflow.add_edge("extract_parameters", "validate_standardize")
    workflow.add_edge("validate_standardize", "model1_interpretation")
    workflow.add_edge("model1_interpretation", END)

    return workflow.compile()
