import fitz
def extract_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    resume_text = ""

    for page in doc:
        resume_text += page.get_text()

    doc.close()
    return resume_text.strip()