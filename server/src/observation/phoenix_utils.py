# observation/phoenix_utils.py

from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from dotenv import load_dotenv

load_dotenv('server/.env')

def setup_phoenix(project_name="genai-book-tracker-lab"):
    tracer_provider = register(
        project_name=project_name,
        endpoint="https://app.phoenix.arize.com/v1/traces",
        auto_instrument=True
    )
    OpenAIInstrumentor().uninstrument()
    OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
    return tracer_provider
