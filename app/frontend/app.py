

import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)


if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


st.title(" AI Travel Planner")
st.markdown(
    "Plan trips, find flights, hotels, and generate itineraries."
)


with st.sidebar:

    st.header("Session")

    st.text_input(
        "Chat ID",
        value=st.session_state.chat_id,
        disabled=True
    )

    if st.button(" New Chat"):
        st.session_state.chat_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()


for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input(
    "Where would you like to travel?"
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        response = requests.post(
            API_URL,
            params={
                "chat_id": st.session_state.chat_id,
                "message": prompt
            },
            timeout=120
        )

        data = response.json()

        bot_response = data.get(
            "response",
            "No response received."
        )

    except Exception as e:

        bot_response = f" Error: {str(e)}"

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_response
        }
    )

    with st.chat_message("assistant"):
        st.markdown(bot_response)