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
    "Provide me with the structure of the thesis.",
    "What are the benefits of using continuous treatments?",
    "Explain cost-sensitive learning.",
    "What did Simon study?",
]

# --- Handle example question buttons ---
clicked_question = None
cols = st.columns(2)
for i, question in enumerate(example_questions):
    if cols[i % 2].button(question):
        clicked_question = question

# --- Query Input ---
default_value = clicked_question if clicked_question else ""
query = st.text_input("Or type your own question below:", value=default_value)

# --- Query Handling ---
if query:
    with st.spinner("Fetching answer..."):
        answer = answer_question(query)
    st.markdown("**Answer:**")
    st.write(answer)

    # --- Send query to your email via Formspree ---
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


