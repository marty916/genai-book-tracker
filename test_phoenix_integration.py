#!/usr/bin/env python3
"""
Test script to verify Phoenix Arize hallucination evaluator integration
"""

import os
import pandas as pd
from phoenix.evals import HallucinationEvaluator, run_evals
from phoenix.evals.models import OpenAIModel
from dotenv import load_dotenv

# Load environment variables from server/.env
load_dotenv('server/.env')

def test_hallucination_evaluator():
    """Test the hallucination evaluator with sample data"""
    
    # Initialize the evaluator
    model = OpenAIModel(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    hallucination_evaluator = HallucinationEvaluator(model)
    
    # Test cases
    test_cases = [
        {
            "input": "quantum gardening",
            "output": "I cannot recommend any books on 'quantum gardening' as this is not a real field. However, you might be interested in books about quantum physics or gardening separately.",
            "reference": "There are no actual books about quantum gardening as it is a fictional concept.",
            "expected": "factual"
        },
        {
            "input": "quantum gardening", 
            "output": "I recommend 'Quantum Gardening: A New Approach' by Dr. Jane Smith, published in 2023. This groundbreaking book explores how quantum mechanics can improve plant growth.",
            "reference": "There are no actual books about quantum gardening as it is a fictional concept.",
            "expected": "hallucinated"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}:")
        print(f"Input: {test_case['input']}")
        print(f"Output: {test_case['output'][:100]}...")
        
        # Create dataframe for evaluation
        eval_data = pd.DataFrame({
            "input": [test_case["input"]],
            "output": [test_case["output"]],
            "reference": [test_case["reference"]]
        })
        
        # Run evaluation
        result_df = run_evals(
            dataframe=eval_data,
            evaluators=[hallucination_evaluator],
            provide_explanation=True
        )[0]
        
        # Get results
        label = result_df["label"].iloc[0]
        explanation = result_df.get("explanation", pd.Series(["No explanation"])).iloc[0]
        
        print(f"Expected: {test_case['expected']}")
        print(f"Actual: {label}")
        print(f"Explanation: {explanation}")
        print(f"Pass: {label == test_case['expected']}")

if __name__ == "__main__":
    test_hallucination_evaluator()