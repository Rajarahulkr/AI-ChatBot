import streamlit as st

from auth.login import login_page
from auth.register import register_page


def show_auth():

    if "page" not in st.session_state:

        st.session_state.page = "login"

    if st.session_state.page == "login":

        login_page()

        st.write("Don't have an account?")

        if st.button("Register Here"):

            st.session_state.page = "register"

            st.rerun()

    else:

        register_page()

        st.write("Already have an account?")

        if st.button("Back to Login"):

            st.session_state.page = "login"

            st.rerun()