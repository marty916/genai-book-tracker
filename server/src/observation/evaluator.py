import os
import pandas as pd
from phoenix.evals import HallucinationEvaluator, run_evals
from phoenix.evals.models import OpenAIModel

class HallucinationEvaluation:
    """
    Handles hallucination evaluation using Phoenix and gpt-4o.
    """
    def __init__(self, api_key: str):
        self.model = OpenAIModel(model="gpt-4o", api_key=api_key)
        self.evaluator = HallucinationEvaluator(self.model)

    def evaluate(self, query: str, response: str, reference: str) -> dict:
        eval_data = pd.DataFrame({
            "input": [query], 
            "output": [response],
            "reference": [reference]
        })
        eval_df = run_evals(
            dataframe=eval_data,
            evaluators=[self.evaluator],
            provide_explanation=True
        )[0]
        label = eval_df["label"].iloc[0]
        explanation = eval_df.get("explanation", pd.Series([None])).iloc[0]
        score = 1.0 if label == "factual" else 0.0
        return {
            "label": label,
            "score": score,
            "explanation": explanation
        }
