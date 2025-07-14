# Phoenix Arize Integration for Hallucination Detection

This document explains how Phoenix Arize is integrated into the Behave test suite for detecting hallucinated book recommendations.

## Overview

The integration uses Phoenix Arize's `HallucinationEvaluator` to automatically detect when the LLM generates fictional book titles or authors. This is particularly important for the "quantum gardening" test case, where no real books exist on this fictional topic.

## How It Works

1. **Test Scenario**: The Gherkin feature file defines a scenario where a user requests books on "quantum gardening"
2. **API Call**: The test makes a request to the book recommendation API
3. **Hallucination Evaluation**: Phoenix evaluates the response against a reference text that clarifies quantum gardening is fictional
4. **Score Threshold**: The test passes if the hallucination score is above 0.8 (meaning the response is factual/not hallucinated)

## Implementation Details

### Step Definition

The `@then('it should not invent book titles or authors')` step in `features/steps/steps_hallucinations.py`:

1. Initializes a Phoenix `HallucinationEvaluator` with OpenAI's GPT-4o model
2. Creates a DataFrame with:
   - `input`: The user's query ("quantum gardening")
   - `output`: The LLM's response
   - `reference`: Factual information stating quantum gardening is fictional
3. Runs the evaluation and extracts the label ("factual" or "hallucinated")
4. Converts the label to a score (1.0 for "factual", 0.0 for "hallucinated")
5. Asserts the score is above 0.8

### Environment Variables

Required environment variable:
- `OPENAI_API_KEY`: Your OpenAI API key for the evaluation model

### CI/CD Integration

To run in CI/CD:

```bash
# Install dependencies
pip install -r server/requirements.txt

# Set environment variable
export OPENAI_API_KEY="your-api-key"

# Run the specific test
behave features/hallucination.feature

# Or run all tests
behave
```

## Testing the Integration

Use the provided test script to verify the integration:

```bash
python test_phoenix_integration.py
```

This script tests both:
- A factual response (should pass)
- A hallucinated response (should fail)

## Troubleshooting

1. **Missing API Key**: Ensure `OPENAI_API_KEY` is set in your environment
2. **Network Issues**: Phoenix needs to connect to OpenAI's API
3. **DataFrame Columns**: Phoenix expects specific column names (`input`, `output`, `reference`)

## Benefits

- **Automated Detection**: No need for manual regex patterns to detect book titles
- **Intelligent Evaluation**: Uses GPT-4o to understand context and nuance
- **Explainable Results**: Phoenix provides explanations for its evaluations
- **CI/CD Ready**: Integrates seamlessly into automated testing pipelines