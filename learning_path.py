import json

from gemini_client import generate_json


LEARNING_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string"},
        "level": {"type": "string"},
        "weeks": {"type": "integer"},
        "overview": {"type": "string"},
        "plan": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "week": {"type": "integer"},
                    "focus": {"type": "string"},
                    "topics": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "practice": {"type": "string"},
                    "resources": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "week",
                    "focus",
                    "topics",
                    "practice",
                    "resources",
                ],
            },
        },
    },
    "required": ["topic", "level", "weeks", "overview", "plan"],
}


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    weeks: int = 6,
) -> dict:
    prompt = f"""
Create a personalized learning path.

Topic: {topic}
Current level: {level}
Duration: {weeks} weeks

Requirements:
- Move from foundational concepts toward more advanced concepts.
- Adapt the difficulty to the learner's level.
- Give a weekly focus, topics, practical activity, and resource suggestions.
- Resource suggestions may be types of resources (documentation, tutorial,
  book, video course); do not invent exact URLs.
- Keep the plan realistic for self-study.
- Return JSON matching the supplied schema.
"""
    raw = generate_json(
        prompt,
        LEARNING_SCHEMA,
        temperature=0.35,
        max_output_tokens=2400,
    )
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Gemini returned malformed learning-path JSON.") from exc
