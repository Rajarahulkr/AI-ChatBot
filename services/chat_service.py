import streamlit as st

from database.database import SessionLocal
from database import crud


class ChatService:

    @staticmethod
    def get_current_chat():
        return st.session_state.chats[
            st.session_state.current_chat
        ]

    @staticmethod
    def add_user_message(message):

        chat = ChatService.get_current_chat()

        chat["messages"].append(
            {
                "role": "user",
                "content": message
            }
        )

    @staticmethod
    def add_ai_message(message):

        chat = ChatService.get_current_chat()

        chat["messages"].append(
            {
                "role": "assistant",
                "content": message
            }
        )

    # -------------------------
    # DATABASE FUNCTIONS
    # -------------------------

    @staticmethod
    def create_chat(user_id, title="New Chat"):

        db = SessionLocal()

        chat = crud.create_chat(
            db=db,
            user_id=user_id,
            title=title
        )

        db.close()

        return chat

    @staticmethod
    def save_message(chat_id, role, content):

        db = SessionLocal()

        crud.save_message(
            db=db,
            chat_id=chat_id,
            role=role,
            content=content
        )

        db.close()

    @staticmethod
    def load_messages(chat_id):

        db = SessionLocal()

        messages = crud.get_chat_messages(
            db=db,
            chat_id=chat_id
        )

        db.close()

        return messages

    @staticmethod
    def delete_chat(chat_id):

        db = SessionLocal()

        crud.delete_chat(
            db=db,
            chat_id=chat_id
        )

        db.close()