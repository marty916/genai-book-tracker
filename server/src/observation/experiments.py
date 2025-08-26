from phoenix.evals import HallucinationEvaluator, QAEvaluator, OpenAIModel
from phoenix.experiments import run_experiment
from phoenix.datasets import Dataset
import pandas as pd
from pandas import DataFrame

class EvalExperimentation:
    
    def __init__(self, api_key: str):
        self.model = OpenAIModel(model="gpt-4o", api_key=api_key)
        self.evaluators = [
            HallucinationEvaluator(self.model),
            QAEvaluator(self.model)
        ]
        self.task = lambda ex: {"output": call_llm(ex["input"])}
        
    def experiment(self, df: DataFrame, task: callable, evaluators: list, experiment_name: str):
        
        dataset = Dataset.from_pandas(df)
        return run_experiment(
            dataset=dataset,
            task=task,
            evaluators=evaluators,
            experiment_name=experiment_name
        )
