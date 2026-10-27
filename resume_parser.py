from io import BytesIO

import pymupdf
from docx import Document

def extract_resume_text(file):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        content = file.read()

        with pymupdf.open(
            stream=content,
            filetype="pdf"
        ) as pdf:
            text = "\n".join(
                page.get_text() for page in pdf
            )

    elif filename.endswith(".docx"):
        document = Document(BytesIO(file.read()))

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    elif filename.endswith(".txt"):
        text = file.read().decode(
            "utf-8",
            errors="replace"
        )

    else:
        raise ValueError(
            "Unsupported file format. Upload PDF, DOCX, or TXT."
        )

    if not text.strip():
        raise ValueError(
            "No readable text found. Your PDF may be scanned or image-based."
        )

    return text.strip()

