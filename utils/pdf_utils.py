import fitz  # PyMuPDF

def extract_pdf_text(path: str) -> str:
    text = ""
    doc = fitz.open(path)
    for page in doc:
        # get_text("text") or get_text()
        text += page.get_text()
    return text
