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
st.subheader("Explanation detail level")
difficulty = st.slider(
    "Adjust explanation complexity",
    min_value=0,
    max_value=10,
    value=5,
    format="%d",
    help="0 = very simple, 10 = highly technical"
)

# --- Difficulty Prompts Mapping ---
explanation_styles = {
    0: "Explain this like I'm 5 years old: ",
    1: "Explain this in very simple everyday language: ",
    2: "Explain this simply, avoiding jargon: ",
    3: "Explain this for a curious high school student: ",
    4: "Explain this for a non-technical professional: ",
    5: "",  # neutral
    6: "Explain this for someone with basic technical knowledge: ",
    7: "Give a moderately technical explanation with examples: ",
    8: "Give a detailed technical explanation with terminology: ",
    9: "Give an in-depth explanation suitable for grad students: ",
    10: "Explain this thoroughly using advanced technical detail and formalism: ",
}

# --- Prompt Construction ---
if query:
    prefix = explanation_styles.get(difficulty, "")
    full_query = prefix + query

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
