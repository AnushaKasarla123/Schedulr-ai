import streamlit as st
import requests

st.set_page_config(page_title="Schedulr AI", page_icon="📅")
st.title("📅 Schedulr AI Assistant")
st.caption("Ask me anything to schedule your next meeting 📆")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Type your message here...")

if user_input:
    with st.spinner("Thinking..."):
        try:
            res = requests.post("http://localhost:8000/chat", json={"user_input": user_input})
            result = res.json()
            bot_response = result["response"]
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Schedulr AI", bot_response))
        except Exception as e:
            st.session_state.chat_history.append(("Error", f"❌ Failed to connect to backend: {e}"))

for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)
