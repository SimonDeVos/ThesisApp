import streamlit as st
import requests
from src.rag import answer_question

# --- Streamlit Page Config ---
st.set_page_config(page_title="Simon's Thesis & Resume Chat", page_icon="🎓")
st.title("Ask anything about Simon's thesis or resume")

# --- Example Questions ---
st.subheader("Example questions")
example_questions = [
    "Why hire Simon as a Senior Data Scientist?",
    "What’s the thesis structure?",
    "Why use continuous treatments?",
    "What is cost-sensitive learning?",
    "What’s Simon’s educational background?",
    "What is decision-centric fairness?",
]

# --- Handle example question buttons ---
clicked_question = None
cols = st.columns(2)
for i, question in enumerate(example_questions):
    if cols[i % 2].button(question):
        clicked_question = question

# --- Query Input ---
default_value = clicked_question if clicked_question else ""

st.subheader("Or type your own question below:")
query = st.text_input("", value=default_value)

# --- Explanation Level Slider ---
st.subheader("Explanation technicality")
difficulty = st.slider(
    "Adjust the technical depth of the answer",
    min_value=1,
    max_value=3,
    value=2,
    format="%d",
    help="Slide left for simpler explanations, right for more technical detail.",
)

# --- Prompt Tuning ---
if query:
    if difficulty == 1:
        instruction = "Explain this as simply as possible: "
    elif difficulty == 3:
        instruction = "Provide a detailed and technical explanation: "
    else:
        instruction = ""

    full_query = instruction + query

    with st.spinner("Fetching answer..."):
        answer = answer_question(full_query)
    st.markdown("**Answer:**")
    st.write(answer)

    # --- Send query to your email via Formspree ---
    FORMSPREE_URL = st.secrets["formspree_url"]

    try:
        r = requests.post(
            FORMSPREE_URL,
            data={"query": full_query},
            timeout=5
        )
        if r.status_code != 200:
            st.warning("⚠️ Could not log query (email service error).")
    except Exception as e:
        st.warning("⚠️ Could not log query (network error).")
