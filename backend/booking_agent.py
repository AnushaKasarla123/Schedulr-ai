import os
import re
import requests
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from calendar_utils import create_event, list_events
from datetime import datetime, timedelta
import dateparser
from dateparser.search import search_dates

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

if not API_TOKEN:
    raise ValueError("HUGGINGFACE_API_KEY not found in .env")

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Define a function to call Hugging Face LLM
def call_huggingface_llm(user_message):
    url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

    prompt = (
        "You are Schedulr AI, a helpful and friendly meeting scheduling assistant. "
        "Respond clearly and concisely in one or two short sentences. "
        "Focus on scheduling logic, not on small talk or unrelated topics.\n\n"
        f"{user_message}"
    )
    ...




    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 100}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            generated_text = response.json()[0]['generated_text'].strip()

            # Clean hallucinated roles
            for tag in ["User:", "Assistant:", "TailorTalk:", "user:", "assistant:"]:
                if tag in generated_text:
                    generated_text = generated_text.split(tag)[-1].strip()

            return generated_text
        else:
            print("❌ Error:", response.text)
            return "❌ Error fetching response"
    except Exception as e:
        print("❌ Exception:", e)
        return "❌ Error fetching response"


# Datetime Parser
def parse_datetime(text):
    results = search_dates(
        text,
        settings={
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': datetime.now(),
            'DATE_ORDER': 'DMY'
        }
    )

    if results:
        _, parsed_dt = results[0]

        # Format with timezone (manually add +05:30 if no tzinfo)
        start = parsed_dt.strftime("%Y-%m-%dT%H:%M:%S")
        end_dt = parsed_dt + timedelta(hours=1)
        end = end_dt.strftime("%Y-%m-%dT%H:%M:%S")

        # Append +05:30 if timezone missing
        if not parsed_dt.tzinfo:
            start += "+05:30"
        if not end_dt.tzinfo:
            end += "+05:30"

        return {
            "title": "TailorTalk Appointment",
            "start": start,
            "end": end
        }

    return None

from calendar_utils import create_event, list_events, delete_event

def planner_node(state):
    user_input = state["user_input"]
    print("🤖 Schedulr AI received:", user_input)

    confirm_phrases = ["yes", "okay", "sure", "go ahead", "book it"]
    if any(p in user_input.lower() for p in confirm_phrases):
        suggested = state.get("suggested_time")
        if suggested:
            calendar_link = create_event("Schedulr AI Appointment", suggested["start"], suggested["end"])
            response = (
                f"✅ Great! Your meeting has been booked.\n📅 [Click to view event]({calendar_link})"
                if calendar_link else "⚠️ Sorry, I couldn't create the event. Please try again."
            )
            return {"user_input": user_input, "response": response, "suggested_time": None}

    if "cancel" in user_input.lower() or "delete" in user_input.lower():
        datetime_info = parse_datetime(user_input)
        if datetime_info:
            success = delete_event(datetime_info["start"], datetime_info["end"])
            response = (
                "🗑️ Your event has been successfully cancelled."
                if success else "⚠️ I couldn’t find any event to cancel at that time."
            )
        else:
            response = "⚠️ Please specify the time of the event you'd like to cancel."
        return {"user_input": user_input, "response": response, "suggested_time": None}

    datetime_info = parse_datetime(user_input)
    if datetime_info:
        start = datetime_info["start"]
        end = datetime_info["end"]
        existing_events = list_events(start, end)

        if existing_events:
            from datetime import datetime as dt
            try:
                end_dt = dt.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                end_dt = dt.strptime(end, "%Y-%m-%dT%H:%M:%S+05:30")

            suggested_start = end_dt
            suggested_end = end_dt + timedelta(hours=1)
            suggested_start_str = suggested_start.strftime("%Y-%m-%dT%H:%M:%S+05:30")
            suggested_end_str = suggested_end.strftime("%Y-%m-%dT%H:%M:%S+05:30")

            suggested_events = list_events(suggested_start_str, suggested_end_str)

            if not suggested_events:
                readable_time = suggested_start.strftime("%I:%M %p on %B %d")
                return {
                    "user_input": user_input,
                    "response": f"⚠️ That time is already booked. Would you like to try **{readable_time}** instead?",
                    "suggested_time": {"start": suggested_start_str, "end": suggested_end_str}
                }
            else:
                return {"user_input": user_input, "response": "⚠️ That time is already booked. Please suggest another time.", "suggested_time": None}
        else:
            calendar_link = create_event("Schedulr AI Appointment", start, end)
            response = (
                f"✅ Your meeting has been scheduled!\n📅 [Click to view event]({calendar_link})"
                if calendar_link else "⚠️ Something went wrong while creating the calendar event."
            )
            return {"user_input": user_input, "response": response, "suggested_time": None}

    # fallback to LLM
    ai_response = call_huggingface_llm(user_input)
    return {"user_input": user_input, "response": ai_response, "suggested_time": None}
