import os
import pandas as pd
import phoenix as px
from phoenix.evals import (
    HallucinationEvaluator,
    OpenAIModel,
    QAEvaluator,
    RelevanceEvaluator,
    run_evals,
)
from phoenix.otel import register
from phoenix.session.evaluation import get_qa_with_reference, get_retrieved_documents
from phoenix.trace import DocumentEvaluations, SpanEvaluations

from dotenv import load_dotenv

# Load environment variables from server/.env
load_dotenv('server/.env')

def run_evaluations():
    queries_df = get_qa_with_reference(px.Client())
    retrieved_documents_df = get_retrieved_documents(px.Client())
    
    eval_model = OpenAIModel(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    hallucination_evaluator = HallucinationEvaluator(eval_model)
    qa_correctness_evaluator = QAEvaluator(eval_model)
    relevance_evaluator = RelevanceEvaluator(eval_model)

    hallucination_eval_df, qa_correctness_eval_df = run_evals(
        dataframe=queries_df,
        evaluators=[hallucination_evaluator, qa_correctness_evaluator],
        provide_explanation=True,
    )
    relevance_eval_df = run_evals(
        dataframe=retrieved_documents_df,
        evaluators=[relevance_evaluator],
        provide_explanation=True,
    )[0]

    px.Client().log_evaluations(
        SpanEvaluations(eval_name="Hallucination", dataframe=hallucination_eval_df),
        SpanEvaluations(eval_name="QA Correctness", dataframe=qa_correctness_eval_df),
        DocumentEvaluations(eval_name="Relevance", dataframe=relevance_eval_df),
    )
    
def task():
    return 