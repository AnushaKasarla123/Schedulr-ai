# backend/langgraph_bot.py

from calendar_utils import create_event
from datetime import datetime, timedelta
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = PromptTemplate(
    input_variables=["message"],
    template="""
You are a calendar assistant. Extract the event details from the user's message and return:
- Title
- Start datetime in format YYYY-MM-DDTHH:MM:SS
- End datetime in format YYYY-MM-DDTHH:MM:SS

Message: {message}
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

def handle_message(message):
    result = chain.run(message)
    print("AI Response:\n", result)

    try:
        lines = result.strip().split("\n")
        title = lines[0].split(":")[1].strip()
        start = lines[1].split(":")[1].strip()
        end = lines[2].split(":")[1].strip()

        event_link = create_event(title, start, end)
        return f"✅ Event booked: {event_link}"
    except Exception as e:
        return f"❌ Failed to create event: {str(e)}"
