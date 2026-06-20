import pdfplumber

# =========================================
# EXTRACT TEXT FROM PDF
# =========================================

def extract_resume_text(uploaded_file):

    text = ""

    try:

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text

    except Exception:

        return ""

    return text
