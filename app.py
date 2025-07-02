import streamlit as st
from src.rag import answer_question

st.set_page_config(page_title="Thesis & Resume Chat", page_icon="🎓")

st.title("🎓 Ask me about my Thesis or Resume")

query = st.text_input("Type your question and press Enter:")

if query:
    with st.spinner("Fetching answer..."):
        answer = answer_question(query)
    st.markdown("**Answer:**")
    st.write(answer)
