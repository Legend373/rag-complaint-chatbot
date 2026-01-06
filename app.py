import streamlit as st
import sys
import os
import time

# Add src/ to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from src.rag import RAGSystem

# -----------------------
# Page setup
# -----------------------
st.set_page_config(page_title="CrediTrust AI", layout="wide")

st.title(" CrediTrust Complaint Assistant")
st.markdown("Ask questions about real consumer complaints. Answers are backed by real evidence.")

# -----------------------
# Load RAG once
# -----------------------
@st.cache_resource
def load_rag():
    return RAGSystem()

rag = load_rag()

# -----------------------
# Session state
# -----------------------
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "sources" not in st.session_state:
    st.session_state.sources = []

# -----------------------
# Input box
# -----------------------
question = st.text_input("Enter your question:", placeholder="Why are people unhappy with credit cards?")

col1, col2 = st.columns([1,1])

with col1:
    ask_btn = st.button("🔍 Ask")

with col2:
    clear_btn = st.button("🧹 Clear")

# -----------------------
# Ask RAG
# -----------------------
if ask_btn and question.strip():
    with st.spinner("Thinking..."):
        answer, sources = rag.ask(question)

        st.session_state.answer = answer
        st.session_state.sources = sources

# -----------------------
# Clear
# -----------------------
if clear_btn:
    st.session_state.answer = ""
    st.session_state.sources = ""
    st.experimental_rerun()

# -----------------------
# Display Answer (Streaming-like)
# -----------------------
if st.session_state.answer:
    st.subheader("🧠 Answer")

    placeholder = st.empty()
    text = ""

    for token in st.session_state.answer.split():
        text += token + " "
        placeholder.markdown(text)
        time.sleep(0.03)   # streaming effect

# -----------------------
# Display Sources
# -----------------------
if st.session_state.sources:
    st.subheader("📄 Evidence Used")

    for i, s in enumerate(st.session_state.sources[:3], 1):
        with st.expander(f"Source {i} — {s['product']} (ID: {s['complaint_id']})"):
            st.write(s["text"])
