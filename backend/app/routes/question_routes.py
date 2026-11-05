from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.controllers.question_controller import generate_questions_controller
from app.schemas.question_schema import GenerateQuestionsRequest
router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


@router.post("/generate")
def generate_questions_route(request: GenerateQuestionsRequest):
    try:
        return generate_questions_controller(
            course_id=request.course_id,
            topic=request.topic,
            instructions=request.instructions,
            question_config=request.question_config,
            learning_history=request.learning_history
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))