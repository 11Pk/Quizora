from pydantic import BaseModel, Field, model_validator
from typing import Literal


class QuestionTypeConfig(BaseModel):
    type: Literal["mcq", "short_answer", "long_answer"]
    count: int = Field(gt=0)
    marks: int = Field(gt=0)


class QuestionConfig(BaseModel):
    total_questions: int = Field(gt=0)
    distribution: list[QuestionTypeConfig]

    @model_validator(mode="after")
    def validate_total(self):
        total = sum(item.count for item in self.distribution)

        if total != self.total_questions:
            raise ValueError(
                "Sum of question counts must equal total_questions"
            )

        return self


class Question(BaseModel):
    question: str
    type: Literal["mcq", "short_answer", "long_answer"]
    marks: int

    options: list[str] | None = None
    correct_answer: str | None = None

    expected_answer: str | None = None
    marking_scheme: list[str] | None = None


class QuestionResponse(BaseModel):
    questions: list[Question]