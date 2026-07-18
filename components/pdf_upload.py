import os
import streamlit as st

from services.pdf_service import PDFService


UPLOAD_FOLDER = "uploads"


def show_pdf_upload():

    st.subheader("📄 Chat with PDF")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        file_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Processing PDF..."):

            chunks = PDFService.process_pdf(file_path)

        st.success(
            f"""
✅ PDF uploaded successfully!

📄 File : {uploaded_file.name}

📚 Chunks Created : {chunks}

🤖 Ready to answer your questions.
"""
        )