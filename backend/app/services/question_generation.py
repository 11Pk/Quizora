import json
from collections import Counter

from google import genai
from google.genai import types


from app.config.gemini import client, MODEL
from app.schemas.question_schema import (
    QuestionConfig,
    QuestionResponse
)
from app.services.prompts import (
    SYSTEM_PROMPT,
    build_user_prompt
)


def generate_questions(
    topic: str,
    instructions: str,
    question_config: dict,
    context: list[dict],
    learning_history: dict | None = None
):
    # Validate configuration
    config = QuestionConfig.model_validate(question_config)

    # Extract retrieved content
    context_text = [
        item["content"] for item in context
    ]

    if not context_text:
        raise ValueError("No relevant study material found")

    # Build prompt
    user_prompt = build_user_prompt(
        topic=topic,
        instructions=instructions,
        question_config=config.model_dump(),
        context=context_text,
        learning_history=learning_history
    )

    # Generate questions using Gemini
    response = client.models.generate_content(
        model=MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=QuestionResponse
        )
    )

    # Validate generated response
    result = QuestionResponse.model_validate_json(response.text)

    if len(result.questions) != config.total_questions:
        raise ValueError("Incorrect number of questions generated")

    actual_distribution = Counter(
        (q.type, q.marks) for q in result.questions
    )

    expected_distribution = Counter(
        (item.type, item.marks)
        for item in config.distribution
        for _ in range(item.count)
    )

    if actual_distribution != expected_distribution:
        raise ValueError("Generated question distribution is incorrect")

    return result