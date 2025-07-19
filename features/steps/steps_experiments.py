from behave import given, when, then


@given("a nightly scheduled run")
def step_given_nightly_scheduled_run(context):
    raise NotImplementedError("Step definition not implemented yet.")


@when("the Phoenix experiment runs against the full nightly dataset")
def step_when_phoenix_experiment_runs(context):
    raise NotImplementedError("Step definition not implemented yet.")


@then("the accuracy must be above 80%")
def step_then_accuracy_above_80(context):
    raise NotImplementedError("Step definition not implemented yet.")


@then("the hallucination rate should be below 10%")
def step_then_hallucination_below_10(context):
    raise NotImplementedError("Step definition not implemented yet.")