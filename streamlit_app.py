import streamlit as st
import requests
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Thomson AI ChatGPT Clone",
    page_icon="🤖",
    layout="centered"
)

# ================= API =================
API_KEY = st.secrets["API_KEY"]
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

# ================= CHAT HISTORY =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= CHATGPT STYLE UI =================
st.markdown("""
<style>

/* background */
[data-testid="stAppViewContainer"] {
    background-color: #0d1117;
    color: #e6edf3;
}

/* center chat width */
.block-container {
    max-width: 750px;
    padding-top: 2rem;
}

/* user bubble */
.user-bubble {
    background: #1f6feb;
    color: white;
    padding: 12px 15px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
}

/* assistant bubble */
.bot-bubble {
    background: #161b22;
    color: #e6edf3;
    padding: 12px 15px;
    border-radius: 15px;
    margin: 8px 0;
    border: 1px solid #30363d;
}

/* input box */
input {
    background-color: #161b22 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("⚙️ Controls")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.write("🤖 Thomson AI ChatGPT Clone")
    st.write("✔ Streaming UI")
    st.write("✔ Memory enabled")

# ================= TITLE =================
st.title("🤖 Thomson AI ChatGPT")

st.caption("A ChatGPT-style AI assistant built with Streamlit")

# ================= FUNCTION =================
def get_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.messages,
            {"role": "user", "content": prompt}
        ]
    }

    try:
        r = requests.post(API_URL, headers=headers, json=payload)
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except:
        return "⚠️ Error: API failed or no response."

# ================= DISPLAY CHAT =================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# ================= INPUT =================
user_input = st.chat_input("Message Thomson AI...")

if user_input:

    # show user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    st.markdown(f"<div class='user-bubble'>🧑 {user_input}</div>", unsafe_allow_html=True)

    # placeholder for streaming effect
    placeholder = st.empty()

    reply = get_response(user_input)

    # ================= STREAMING EFFECT =================
    streamed_text = ""
    for char in reply:
        streamed_text += char
        placeholder.markdown(f"<div class='bot-bubble'>🤖 {streamed_text}</div>", unsafe_allow_html=True)
        time.sleep(0.01)

    # save final message
    st.session_state.messages.append({"role": "assistant", "content": reply})