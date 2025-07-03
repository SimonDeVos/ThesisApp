'''import streamlit as st
from src.rag import answer_question

st.set_page_config(page_title="Thesis & Resume Chat", page_icon="🎓")

st.title("🎓 Ask me about my Thesis or Resume")

query = st.text_input("Type your question and press Enter:")

if query:
    with st.spinner("Fetching answer..."):
        answer = answer_question(query)
    st.markdown("**Answer:**")
    st.write(answer)'''

import streamlit as st
import requests
from src.rag import answer_question

# --- Streamlit Page Config ---
st.set_page_config(page_title="Simon's Thesis & Resume Chat", page_icon="🎓")
st.title("🎓 Ask me about my thesis or resume")

# --- Example Questions ---
st.subheader("📌 Example questions")
example_questions = [
    "Why should I hire Simon as senior data scientist?",
    "Provide me with the structure of the thesis."
    "What are the benefits of using continuous treatments?",
    "Explain cost-sensitive learning.",
    "What did Simon study?",
]

selected_example = st.selectbox("Try one of these:", [""] + example_questions)

# --- Query Input ---
query = st.text_input("Or type your own question below:", value=selected_example if selected_example else "")

# --- Query Handling ---
if query:
    with st.spinner("Fetching answer..."):
        answer = answer_question(query)
    st.markdown("**Answer:**")
    st.write(answer)

    FORMSPREE_URL = st.secrets["formspree_url"]

    try:
        r = requests.post(
            FORMSPREE_URL,
            data={"query": query},
            timeout=5
        )
        if r.status_code != 200:
            st.warning("⚠️ Could not log query (email service error).")
    except Exception as e:
        st.warning("⚠️ Could not log query (network error).")



