# backend/fastapi_app.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from booking_agent import planner_node

app = FastAPI()

# Allow CORS for local testing (Streamlit can talk to FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("user_input", "")
    state = {"user_input": user_input}

    result = planner_node(state)
    return result
