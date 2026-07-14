import streamlit as st
from ai.service import generate_response

st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI ChatBot")

# ----------------------------------
# Initialize Chat History
# ----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------
# Display Previous Messages
# ----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------------
# User Input
# ----------------------------------

prompt = st.chat_input("Ask anything...")

if prompt:

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Generate AI Response
    answer = generate_response(prompt)

    # Display AI Response
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Save AI Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )