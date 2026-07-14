import streamlit as st

from auth.auth_service import AuthService


def register_page():

    st.title("🤖 Nova AI")

    st.subheader("Register")

    username = st.text_input("Username")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button(
        "Register",
        use_container_width=True
    ):

        if password != confirm:

            st.error("Passwords do not match")

            return

        success, message = AuthService.register(
            username,
            email,
            password
        )

        if success:

            st.success(message)

        else:

            st.error(message)