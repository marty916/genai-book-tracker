from typing import Dict, Optional
from src.observation.phoenix_utils import setup_phoenix, get_openai_client

# Initialize these as None, set them up on first use
_tracer_provider = None
_openai_client = None

OPENAI_MODEL = "gpt-4o"  # or your preferred model

def _ensure_initialized():
    """Ensure Phoenix and OpenAI client are initialized."""
    global _tracer_provider, _openai_client
    if _tracer_provider is None:
        _tracer_provider = setup_phoenix()
    if _openai_client is None:
        _openai_client = get_openai_client()
    return _openai_client

def ask_llm(prompt: str) -> str:
    client = _ensure_initialized()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.7,
    )
    answer = response.choices[0].message.content.strip()
    return answer

def get_book_response(user_query: str) -> Dict:
    prompt = f"A user requests a book on '{user_query}'. Reply with book suggestions, but do not invent book titles or authors. Suggest related, real topics if possible."
    response = ask_llm(prompt)
    # Phoenix instrumentation will automatically log/traces this interaction
    return {"response": response}