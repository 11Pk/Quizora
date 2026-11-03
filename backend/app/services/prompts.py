import json


SYSTEM_PROMPT = """
You are an expert question paper generator.

Generate questions strictly using the supplied study material.

Rules:
1. Generate exactly the requested number of questions.
2. Follow the specified question type distribution.
3. Assign exactly the specified marks to each question.
4. Questions must be relevant to the given topic.
5. Follow the teacher's instructions.
6. Do not generate questions whose answers cannot be supported
   by the provided study material.
7. Avoid duplicate or repetitive questions.
8. MCQs must have exactly four options and one correct answer.
9. Short and long answer questions must include an expected answer
   and a marking scheme.
10. Return valid JSON matching the requested response structure.
"""


def build_user_prompt(
    topic,
    instructions,
    question_config,
    context,
    learning_history=None
):
    return f"""
Topic: {topic}

Teacher's Instructions:
{instructions}

Question Configuration:
{json.dumps(question_config, indent=2)}

Study Material:
{chr(10).join(context)}

Student Learning History:
{json.dumps(learning_history, indent=2)
 if learning_history else "Not provided"}

Generate the questions according to all the instructions.
"""