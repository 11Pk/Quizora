import fitz
from pathlib import Path


def parse_pdf(pdf_source: str | Path | bytes) -> str:

    # Open PDF
    if isinstance(pdf_source, bytes):
        pdf = fitz.open(stream=pdf_source, filetype="pdf")
    else:
        pdf = fitz.open(pdf_source)

    extracted_content = []

    try:
        # Extract text from each page
        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text("text").strip()

            if text:
                extracted_content.append(
                    f"\n--- Page {page_number} ---\n{text}"
                )

    finally:
        pdf.close()

    if not extracted_content:
        raise ValueError(
            "No text could be extracted from the PDF. "
            "It may be a scanned document."
        )

    return "\n".join(extracted_content)