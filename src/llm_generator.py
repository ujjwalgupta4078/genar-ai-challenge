import os
from typing import Dict, Any

from dotenv import load_dotenv
from google import genai


# ==========================================
# LLM CONFIGURATION
# ==========================================

load_dotenv()

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash"
)


# ==========================================
# LLM CLIENT
# ==========================================

def get_client() -> genai.Client:
    """
    Create a Gemini client using the API key
    stored in the environment.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Add it to your .env file before "
            "running LLM generation."
        )

    return genai.Client(
        api_key=api_key
    )


# ==========================================
# GENERATE PADER NARRATIVE
# ==========================================

def generate_pader_report(
    prompt: str
) -> str:
    """
    Generate a PADER-style narrative from the
    controlled evidence prompt.

    The prompt is responsible for grounding
    the model to deterministic evidence.
    """

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# ==========================================
# GENERATE FROM STRUCTURED EVIDENCE
# ==========================================

def generate_from_evidence(
    evidence: Dict[str, Any],
    prompt_builder
) -> str:
    """
    Build the controlled prompt from structured
    evidence and generate the final narrative.
    """

    prompt = prompt_builder(evidence)

    return generate_pader_report(prompt)