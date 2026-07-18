import time
import streamlit as st
from database.database import Base, engine
from database import models

from router import show_auth
from services.ai_service import AIService
from services.chat_service import ChatService
from components.sidebar import show_sidebar
from utils.session import (
    initialize_session,
    get_current_chat_id,
)

from database.database import SessionLocal
from database import crud


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="wide"
)

# ==================================================
# CREATE DATABASE TABLES
# ==================================================

Base.metadata.create_all(bind=engine)


# ==================================================
# LOGIN CHECK
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_auth()
    st.stop()


# ==================================================
# INITIALIZE SESSION
# ==================================================

initialize_session()


# ==================================================
# SIDEBAR
# ==================================================

show_sidebar()


# ==================================================
# MAIN PAGE
# ==================================================

st.title("🤖 AI ChatBot")


chat_id = get_current_chat_id()

if chat_id is None:

    st.info("👈 Click **New Chat** to start chatting.")

    st.stop()


# ==================================================
# LOAD CHAT HISTORY
# ==================================================

messages = ChatService.load_messages(chat_id)

for message in messages:

    with st.chat_message(message.role):

        st.markdown(message.content)


# ==================================================
# USER INPUT
# ==================================================

prompt = st.chat_input("Ask anything...")


if prompt:

    # -----------------------------
    # USER MESSAGE
    # -----------------------------

    with st.chat_message("user"):

        st.markdown(prompt)

    ChatService.save_message(
        chat_id=chat_id,
        role="user",
        content=prompt
    )

    # -----------------------------
    # AUTO RENAME CHAT
    # -----------------------------

    db = SessionLocal()

    try:

        chat = crud.get_chat(
            db=db,
            chat_id=chat_id
        )

        if chat and chat.title == "New Chat":

            MAX_TITLE_LENGTH = 40

            if len(prompt) > MAX_TITLE_LENGTH:
                chat.title = (
                    prompt[:MAX_TITLE_LENGTH] + "..."
                )
            else:
                chat.title = prompt

            db.commit()

    finally:

        db.close()

    # -----------------------------
    # LOAD UPDATED HISTORY
    # -----------------------------

    history = ChatService.load_messages(chat_id)

    ai_messages = [

        {
            "role": message.role,
            "content": message.content
        }

        for message in history

    ]

    # -----------------------------
    # AI RESPONSE
    # -----------------------------

    answer = AIService.get_response(ai_messages)

    # -----------------------------
    # STREAMING EFFECT
    # -----------------------------

    with st.chat_message("assistant"):

        placeholder = st.empty()

        streamed_text = ""

        for word in answer.split():

            streamed_text += word + " "

            placeholder.markdown(
                streamed_text + "▌"
            )

            time.sleep(0.03)

        placeholder.markdown(streamed_text)

    # -----------------------------
    # SAVE AI MESSAGE
    # -----------------------------

    ChatService.save_message(
        chat_id=chat_id,
        role="assistant",
        content=answer
    )

    st.rerun()