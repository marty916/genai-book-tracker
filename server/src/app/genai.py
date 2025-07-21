import os
from typing import Dict
from dotenv import load_dotenv
from ..app.llm_client import LLMClient
from ..observation.phoenix_utils import setup_phoenix
from ..observation.evaluator import HallucinationEvaluation

# Load environment variables from server/.env
load_dotenv()

# Model names
USER_MODEL = "gpt-3.5-turbo"
EVAL_MODEL = "gpt-4o"

# Singleton for Phoenix setup
_tracer_provider = None

# Singleton for LLM client
_llm_client = None

def _ensure_initialized():
    global _tracer_provider, _llm_client
    if _tracer_provider is None:
        _tracer_provider = setup_phoenix()
    if _llm_client is None:
        _llm_client = LLMClient(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=USER_MODEL
        )
    return _llm_client

def ask_llm(prompt: str) -> str:
    llm_client = _ensure_initialized()
    return llm_client.chat(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.7,
    )

def get_book_response(user_query: str) -> Dict:
    ## prompt = f"A user requests a book on '{user_query}'. Reply with book suggestions, but do not invent book titles or authors. ## Suggest related, real topics if possible."
    
    prompt = f"A user requests book recommendations on '{user_query}'. Provide only real, existing books and authors related to this topic. If no matching books are found, clearly inform the user that no matching books were found. Do not create fictitious titles or authors."
    
    response = ask_llm(prompt)
    # Phoenix instrumentation will automatically log/traces this interaction
    return {"response": response}

