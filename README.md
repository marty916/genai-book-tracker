# genai-book-tracker

A robust, SOLID-principled FastAPI application for book recommendation and LLM response evaluation, with Phoenix Arize integration for hallucination detection and CI/CD-friendly Gherkin/Behave tests.

---

## Features
- **Book Recommendation API**: Suggests real books and related topics, never invents titles/authors.
- **LLM Model Selection**: Uses `gpt-3.5-turbo` for user-facing queries, `gpt-4o` for all evaluation tasks.
- **Phoenix Arize Integration**: Automated hallucination detection and evaluation logging.
- **Behavior-Driven Testing**: Gherkin feature files and Behave steps for CI/CD pipelines.
- **SOLID Architecture**: Clean separation of concerns, extensible and maintainable codebase.

---

## Project Structure
```
server/
  src/
    llm_client.py                # LLMClient abstraction for OpenAI
    main.py                      # FastAPI app entrypoint
    genai.py                     # Main business logic, API, and evaluation interface
    observation/
      phoenix_utils.py           # Phoenix setup and instrumentation
      evaluator.py               # Hallucination evaluation logic (Phoenix + gpt-4o)
      test_set.csv               # Test/eval dataset
features/
  hallucination.feature          # Gherkin feature for hallucination prevention
  steps/
    steps_hallucinations.py      # Behave step definitions
README.md
PHOENIX_INTEGRATION.md          # Details on Phoenix integration
```

---

## Setup & Installation

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   cd server
   python -m venv .venv
   .venv/Scripts/activate  # or source .venv/bin/activate on macOS/Linux
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   - Copy `.env.example` to `.env` in the `server` directory (or create `.env`):
     ```
     OPENAI_API_KEY=sk-...
     ```

---

## Running the API Server

From the project root:
```bash
cd server
uvicorn src.main:app --reload
```
- The API will be available at `http://localhost:8000`.
- Interactive docs: `http://localhost:8000/docs`

---

## API Usage
- **POST /book_request**
  - Request body: `{ "query": "quantum gardening" }`
  - Response: `{ "response": "..." }`

---

## Running Tests & Evaluations

### 1. Run Behave BDD tests
```bash
behave features/hallucination.feature
```

### 2. Run Phoenix hallucination evaluation test
```bash
python test_phoenix_integration.py
```

---

## Model Usage Policy
- **User queries**: Always use `gpt-3.5-turbo` (fast, cost-effective, good for general recommendations).
- **Evaluation (Phoenix, hallucination detection, etc.)**: Always use `gpt-4o` (higher accuracy for evals).
- Model selection is enforced in code via the `LLMClient` abstraction and the evaluation module.

---

## SOLID Principles & Architecture
- **Single Responsibility**: Each module/class has one clear job (LLM client, Phoenix setup, evaluation, API logic).
- **Open/Closed**: Easy to add new models or evaluation strategies.
- **Liskov Substitution**: LLMClient and evaluation classes can be swapped/extended.
- **Interface Segregation**: Minimal, focused interfaces.
- **Dependency Inversion**: High-level modules depend on abstractions, not concrete implementations.

---

## Troubleshooting
- **500 Internal Server Error**: Usually means the OpenAI API key is missing or not loaded. Ensure `.env` is present and loaded, or set `OPENAI_API_KEY` in your environment.
- **JSONDecodeError in Behave tests**: The API server is not running or is returning an error. Start the server and check logs.
- **Phoenix evaluation errors**: Ensure you have access to `gpt-4o` and your API key is valid.

---

## Credits
- Built with [FastAPI](https://fastapi.tiangolo.com/), [Phoenix Arize](https://arize.com/phoenix/), [OpenAI](https://platform.openai.com/), [Behave](https://behave.readthedocs.io/), and [SOLID principles](https://en.wikipedia.org/wiki/SOLID).
