# observation/log_to_phoenix.py

import pandas as pd
from phoenix_utils import setup_phoenix, get_openai_client
from dotenv import load_dotenv
load_dotenv()


def run_inference_on_test_set(test_set_path):
    test_set = pd.read_csv(test_set_path)
    client = get_openai_client()
    for idx, row in test_set.iterrows():
        prompt = row['question']
        reference = row['reference_answer']
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        model_response = response.choices[0].message.content.strip()
        # Print for workshop feedback
        print(f"\nPrompt: {prompt}\nModel: {model_response}\nReference: {reference}\n")

if __name__ == "__main__":
    setup_phoenix()  # Registers and instruments OpenAI
    run_inference_on_test_set("observation/test_set.csv")