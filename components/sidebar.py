import streamlit as st

from components.pdf_upload import show_pdf_upload
from components.pdf_manager import show_pdf_manager
from components.settings import show_settings

from database.database import SessionLocal
from database import crud

from utils.session import (
    new_chat,
    load_chat,
)


def show_sidebar():

    with st.sidebar:

        st.title("🤖 AI ChatBot")

        # ---------------- Personality ---------------- #

        personality = st.selectbox(
            "🎭 AI Personality",
            [
                "Default",
                "Happy 😊",
                "Angry 😡",
                "Sad 😢",
                "Teacher 👨‍🏫",
                "Interviewer 💼",
            ],
            index=[
                "Default",
                "Happy 😊",
                "Angry 😡",
                "Sad 😢",
                "Teacher 👨‍🏫",
                "Interviewer 💼",
            ].index(
                st.session_state.get(
                    "personality",
                    "Default",
                )
            ),
        )

        st.session_state.personality = personality

        st.divider()

        # ---------------- New Chat ---------------- #

        if st.button(
            "➕ New Chat",
            use_container_width=True,
        ):
            new_chat()
            st.rerun()

        st.divider()

        # ---------------- Chat History ---------------- #

        st.subheader("💬 Chats")

        db = SessionLocal()

        try:

            chats = crud.get_user_chats(
                db=db,
                user_id=st.session_state.user.id,
            )

            if chats:

                for chat in chats:

                    col1, col2, col3 = st.columns([4, 1, 1])

                    # Open Chat
                    with col1:

                        if st.button(
                            chat.title,
                            key=f"chat_{chat.id}",
                            use_container_width=True,
                        ):
                            load_chat(chat.id)
                            st.rerun()

                    # Rename Chat
                    with col2:

                        if st.button(
                            "✏️",
                            key=f"rename_{chat.id}",
                        ):
                            st.session_state.rename_chat = chat.id

                    # Delete Chat
                    with col3:

                        if st.button(
                            "🗑️",
                            key=f"delete_{chat.id}",
                        ):

                            crud.delete_chat(
                                db=db,
                                chat_id=chat.id,
                            )

                            if (
                                st.session_state.current_chat_id
                                == chat.id
                            ):

                                remaining = crud.get_user_chats(
                                    db=db,
                                    user_id=st.session_state.user.id,
                                )

                                if remaining:
                                    st.session_state.current_chat_id = (
                                        remaining[0].id
                                    )
                                else:
                                    st.session_state.current_chat_id = None

                            st.rerun()

                    # Rename Input
                    if st.session_state.get("rename_chat") == chat.id:

                        new_title = st.text_input(
                            "Rename Chat",
                            value=chat.title,
                            key=f"title_{chat.id}",
                        )

                        col_save, col_cancel = st.columns(2)

                        with col_save:

                            if st.button(
                                "💾 Save",
                                key=f"save_{chat.id}",
                                use_container_width=True,
                            ):

                                crud.rename_chat(
                                    db=db,
                                    chat_id=chat.id,
                                    new_title=new_title.strip(),
                                )

                                st.session_state.pop(
                                    "rename_chat",
                                    None,
                                )

                                st.rerun()

                        with col_cancel:

                            if st.button(
                                "❌ Cancel",
                                key=f"cancel_{chat.id}",
                                use_container_width=True,
                            ):

                                st.session_state.pop(
                                    "rename_chat",
                                    None,
                                )

                                st.rerun()

            else:

                st.caption("No chats yet.")

        finally:

            db.close()

        # ---------------- PDF Upload ---------------- #

        st.divider()

        show_pdf_upload()

        # ---------------- PDF Manager ---------------- #

        st.divider()

        show_pdf_manager()

        # ---------------- Settings ---------------- #

        st.divider()

        show_settings()

        # ---------------- Account ---------------- #

        st.divider()

        st.subheader("👤 Account")

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):

            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.current_chat_id = None

            st.session_state.pop(
                "rename_chat",
                None,
            )

            st.rerun()