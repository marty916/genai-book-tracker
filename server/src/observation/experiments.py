from phoenix.evals import HallucinationEvaluator, QAEvaluator, OpenAIModel
from phoenix.experiments import run_experiment
from phoenix.datasets import Dataset
import pandas as pd

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
