import os

from gemini_client import generate_text


def _local_explanation(topic: str) -> str:
    """
    Optional LaMini-Flan-T5 implementation.

    Enable it with USE_LOCAL_EXPLANATION=true after installing the optional
    dependencies listed in requirements-local.txt. The import is intentionally
    lazy so the normal Gemini application does not require PyTorch/Transformers.
    """
    from transformers import pipeline

    model_name = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M",
    )
    generator = pipeline("text2text-generation", model=model_name)
    prompt = (
        "Explain the following topic for a beginner in simple language. "
        "Give a short definition, key idea, and one example.\n\n"
        f"Topic: {topic}"
    )
    result = generator(prompt, max_new_tokens=300, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    use_local = os.getenv("USE_LOCAL_EXPLANATION", "false").lower() == "true"

    if use_local:
        try:
            return _local_explanation(topic)
        except Exception:
            # If the optional local model is unavailable, keep the application
            # usable by falling back to Gemini.
            pass

    prompt = f"""
You are EduGenie, an educational tutor.

Explain this topic to a beginner:
{topic}

Use this structure:
1. Simple definition
2. How it works
3. Easy example
4. Key points to remember

Keep the explanation concise, friendly, and easy to understand.
"""
    return generate_text(prompt, temperature=0.25, max_output_tokens=1000)
