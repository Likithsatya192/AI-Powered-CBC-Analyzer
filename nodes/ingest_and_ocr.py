from utils.pdf_utils import extract_pdf_text
from utils.ocr_utils import run_ocr

def ingest_and_ocr_node(state):
    """
    Node input: state (ReportState)
    Node returns: dict to update state (langgraph expects node returns)
    """
    file_path = state.raw_file_path
    text = ""
    try:
        text = extract_pdf_text(file_path)
    except Exception:
        # fallback to OCR if pdf text extraction fails
        text = ""

    if not text or len(text.strip()) < 50:
        try:
            text = run_ocr(file_path)
        except Exception as e:
            # Bubble up a clear, user-friendly error instead of crashing.
            return {"errors": state.errors + [f"OCR failed: {str(e)}"]}

    return {"raw_text": text}
