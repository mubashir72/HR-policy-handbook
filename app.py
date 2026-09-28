"""Streamlit entry point for the HR Policy Assistant."""

from __future__ import annotations

import hashlib

import streamlit as st

from src.answering import answer_question, user_facing_groq_error
from src.chunking import chunk_pages
from src.config import RETRIEVAL_TOP_K, load_config
from src.pdf_processing import PdfProcessingError, extract_pdf_pages, validate_pdf_upload
from src.retrieval import EMBEDDING_MODEL, PolicyIndex

st.set_page_config(
    page_title="HR Policy Assistant",
    page_icon=":material/menu_book:",
    layout="wide",
    initial_sidebar_state="expanded",
)

SUGGESTIONS = {
    "How much annual leave do I receive?": "How much annual leave do I receive, and how much can I carry over?",
    "What should I do if I am sick?": "What should I do if I need to take sick leave?",
    "Can I work remotely?": "What are the requirements for flexible or remote work?",
}


@st.cache_resource(show_spinner=False)
def get_embedding_model():
    """Load the shared embedding model once per server process."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL)


def initialize_state() -> None:
    defaults = {
        "document_hash": None,
        "document_name": None,
        "page_count": 0,
        "passage_count": 0,
        "policy_index": None,
        "messages": [],
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def reset_document() -> None:
    for key, default in {
        "document_hash": None,
        "document_name": None,
        "page_count": 0,
        "passage_count": 0,
        "policy_index": None,
        "messages": [],
    }.items():
        st.session_state[key] = default
    st.session_state.suggested_question = None


def clear_conversation() -> None:
    st.session_state.messages = []
    st.session_state.suggested_question = None
    st.toast("Conversation cleared", icon=":material/delete_sweep:")


def index_upload(uploaded_file) -> None:
    content = uploaded_file.getvalue()
    file_hash = hashlib.sha256(content).hexdigest()
    if file_hash == st.session_state.document_hash:
        return

    with st.status("Preparing your policy", expanded=True) as status:
        try:
            validate_pdf_upload(uploaded_file.name, content)
            pages = extract_pdf_pages(content)
            st.write(f"Read text from {len(pages)} pages.")
            chunks = chunk_pages(pages, uploaded_file.name)
            st.write(f"Prepared {len(chunks)} searchable passages.")
            st.write("Creating a local search index…")
            index = PolicyIndex.build(chunks, get_embedding_model())
        except PdfProcessingError as error:
            reset_document()
            status.update(label="Could not use this PDF", state="error")
            st.error(str(error), icon=":material/error:")
            return
        except Exception:
            reset_document()
            status.update(label="Indexing failed", state="error")
            st.error(
                "The policy could not be indexed. Please try another text-based PDF.",
                icon=":material/error:",
            )
            return

        st.session_state.document_hash = file_hash
        st.session_state.document_name = uploaded_file.name
        st.session_state.page_count = len(pages)
        st.session_state.passage_count = len(chunks)
        st.session_state.policy_index = index
        st.session_state.messages = []
        status.update(label="Policy ready", state="complete")
        st.toast("Your policy is ready for questions", icon=":material/check_circle:")


def show_sources(results) -> None:
    with st.expander("Source excerpts", icon=":material/article:"):
        for result in results:
            st.markdown(f"**Page {result.chunk.page_number}**")
            st.caption(result.chunk.text)


def answer_from_question(question: str, config) -> None:
    """Render and record one complete answer exchange."""
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant", avatar=":material/auto_awesome:"):
        with st.status(":shimmer[Finding policy evidence]", type="compact") as status:
            results = st.session_state.policy_index.search(
                question, get_embedding_model(), RETRIEVAL_TOP_K
            )
            st.write(f"Found {len(results)} relevant passages.")
            status.update(label="Evidence ready", state="complete")
        if not config.groq_api_key:
            answer = "A Groq API key is required to generate an answer. Set `GROQ_API_KEY` and try again."
        else:
            try:
                with st.spinner("Writing an answer…"):
                    answer = answer_question(question, results, config.groq_api_key, config.groq_model)
            except Exception as error:
                answer = user_facing_groq_error(error)
        st.markdown(answer)
        show_sources(results)
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": results})


initialize_state()
config = load_config(st.secrets)

with st.sidebar:
    st.title("HR Policy Assistant", icon=":material/menu_book:")
    st.caption("Answers grounded in your uploaded policy.")
    st.space("small")

    if st.session_state.policy_index is None:
        st.badge("No policy uploaded", icon=":material/upload_file:", color="gray")
    else:
        st.badge("Policy ready", icon=":material/check_circle:", color="green")
        st.caption(st.session_state.document_name)
        if st.button("Clear conversation", icon=":material/delete_sweep:", width="stretch"):
            clear_conversation()

    with st.expander("How it works", icon=":material/help:"):
        st.markdown(
            "1. Upload one text-based HR policy PDF.\n\n"
            "2. Ask a plain-language question.\n\n"
            "3. Check the source excerpts and page references."
        )
    with st.expander("Privacy and limits", icon=":material/shield:"):
        st.caption(
            "The policy index and conversation stay in this browser session. "
            "Scanned PDFs without selectable text need OCR before they can be searched."
        )

st.title("Find answers in your HR policy", icon=":material/forum:")
st.caption("Upload a policy once, then ask questions in everyday language. Each answer includes the PDF evidence used.")

uploaded_file = st.file_uploader(
    "Upload an HR policy PDF",
    type=["pdf"],
    help="One text-based PDF, up to 20 MB. Uploading a new policy starts a new session.",
)

if uploaded_file is None:
    if st.session_state.document_hash is not None:
        reset_document()
    with st.container(border=True):
        st.subheader("Start with your policy", icon=":material/upload_file:")
        st.write("Choose a text-based PDF above. Once it is ready, you can ask questions about leave, attendance, benefits, remote work, and more.")
        st.caption("Tip: scanned or image-only PDFs need OCR before they can be searched.")
else:
    index_upload(uploaded_file)

if st.session_state.policy_index is not None:
    with st.container(border=True):
        details, pages, passages = st.columns([2.2, 1, 1], vertical_alignment="center")
        with details:
            st.subheader("Current policy", icon=":material/description:")
            st.write(st.session_state.document_name)
            st.badge("Ready for questions", icon=":material/check_circle:", color="green")
        with pages:
            st.metric("Text pages", st.session_state.page_count)
        with passages:
            st.metric("Search passages", st.session_state.passage_count)

    st.space("small")
    st.subheader("Ask about this policy", icon=":material/chat:")

    for message in st.session_state.messages:
        avatar = ":material/auto_awesome:" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            if message.get("sources"):
                show_sources(message["sources"])

    selected_question = None
    if not st.session_state.messages:
        st.caption("Try one of these common questions:")
        selected_question = st.pills(
            "Suggested questions",
            list(SUGGESTIONS),
            label_visibility="collapsed",
            key="suggested_question",
        )

    typed_question = st.chat_input("Ask a question about this policy", submit_mode="disable")
    question = typed_question or (SUGGESTIONS.get(selected_question) if selected_question else None)
    if question:
        answer_from_question(question, config)
