import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

if not API_TOKEN:
    raise ValueError("Hugging Face API key not found. Please add it to the .env file.")

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Failed to fetch response:\n", response.text)
        return None
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Could not decode JSON response")
        return None

print("🤖 Generating response from Mixtral LLM...")
output = query({
    "inputs": "Hello, I'm TailorTalk AI! What can you do?",
    "parameters": {
        "max_new_tokens": 100,
        "temperature": 0.7
    }
})

if output and isinstance(output, list):
    print("\n📝 Generated Text:\n", output[0]['generated_text'])
else:
    print("No valid response from model.")
