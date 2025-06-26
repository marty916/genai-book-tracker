# Observation & Evaluation Setup

This folder contains scripts and data for logging model inferences and evaluation traces to Phoenix (Arize).

- `test_set.csv` - Test/eval dataset
- `phoenix_utils.py` - Helpers for Phoenix instrumentation and OpenAI setup
- `log_to_phoenix.py` - Script to run model on test set and log to Phoenix
- `sample_dashboard.ipynb` - Notebook for interactive analysis

## Usage

1. Set your environment variables (see above).
2. Run: `python observation/log_to_phoenix.py`
3. View results and traces in your Phoenix Cloud dashboard.

This code follows SOC/SRP principles: business logic stays in `src/`, evaluation & observability are here.
