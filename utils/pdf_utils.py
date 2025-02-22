import pdfplumber
from io import BytesIO

def extract_text_from_pdf(pdf_bytes):
    """
    Extracts text from a PDF file given its binary content.
    
    Args:
        pdf_bytes (bytes): PDF file content in binary format.
    
    Returns:
        str: Extracted text.
    """
    text = ""

    # Convert bytes to a file-like object
    pdf_stream = BytesIO(pdf_bytes)
    with pdfplumber.open(pdf_stream) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    return text.strip()
