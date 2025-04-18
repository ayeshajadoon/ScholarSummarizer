import requests
import re
import os
def sanitize_text(text):
    # Remove special characters and non-standard characters
    cleaned_text = re.sub(r'[^A-Za-z0-9\s,.!?]', '', text)  # Keep only alphanumeric characters and common punctuation
    return cleaned_text

from dotenv import load_dotenv
load_dotenv()


API_TOKEN = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def summarize_text(text):
    text = sanitize_text(text)  # Optional: Clean the text if needed
    payload = {
        "inputs": text,
        "parameters": {"max_length": 200, "min_length": 50},
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list) and "summary_text" in result[0]:
                return result[0]["summary_text"]
            else:
                return f"Unexpected response format: {result}"
        except Exception as e:
            return f"Error parsing response: {e}"
    else:
        try:
            error_message = response.json().get("error", "Unknown error")
            return f"Error {response.status_code}: {error_message}"
        except Exception as e:
            return f"Error {response.status_code}: Could not parse error message"
