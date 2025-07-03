# type: ignore
import fitz  # PyMuPDF

def load_pdf(pdf_file):
    """
    Reads uploaded PDF file and extracts all text.
    
    Args:
        pdf_file: File-like object from Streamlit uploader.

    Returns:
        str: Combined text from all pages of the PDF.
    """
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
