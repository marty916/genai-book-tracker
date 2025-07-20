from phoenix.evals import HallucinationEvaluator, QAEvaluator, OpenAIModel
from phoenix.experiments import run_experiment
from phoenix.datasets import Dataset
import pandas as pd

class EvalExperimentation:
    
    def __init__(self, api_key: str):
        self.model = OpenAIModel(model="gpt-4o", api_key=api_key)
        self.evaluators = [
            HallucinationEvaluator(self.model),
            QAEvaluator(self.model)
        ]
        self.task = lambda ex: {"output": call_llm(ex["input"])}
        
    def experiment(self, dataset: Dataset, task: callable, evaluators: list, experiment_name: str):
        return run_experiment(
            dataset=dataset,
            task=task,
            evaluators=evaluators,
            experiment_name="Nightly Eval Experiment"
        )
        
        
df = pd.read_csv("test_set.csv")
dataset = Dataset.from_pandas(df)
experiment = run_experiment(
    dataset=dataset,
    task=lambda ex: {"output": call_llm(ex["input"])},
    evaluators=[
        HallucinationEvaluator(OpenAIModel("gpt-4")),
        QAEvaluator(OpenAIModel("gpt-4"))
    ],
    experiment_name="Nightly Eval Experiment"
)
results_df = experiment.get_evaluations()
