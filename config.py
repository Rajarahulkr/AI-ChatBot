import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv(
    "MISTRAL_API_KEY",
    st.secrets.get("MISTRAL_API_KEY", "")
)

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY",
    st.secrets.get("TAVILY_API_KEY", "")
)

MODEL = os.getenv(
    "MODEL",
    st.secrets.get("MODEL", "mistral-small-latest")
)