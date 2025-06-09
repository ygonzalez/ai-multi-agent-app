import streamlit as st
import requests, os
import uuid

if "thread_id" not in st.session_state:
    # one ID per browser tab = keeps context & memory
    st.session_state.thread_id = str(uuid.uuid4())

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")


st.set_page_config(page_title="Multi-Agent Demo", layout="wide")
st.title("🎧  Multi-Agent Customer Support")

if "history" not in st.session_state:
    st.session_state.history = []

prompt = st.chat_input("Ask me something…")
if prompt:
    # optimistic UI
    st.session_state.history.append(("user", prompt))

    r = requests.post(
        f"{BACKEND}/chat",
        json={
            "message": prompt,
            "thread_id": st.session_state.thread_id  # NEW
        },
        timeout=30,
    )
    answer = r.json()["response"]
    st.session_state.history.append(("bot", answer))

for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)
