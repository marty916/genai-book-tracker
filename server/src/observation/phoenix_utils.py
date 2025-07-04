# observation/phoenix_utils.py

import os
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def setup_phoenix(project_name="genai-book-tracker-lab"):
    tracer_provider = register(
        project_name=project_name,
        endpoint="https://app.phoenix.arize.com/v1/traces",
        auto_instrument=True
    )
    OpenAIInstrumentor().uninstrument()
    OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
    return tracer_provider

def get_openai_client():
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                  