from pydantic import BaseModel


class KnowledgeResponse(BaseModel):
    message: str
    course_id: str
    content_type: str
    document_id: str
    total_chunks: int