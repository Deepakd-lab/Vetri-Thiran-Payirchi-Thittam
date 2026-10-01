from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the educational passage below for quick revision.

Requirements:
- Preserve the important facts and ideas.
- Remove repetition and unnecessary detail.
- Use simple language.
- Prefer short paragraphs and bullet points where useful.
- Do not add information that is not supported by the passage.

Passage:
{text}
"""
    return generate_text(prompt, temperature=0.2, max_output_tokens=1200)
