import streamlit as st

from services.chat_service import ChatService


def initialize_session():

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None


def new_chat():

    user = st.session_state.user

    chat = ChatService.create_chat(
        user.id,
        "New Chat"
    )

    st.session_state.current_chat_id = chat.id

    return chat


def load_chat(chat_id):

    st.session_state.current_chat_id = chat_id


def get_current_chat_id():

    return st.session_state.current_chat_id