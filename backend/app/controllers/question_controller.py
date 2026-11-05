from app.services.retriever import retrieve_context
from app.services.question_generation import generate_questions


def generate_questions_controller(
    course_id: str,
    topic: str,
    instructions: str,
    question_config: dict,
    learning_history: dict | None = None
):
    # 1. Retrieve relevant context from the knowledge base
    context = retrieve_context(
        topic=topic,
        course_id=course_id,
        top_k=5
    )

    if not context:
        raise ValueError(
            "No relevant study material found for this topic."
        )

    # 2. Generate questions using Gemini
    questions = generate_questions(
        topic=topic,
        instructions=instructions,
        question_config=question_config,
        context=context,
        learning_history=learning_history
    )

    return {
        "message": "Questions generated successfully",
        "course_id": course_id,
        "topic": topic,
        "questions": questions.model_dump()
    }