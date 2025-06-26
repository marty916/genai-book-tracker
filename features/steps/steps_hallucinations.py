from behave import given, when, then
import requests
import re

API_URL = "http://localhost:8000/book_request"

@given('a user requests a book on "quantum gardening"')
def step_given_user_requests_quantum_gardening(context):
    context.user_query = "quantum gardening"

@when('the system replies')
def step_when_system_replies(context):
    response = requests.post(API_URL, json={"query": context.user_query})
    context.api_result = response.json()
    context.llm_response = context.api_result["response"]

@then('it should not invent book titles or authors')
def step_then_no_invented_titles_or_authors(context):
    # Check for invented book titles/authors (very basic heuristic: look for book-like patterns)
    hallucination_patterns = [
        r'"[^"]+" by [^\n\r]+',  # "Book Title" by Author
        r'\bby [A-Z][a-z]+ [A-Z][a-z]+\b',  # by Firstname Lastname
    ]
    for pattern in hallucination_patterns:
        if re.search(pattern, context.llm_response):
            assert False, f"Response appears to invent a book or author: {context.llm_response}"

@then('it should suggest related, real topics if possible')
def step_then_suggest_related_real_topics(context):
    # Check for suggestion of related, real topics (look for keywords like 'related', 'real', 'actual', etc.)
    related_keywords = ["related", "real", "actual", "existing", "non-fiction", "science", "gardening"]
    found = any(word in context.llm_response.lower() for word in related_keywords)
    assert found, f"Response does not suggest related, real topics: {context.llm_response}"
