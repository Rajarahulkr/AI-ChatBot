import os
import shutil
import streamlit as st

from services.pdf_service import UPLOAD_FOLDER, VECTOR_FOLDER


def show_pdf_manager():

    st.subheader("📚 Uploaded PDFs")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(VECTOR_FOLDER, exist_ok=True)

    pdfs = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if f.lower().endswith(".pdf")
    ]

    if not pdfs:
        st.info("No PDF uploaded.")
        return

    st.caption(f"{len(pdfs)} PDF(s) available")

    for pdf in pdfs:

        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(f"📄 {pdf}")

        with col2:

            if st.button(
                "🗑️",
                key=f"delete_pdf_{pdf}"
            ):

                pdf_path = os.path.join(
                    UPLOAD_FOLDER,
                    pdf
                )

                if os.path.exists(pdf_path):
                    os.remove(pdf_path)

                vector_path = os.path.join(
                    VECTOR_FOLDER,
                    os.path.splitext(pdf)[0]
                )

                if os.path.exists(vector_path):
                    shutil.rmtree(vector_path)

                st.success(f"{pdf} deleted.")

                st.rerun()