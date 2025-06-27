import streamlit as st
from backend.booking_agent import planner_node

# Page config
st.set_page_config(page_title="📅 Schedulr AI", page_icon="📆")
st.title("📅 Schedulr AI Assistant")
st.caption("Ask me anything to schedule your next meeting 📆")

# Chat history state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    with st.spinner("Thinking..."):
        # Call your booking logic
        state = {"user_input": user_input, "suggested_time": None}
        result = planner_node(state)
        response = result["response"]

        # Store messages
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Schedulr", response))

# Display full conversation
for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)
