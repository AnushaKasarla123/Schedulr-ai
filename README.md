# 🤖 Schedulr AI Assistant

Schedulr AI is a conversational scheduling assistant built using **Streamlit + FastAPI + Google Calendar API + Hugging Face Mixtral LLM**. It helps users **schedule meetings using natural language**, check calendar availability, suggest alternate time slots, confirm bookings, and now also **cancel events**.

---

## ✅ Features Implemented

| Feature                     | Status | Description                                             |
| --------------------------- | ------ | ------------------------------------------------------- |
| Natural language input      | ✅      | Accepts input like "Schedule a meeting tomorrow at 3pm" |
| Date & time parsing         | ✅      | Parses vague time expressions using `dateparser`        |
| Google Calendar Integration | ✅      | Creates events and returns calendar links               |
| Conflict detection          | ✅      | Checks if time is already booked using `list_events()`  |
| Suggest alternate time      | ✅      | Proposes next available 1-hour slot if conflict found   |
| Multi-turn support          | ✅      | Remembers suggested slot; books it if user says "Yes"   |
| Cancel event by time        | ✅      | Deletes scheduled event if user requests cancellation   |
| Backend API                 | ✅      | Powered by FastAPI at `http://localhost:8000/chat`      |
| Frontend UI                 | ✅      | Streamlit chatbot interface with message history        |

---

## 📁 Project Structure

```
schedulr-ai/
├── backend/
│   ├── booking_agent.py         # Core LLM + calendar logic
│   ├── calendar_utils.py        # Google Calendar integration
│   ├── fastapi_app.py           # FastAPI backend server
│   ├── .env                     # Contains API keys
│
├── frontend/
│   ├── chatbot_ui.py            # Streamlit chatbot UI
│
├── credentials.json             # Google OAuth credentials
├── token.json                   # Google Calendar access token
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start FastAPI Backend

```bash
cd backend
uvicorn fastapi_app:app --reload
```

### 3. Start Streamlit Frontend

```bash
cd ../frontend
streamlit run chatbot_ui.py
```

---

## 🧪 Sample Prompts to Test

* `Schedule a meeting tomorrow at 4pm`
* `Can I get a slot on July 3rd between 2 and 3pm?`
* `Book a call next Friday at 11am`
* `Yes` *(after a suggested time)*
* `Cancel my meeting tomorrow at 4pm`
* `Delete event on July 3rd at 2pm`
* `Schedule a meeting at 3pm tomorrow` *(and reply Yes if bot suggests a time)*
* `Book a slot next Tuesday at 1pm` *(check for availability + alternate suggestion)*

---

## 👩‍💻 Built by

**Anusha Kasarla**
B.Tech CSE  |  Schedulr AI Project 2025
