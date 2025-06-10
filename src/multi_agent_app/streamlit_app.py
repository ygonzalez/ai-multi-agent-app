import streamlit as st
import requests
import uuid
from multi_agent_app.settings import settings


if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

BACKEND = settings.backend_url

st.set_page_config(page_title="Multi-Agent Demo", layout="wide")
st.title("🎧  Multi-Agent Customer Support")

if "history" not in st.session_state:
    st.session_state.history = []

prompt = st.chat_input("Ask me something…")
if prompt:
    st.session_state.history.append(("user", prompt))

    with st.spinner("Thinking…"):
        try:
            r = requests.post(
                f"{BACKEND}/chat",
                json={
                    "message": prompt,
                    "thread_id": st.session_state.thread_id
                },
                timeout=30,
            )
            r.raise_for_status()
            answer = r.json()["response"]
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            answer = None
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with backend: {e}")
            answer = None

    if answer:
        st.session_state.history.append(("bot", answer))

for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)
