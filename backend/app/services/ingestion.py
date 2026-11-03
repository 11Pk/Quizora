from uuid import uuid4

from app.services.vector_store import (
    collection,
    embedding_model
)


def create_chunks(text, chunk_size=1000, overlap=200):

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap")

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def ingest_content(content: str, course_id: str):

    if not content or not content.strip():
        raise ValueError("Content cannot be empty")

    if not course_id or not course_id.strip():
        raise ValueError("Course ID cannot be empty")

    # Generate a unique ID for this uploaded document
    document_id = str(uuid4())

    # 1. Split content into chunks
    chunks = create_chunks(content)

    if not chunks:
        raise ValueError("No valid chunks generated")

    # 2. Generate embeddings
    embeddings = embedding_model.encode(
        chunks,
        normalize_embeddings=True
    ).tolist()

    # 3. Generate unique IDs for chunks
    ids = [str(uuid4()) for _ in chunks]

    # 4. Create metadata
    metadatas = [
        {
            "course_id": course_id,
            "document_id": document_id,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    # 5. Store in ChromaDB
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return {
        "document_id": document_id,
        "total_chunks": len(chunks),
        "message": "Content successfully ingested"
    }
