import streamlit as st

from utils.session import new_chat


def show_sidebar():

    with st.sidebar:

        st.title("🤖 AI ChatBot")
        personality = st.selectbox(

           "🎭 AI Personality",

            [

                "Default",

                "Happy 😊",

                "Angry 😡",

                "Sad 😢",

                "Teacher 👨‍🏫",

                "Interviewer 💼"

            ]

        )

        st.session_state.personality = personality

        st.divider()

        if st.button(
            "➕ New Chat",
            use_container_width=True
        ):
            new_chat()
            st.rerun()

        st.divider()

        st.subheader("Chats")

        for chat_id, chat in st.session_state.chats.items():

            if st.button(
                chat["title"],
                key=chat_id,
                use_container_width=True
            ):
                st.session_state.current_chat = chat_id
                st.rerun()

        st.divider()

        st.subheader("Account")

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.user = None

            st.rerun()