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

        # Remove extra spaces
        username = username.strip()
        email = email.strip().lower()

        # Validation
        if not username:

            st.error("Username is required.")

            return

        if not email:

            st.error("Email is required.")

            return

        if not password:

            st.error("Password is required.")

            return

        if password != confirm:

            st.error("Passwords do not match.")

            return

        success, message = AuthService.register(
            username,
            email,
            password
        )

        if success:

            st.success(message)

            st.info("Please go to the Login page and sign in.")

        else:

            st.error(message)