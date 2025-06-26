import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.title("📅 Booking Bot")

if 'history' not in st.session_state:
    st.session_state.history = []

def send(msg):
    try:
        resp = requests.post(API_URL, json={"user": "default", "message": msg})
        resp.raise_for_status()  # This will raise an HTTPError for bad responses
        data = resp.json()
        print("Response:", data)
        return data
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
        print("Server response:", resp.text)
    except requests.exceptions.JSONDecodeError as e:
        print("Invalid JSON:", e)
        print("Raw response:", resp.text)

for speaker, text in st.session_state.history:
    st.markdown(f"**{speaker}:** {text}")

user_input = st.text_input("Type a message")
if st.button("Send"):
    send(user_input)
