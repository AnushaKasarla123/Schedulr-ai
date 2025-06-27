import os
import requests
from dotenv import load_dotenv
from calendar_utils import list_events, create_event

# Load environment variables
load_dotenv()

# ==== 1. Show upcoming calendar events ====
print("📅 Upcoming Events:")
list_events()

# ==== 2. Create a test event ====
print("\n📅 Creating Test Event...")
create_event(
    "TailorTalk Sample Meeting",
    "2025-06-28T11:00:00",
    "2025-06-28T11:30:00"
)

# ==== 3. Generate AI Response ====
print("\n🤖 Generating response from Mixtral LLM...")

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
        print("❌ Error decoding response")
        return None

output = query({
    "inputs": "Hello, I'm TailorTalk AI. How can I assist with your wedding planning today?",
    "parameters": {"max_new_tokens": 60}
})

# Print LLM output
if output and isinstance(output, list) and 'generated_text' in output[0]:
    print("\n📝 Generated Text:\n", output[0]['generated_text'])
else:
    print("No valid response from model.")
