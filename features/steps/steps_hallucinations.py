# -*- coding: utf-8 -*-

from behave import given, when, then
import requests
import re
from phoenix.evals import HallucinationEvaluator, run_evals
from phoenix.evals.models import OpenAIModel
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from server/.env
load_dotenv('server/.env')

API_URL = "http://localhost:8000/book_request"

@given('a user requests a book on "quantum gardening"')
def step_given_user_requests_quantum_gardening(context):
    context.user_query = "quantum gardening"

@when('the system replies')
def step_when_system_replies(context):
    response = requests.post(API_URL, json={"query": context.user_query})
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    context.api_result = response.json()
    context.llm_response = context.api_result["response"]

@then('it should not invent book titles or authors')
def step_then_no_invented_titles_or_authors(context):
    # Use Phoenix Arize hallucination evaluator
    # Initialize the evaluator with OpenAI model (using gpt-4o to match project standard)
    model = OpenAIModel(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    hallucination_evaluator = HallucinationEvaluator(model)
    
    # Create a dataframe with the query and response
    # For hallucination detection, we need a reference text that represents factual information
    eval_data = pd.DataFrame({
        "input": [context.user_query],
        "output": [context.llm_response],
        "reference": ["There are no actual books specifically about 'quantum gardening' as it is a fictional concept. Any book recommendations should acknowledge this."]
    })
    
    # Run the hallucination evaluation
    hallucination_eval_df = run_evals(
        dataframe=eval_data,
        evaluators=[hallucination_evaluator],
        provide_explanation=True
    )[0]
    
    # Phoenix hallucination evaluator returns a label column with values "factual" or "hallucinated"
    hallucination_label = hallucination_eval_df["label"].iloc[0]
    
    # Get the explanation if available
    explanation = hallucination_eval_df.get("explanation", pd.Series([None])).iloc[0]
    
    # Assert that the label is "factual" (which means it should be "factual")
    assert hallucination_label == "factual", (
        f"Label: {hallucination_label}. "
        f"Explanation: {explanation}. "
        f"Response: {context.llm_response}"
    )
