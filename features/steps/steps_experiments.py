from behave import given, when, then
import pandas as pd
from werver.src.observation.experiments import EvalExperimentation

@given("a nightly scheduled run")
def step_given_nightly_scheduled_run(context):
    df = pd.read_csv("test_set.csv")
    experiment_name = "Nightly Eval Experiment"



@when("the Phoenix experiment runs against the full nightly dataset")
def step_when_phoenix_experiment_runs(context):
    experiment_run = experiment(df, context.task, context.evaluators, experiment_name)
    experiment_results_df = experiment_run.get_evaluations()
    context.experiment_results_df = experiment_results_df


@then("the accuracy must be above 80%")
def step_then_accuracy_above_80(context):
    assert context.experiment_results_df["accuracy"].mean() > 0.8


@then("the hallucination rate should be below 10%")
def step_then_hallucination_below_10(context):
    assert context.experiment_results_df["hallucination_rate"].mean() < 0.1
