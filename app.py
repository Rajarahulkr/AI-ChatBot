import streamlit as st

from router import show_auth

from services.ai_service import AIService

from services.chat_service import ChatService

from ai.service import generate_response

from components.sidebar import show_sidebar

from utils.session import (
    initialize_session,
    get_current_chat
)

st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="wide"
)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    show_auth()

    st.stop()

initialize_session()

show_sidebar()

chat = get_current_chat()

st.title("🤖 AI ChatBot")

for message in chat["messages"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask anything...")

if prompt:

    ChatService.add_user_message(prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    answer = AIService.get_response(chat["messages"])

    with st.chat_message("assistant"):
        st.markdown(answer)

    ChatService.add_ai_message(answer)

    if chat["title"] == "New Chat":

        chat["title"] = prompt[:30]

    st.rerun()