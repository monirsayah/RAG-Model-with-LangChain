import streamlit as st
import os

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.documents import Document 


os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API KEY"



def load_documents(file_path):
    loader = TextLoader(file_path)
    return loader.load()


def chunker(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=250,
    )
    chunks = text_splitter.split_text(text)
    return chunks


def init_vector_store(chunks):
    embedding_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        collection_name="Original",
        persist_directory=None
    )
    return vector_store


def rag_pipeline(_vector_store):
    llm = ChatGroq(
        model="compound-beta-mini",
        temperature=0
    )
    top_k = 3
    retriever = _vector_store.as_retriever(search_kwargs={"k": top_k})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    return qa_chain


def query_rag_model(qa_chain, query):
    result = qa_chain.invoke({"query": query})
    return result


def main():
    @st.cache_resource
    def setup_rag_components(uploaded_files):
        if not uploaded_files:
            return None

        all_text_content = ""
        for uploaded_file in uploaded_files:
            string_data = uploaded_file.read().decode("utf-8")
            all_text_content += string_data + "\n"

        if not all_text_content.strip():
            st.error("Uploaded document(s) are empty.")
            return None

        chunks = chunker(text=all_text_content)
        vector_store = init_vector_store(chunks=chunks)
        qa_chain = rag_pipeline(_vector_store=vector_store)
        return qa_chain

    file_path = st.file_uploader("Insert Files", type=[".txt"], accept_multiple_files=True)

    if file_path:
        qa_chain_instance = setup_rag_components(file_path)
    else:
        qa_chain_instance = None
        st.info("Please upload one or more text files to begin.")


    if qa_chain_instance is None:
        st.stop()


    st.title("RAG Chatbot")

    query = st.chat_input("Ask a question about the document...")

    if query:
        with st.spinner("Thinking..."):
            result = query_rag_model(qa_chain=qa_chain_instance, query=query)
            st.write(result.get("result", "No answer found."))


if __name__ == "__main__":
    main()
