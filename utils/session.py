import streamlit as st
import uuid


def initialize_session():

    if "chats" not in st.session_state:

        first_chat = str(uuid.uuid4())

        st.session_state.chats = {
            first_chat: {
                "title": "New Chat",
                "messages": []
            }
        }

        st.session_state.current_chat = first_chat


def get_current_chat():

    return st.session_state.chats[
        st.session_state.current_chat
    ]


def new_chat():

    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.current_chat = chat_id


def delete_chat(chat_id):

    del st.session_state.chats[chat_id]

    if len(st.session_state.chats) == 0:
        new_chat()

    st.session_state.current_chat = list(
        st.session_state.chats.keys()
    )[0]