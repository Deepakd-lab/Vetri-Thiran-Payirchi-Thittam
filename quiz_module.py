import json
from typing import Any

from gemini_client import generate_json


QUIZ_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "correct_answer": {"type": "string"},
                    "explanation": {"type": "string"},
                },
                "required": [
                    "question",
                    "options",
                    "correct_answer",
                    "explanation",
                ],
            },
        }
    },
    "required": ["questions"],
}


def _validate_quiz(data: Any, count: int) -> dict:
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        raise ValueError("Gemini returned an invalid quiz structure.")

    questions = data["questions"][:count]
    if not questions:
        raise ValueError("No quiz questions were generated.")

    cleaned = []
    for item in questions:
        if not isinstance(item, dict):
            continue

        options = item.get("options", [])
        if not isinstance(options, list) or len(options) != 4:
            continue

        question = str(item.get("question", "")).strip()
        correct = str(item.get("correct_answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question or not correct:
            continue

        cleaned.append(
            {
                "question": question,
                "options": [str(x).strip() for x in options],
                "correct_answer": correct,
                "explanation": explanation,
            }
        )

    if not cleaned:
        raise ValueError("Generated quiz did not contain valid MCQs.")

    return {"questions": cleaned}


def generate_quiz(text: str, count: int = 3) -> dict:
    prompt = f"""
Create exactly {count} multiple-choice questions from the educational text below.

Rules:
- Each question must have exactly four options.
- Only one option may be correct.
- The correct_answer must exactly match one option.
- Include a brief explanation of the correct answer.
- Questions must be based only on the supplied text.
- Return JSON matching the requested schema.

Educational text:
{text}
"""
    raw = generate_json(
        prompt,
        QUIZ_SCHEMA,
        temperature=0.25,
        max_output_tokens=1800,
    )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Gemini returned malformed JSON.") from exc

    return _validate_quiz(data, count)
