import streamlit as st


def show_settings():

    st.subheader("⚙️ Settings")

    if "use_pdf" not in st.session_state:
        st.session_state.use_pdf = True

    if "use_web" not in st.session_state:
        st.session_state.use_web = False

    if "stream_response" not in st.session_state:
        st.session_state.stream_response = True

    st.session_state.use_pdf = st.toggle(
        "📄 Use Uploaded PDFs",
        value=st.session_state.use_pdf
    )

    st.session_state.use_web = st.toggle(
        "🌐 Enable Web Search",
        value=st.session_state.use_web
    )

    st.session_state.stream_response = st.toggle(
        "⚡ Stream Responses",
        value=st.session_state.stream_response
    )