import streamlit as st
import random

st.title("💬 Smart Offline AI Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Type your message")

if st.button("Send"):

    st.session_state.history.append(f"You: {user_input}")

    user_message = user_input.lower()

    greetings = ["Hello!", "Hi!", "Hey there!"]
    jokes = ["Why did the computer laugh? It had a byte!", "Programming is fun 😄"]

    if "hello" in user_message:
        reply = random.choice(greetings)

    elif "joke" in user_message:
        reply = random.choice(jokes)

    elif "name" in user_message:
        reply = "I am your Streamlit AI chatbot."

    else:
        reply = "I understand: " + user_input

    st.session_state.history.append(f"Bot: {reply}")

for msg in st.session_state.history:
    st.write(msg)