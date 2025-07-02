import streamlit as st
from src.rag import answer_question

st.set_page_config(page_title="Thesis & Resume Chat", page_icon="🎓", layout="wide")

# Sidebar info
with st.sidebar:
    st.title("🎓 Thesis & Resume Chat")
    st.markdown(
        """
        Ask me anything about my PhD thesis or resume.
        - Powered by RAG + OpenAI GPT
        - Uses FAISS for fast retrieval
        """
    )
    st.markdown("---")
    st.markdown("Made by You 🚀")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input box
def get_text():
    return st.text_input("Your question:", key="input", placeholder="Type your question here and hit Enter")

query = get_text()

if query:
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": query})

    # Get answer from rag.py
    with st.spinner("Thinking..."):
        answer = answer_question(query)
    st.session_state.history.append({"role": "assistant", "content": answer})

# Display chat messages
for msg in st.session_state.history[::-1]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Answer:** {msg['content']}")
    st.markdown("---")
