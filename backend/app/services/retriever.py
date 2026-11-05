from app.services.vector_store import (
    collection,
    embedding_model
)


def retrieve_context(
    topic: str,
    course_id: str,
    top_k: int = 5
):

    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty")

    if not course_id or not course_id.strip():
        raise ValueError("Course ID cannot be empty")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    # 1. Convert topic into embedding
    query_embedding = embedding_model.encode(
        topic,
        normalize_embeddings=True
    ).tolist()
    print("Collection:", collection.name)
    print("Count:", collection.count())
    print("Topic:", topic)
    print("Course ID:", course_id)
    print("Course ID type:", type(course_id))
    # 2. Retrieve relevant chunks from ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"course_id": course_id},
        include=["documents", "metadatas", "distances"]
    )
    print("Documents:", results["documents"])
    print("Distances:", results["distances"])
    print("Metadata:", results["metadatas"])
    # 3. Handle empty results
    if not results["documents"] or not results["documents"][0]:
        return []

    # 4. Prepare retrieved context
    retrieved_context = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        retrieved_context.append({
            "content": document,
            "metadata": metadata,
            "distance": distance
        })

    return retrieved_context
