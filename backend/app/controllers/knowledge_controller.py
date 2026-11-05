from app.services.pdf_parsing import parse_pdf
from app.services.ingestion import ingest_content


def add_content_controller(
    course_id: str,
    content_type: str,
    file_bytes: bytes
):
    if content_type == "pdf":
        content = parse_pdf(file_bytes)

    else:
        raise ValueError(
            f"Unsupported content type: {content_type}"
        )

    result = ingest_content(
        content=content,
        course_id=course_id
    )

    return {
        "message": "Content added to knowledge base successfully",
        "course_id": course_id,
        "content_type": content_type,
        **result
    }