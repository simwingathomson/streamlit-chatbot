import streamlit as st
import requests
import time
import json
import os
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Ultimate AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------- OPENROUTER API ----------
API_KEY = "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"

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ---------- MEMORY FILE ----------
MEMORY_FILE = "chat_memory.json"

# ---------- LOAD MEMORY ----------
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as file:
        try:
            st.session_state.messages = json.load(file)
        except:
            st.session_state.messages = []
else:
    st.session_state.messages = []

# ---------- SAVE MEMORY ----------
def save_memory():
    with open(MEMORY_FILE, "w") as file:
        json.dump(st.session_state.messages, file)

# ---------- AI FUNCTION ----------
def get_ai_response(user_message):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": """
                You are a smart, friendly, professional AI assistant.
                Reply clearly and naturally.
                Support multiple languages automatically.
                """
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload
    )

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except:
        return "⚠️ AI service unavailable right now."

# ---------- SIDEBAR ----------
with st.sidebar:

    st.title("🤖 AI Chatbot")

    st.markdown("---")

    st.subheader("📜 Chat History")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        save_memory()
        st.rerun()

    st.markdown("---")

    for msg in st.session_state.messages[-10:]:

        role = "🧑 You" if msg["role"] == "user" else "🤖 Bot"

        st.write(f"{role}: {msg['content'][:40]}")

# ---------- STYLING ----------
st.markdown("""
<style>

body {
    background-color: #343541;
}

.chat-title {
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

.user-bubble {
    background-color: #19c37d;
    color: white;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 10px 0;
    text-align: right;
    font-size: 16px;
}

.bot-bubble {
    background-color: #444654;
    color: white;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 10px 0;
    text-align: left;
    font-size: 16px;
}

.stTextInput input {
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown(
    "<h1 class='chat-title'>💬 Ultimate AI Chatbot</h1>",
    unsafe_allow_html=True
)

# ---------- DISPLAY CHAT ----------
for msg in st.session_state.messages:

    if msg["role"] == "user":
        st.markdown(
            f"<div class='user-bubble'>🧑 {msg['content']}</div>",
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"<div class='bot-bubble'>🤖 {msg['content']}</div>",
            unsafe_allow_html=True
        )

# ---------- INPUT ----------
user_input = st.text_input(
    "Type your message",
    placeholder="Ask anything..."
)

# ---------- SEND BUTTON ----------
if st.button("Send") and user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": str(datetime.now())
    })

    save_memory()

    # Typing animation
    with st.spinner("🤖 AI is thinking..."):
        time.sleep(1)

        reply = get_ai_response(user_input)

    # Save AI reply
    st.session_state.messages.append({
        "role": "bot",
        "content": reply,
        "time": str(datetime.now())
    })

    save_memory()

    st.rerun()

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🚀 Powered by Streamlit + OpenRouter AI")