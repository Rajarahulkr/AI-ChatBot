import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


UPLOAD_FOLDER = "uploads"
VECTOR_FOLDER = "vectorstore"


class PDFService:

    @staticmethod
    def get_embeddings():
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    @staticmethod
    def process_pdf(file_path):

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(VECTOR_FOLDER, exist_ok=True)

        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(documents)

        pdf_name = os.path.splitext(os.path.basename(file_path))[0]

        for chunk in chunks:
            chunk.metadata["document"] = pdf_name

        embeddings = PDFService.get_embeddings()

        db = FAISS.from_documents(
            chunks,
            embeddings
        )

        db.save_local(
            os.path.join(VECTOR_FOLDER, pdf_name)
        )

        return len(chunks)

    @staticmethod
    def get_context(query, k=4):

        embeddings = PDFService.get_embeddings()

        all_docs = []

        if not os.path.exists(VECTOR_FOLDER):
            return "", []

        for folder in os.listdir(VECTOR_FOLDER):

            index_path = os.path.join(
                VECTOR_FOLDER,
                folder
            )

            if not os.path.isdir(index_path):
                continue

            db = FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True
            )

            docs = db.similarity_search(
                query,
                k=k
            )

            all_docs.extend(docs)

        all_docs = sorted(
            all_docs,
            key=lambda x: x.metadata.get("score", 0)
        )[:k]

        context = ""

        sources = []

        for doc in all_docs:

            context += doc.page_content + "\n\n"

            sources.append(
                {
                    "document": doc.metadata.get("document", "Unknown"),
                    "page": doc.metadata.get("page", 0) + 1
                }
            )

        return context.strip(), sources