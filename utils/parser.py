"""
PDF Parser — extracts text from uploaded resume PDF files.
Handles multi-page documents and gives clear error messages
for scanned/image-only PDFs.
"""

import pdfplumber


def extract_resume_text(uploaded_file) -> str:
    """
    Extract all text from a PDF file.

    Returns:
        str — extracted text, or empty string on failure.
    """
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[parser] PDF extraction error: {e}")
        return ""

    return text.strip()


def estimate_word_count(text: str) -> int:
    return len(text.split())


def is_likely_scanned(text: str) -> bool:
    """
    Heuristic: if we got almost no text from a multi-page PDF,
    it's probably a scanned image that needs OCR.
    """
    return estimate_word_count(text) < 30
