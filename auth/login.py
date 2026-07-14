import streamlit as st

from auth.auth_service import AuthService


def login_page():

    st.title("🤖 Nova AI")

    st.subheader("Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        success, user = AuthService.login(
            email,
            password
        )

        if success:

            st.session_state.logged_in = True
            st.session_state.user = user

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid Email or Password")