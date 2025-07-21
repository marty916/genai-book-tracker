# -*- coding: utf-8 -*-

from behave import given, when, then
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add server src to path to import internal modules
server_src_path = Path(__file__).parent.parent / "server" / "src"
sys.path.insert(0, str(server_src_path))

from server.src.app.genai import get_book_response
from server.src.observation.evaluator import HallucinationEvaluation

# Load environment variables from server/.env
load_dotenv('server/.env')

# Initialize the hallucination evaluator once
_hallucination_eval = None

def _get_evaluator():
    """Lazy initialization of hallucination evaluator"""
    global _hallucination_eval
    if _hallucination_eval is None:
        _hallucination_eval = HallucinationEvaluation(
            api_key=os.getenv("OPENAI_API_KEY")
        )
    return _hallucination_eval

@given('a user requests a book on "quantum gardening"')
def step_given_user_requests_quantum_gardening(context):
    context.user_query = "quantum gardening"

@when('the system replies')
def step_when_system_replies(context):
    # Use the existing get_book_response function from genai.py
    result = get_book_response(context.user_query)
    context.llm_response = result["response"]
    print(f"LLM Response: {context.llm_response}")

@then('it should not invent book titles or authors')
def step_then_no_invented_titles_or_authors(context):
    # Define reference text for quantum gardening (fictional concept)
    reference_text = (
        "There are no actual books specifically about 'quantum gardening' as it is "
        "a fictional concept. Any book recommendations should acknowledge this and "
        "state that the book doesn't exist."
    )
    
    # Use the existing HallucinationEvaluation class
    evaluator = _get_evaluator()
    result = evaluator.evaluate(
        query=context.user_query,
        response=context.llm_response,
        reference=reference_text
    )
    
    # Extract evaluation results
    label = result["label"]
    score = result["score"]
    explanation = result["explanation"]
    
    # Assert that the response is factual (not hallucinated)
    assert label == "factual", (
        f"Hallucination detected! "
        f"Label: {label}, Score: {score:.2f}. "
        f"Explanation: {explanation}. "
        f"Response: {context.llm_response}"
    )
    
    # Print success message with score
    print(f"✓ Response passed hallucination check (label: {label}, score: {score:.2f})")
