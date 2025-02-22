from typing import Any

import pytesseract
from PIL import Image
from io import BytesIO

def set_tesseract_path(path: str = "/usr/bin/tesseract"):
    """
    Explicitly set the path for the Tesseract OCR executable.
    
    Args:
        path (str): The absolute path to the Tesseract binary.
    """
    pytesseract.pytesseract.tesseract_cmd = path

def extract_text_from_image(image_bytes: bytes) -> Any | None:
    """
    Extracts text from an image using Tesseract OCR.
    
    Args:
        image_bytes (bytes): Raw image data in bytes.
    
    Returns:
        str: Extracted text from the image.
    """
    try:
        # Convert raw image bytes into a PIL Image object
        image = Image.open(BytesIO(image_bytes))
        
        # Perform OCR (Optical Character Recognition) using Tesseract
        text = pytesseract.image_to_string(image)
        
        # Return cleaned-up extracted text
        return text.strip()
    
    except Exception as e:
        # Handle exceptions gracefully and log errors
        print(f"ERROR: OCR extraction failed - {e}")
        return None 

# Set Tesseract path (modify if Tesseract is installed elsewhere)
set_tesseract_path()
