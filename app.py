

import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from html_templates import css, USER_TEMPLATE, BOT_TEMPLATE




def get_pdf_text(pdf_docs) -> str:
    """Extract text from a list of uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text




def get_text_chunks(raw_text: str):
    """Split raw text into overlapping chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return splitter.split_text(raw_text)




def get_vectorstore(text_chunks):
    """Embed text chunks and store them in a FAISS index."""
    provider = detect_provider()

    if provider == "gemini":
        embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore




def get_conversation_chain(vectorstore):
    """Build a ConversationalRetrievalChain backed by the vectorstore."""
    provider = detect_provider()

    if provider == "gemini":
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3,
            convert_system_message_to_human=True,
        )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        memory=memory,
        return_source_documents=True,
    )
    return chain


def handle_userinput(user_question: str):
    if st.session_state.conversation is None:
        st.warning(" Please upload and process a PDF first!")
        return

    with st.spinner("Thinking..."):
        response = st.session_state.conversation({"question": user_question})

    st.session_state.chat_history = response["chat_history"]

    # Render chat history
    chat_html = '<div class="chat-container">'
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:  # human
            chat_html += USER_TEMPLATE.replace("{{MSG}}", message.content)
        else:            # AI
            chat_html += BOT_TEMPLATE.replace("{{MSG}}", message.content)
    chat_html += "</div>"

    st.write(chat_html, unsafe_allow_html=True)

    # Show source chunks in an expander
    if "source_documents" in response and response["source_documents"]:
        with st.expander(" Source excerpts used to answer"):
            for i, doc in enumerate(response["source_documents"], 1):
                st.markdown(
                    f'<div class="source-box"><b>Excerpt {i}:</b><br>{doc.page_content[:400]}…</div>',
                    unsafe_allow_html=True,
                )


def detect_provider() -> str:
    if os.getenv("GOOGLE_API_KEY"):
        return "gemini"
    return "none"  # no valid key found



def main():
    load_dotenv()

    st.set_page_config(
        page_title="Chat with PDF",
        page_icon="",
        layout="wide",
    )
    st.write(css, unsafe_allow_html=True)

    # ── session state init ──
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # ── check keys ──
    provider = detect_provider()
    if provider == "none":
        st.error(
            " No API key found. Copy `.env.example` → `.env` and add your key.",
            icon="",
        )
        st.stop()

    # ── header ──
    st.markdown(
        "<h1 style='text-align:center'>📚 Chat with your PDF</h1>",
        unsafe_allow_html=True,
    )

    # ── chat input ──
    user_question = st.text_input(
        " Ask a question about your documents",
        placeholder="e.g. Summarise the key findings …",
    )
    if user_question:
        handle_userinput(user_question)

    # ── sidebar ──
    with st.sidebar:
        st.markdown("## 📂 Your Documents")
        pdf_docs = st.file_uploader(
            "",
            type="pdf",
            accept_multiple_files=True,
        )

        if st.button("Process", use_container_width=True):
            if not pdf_docs:
                st.warning("Please upload at least one PDF first.")
            else:
                with st.spinner("Processing your PDFs …"):
                    # Step 1 – extract text
                    raw_text = get_pdf_text(pdf_docs)
                    if not raw_text.strip():
                        st.error("Could not extract text from the PDFs. Are they scanned images?")
                        st.stop()

                    # Step 2 – chunk
                    text_chunks = get_text_chunks(raw_text)
                    st.info(f" {len(text_chunks)} text chunks created")

                    # Step 3 – embed & store
                    vectorstore = get_vectorstore(text_chunks)

                    # Step 4 – conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.session_state.chat_history = None  # reset history on new upload

                st.success("Ready! Ask your questions above.")

        st.markdown("---")
        st.markdown(
            """
            
            """
        )

        if st.session_state.conversation:
            if st.button("🗑️ Clear conversation", use_container_width=True):
                st.session_state.conversation = None
                st.session_state.chat_history = None
                st.rerun()


if __name__ == "__main__":
    main()
