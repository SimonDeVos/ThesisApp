import streamlit as st
import requests
from src.rag import answer_question

# --- Streamlit Page Config ---
st.set_page_config(page_title="Simon's Thesis & Resume Chat", page_icon="🎓")
st.title("🎓 Ask anything about Simon's thesis or resume")

# --- Initialize session history ---
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

# --- Example Questions ---
st.subheader("💡 Example questions")
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

# --- Persona toggle ---
st.subheader("🧑‍🔬 Answering style")
persona = st.radio(
    "How should Simon answer?",
    ["As a serious PhD researcher", "As a sleep-deprived researcher running on caffeine"],
    horizontal=True
)

# --- Query Input ---
default_value = clicked_question if clicked_question else ""
st.subheader("💬 Or type your own question below:")
query = st.text_input("", value=default_value)

# --- Custom persona prompt ---
def apply_persona(persona_choice, base_query):
    if "sleep-deprived" in persona_choice:
        return f"Answer as if you're a sleep-deprived PhD student. Be witty but still informative: {base_query}"
    else:
        return base_query

# --- Handle query submission ---
if query:
    if query.strip().lower() in ["who is simon", "who's simon"]:
        response = "👋 Simon is a PhD researcher at KU Leuven, specializing in fairness, causal ML, and HR analytics. Rumor has it he runs on data, code, and espresso. He also loves het klein bazeke."
    else:
        full_query = apply_persona(persona, query)

        with st.spinner("Fetching answer..."):
            response = answer_question(full_query)

    # --- Display Answer ---
    st.markdown("**Answer:**")
    st.write(response)

    # --- Update history ---
    st.session_state.qa_history.append((query, response))

    # --- Log to Google Sheets via Apps Script Webhook ---
    GOOGLE_APPS_SCRIPT_URL = st.secrets["google_logging_url"]

    form_data = {
        "query": query,
        "response": response,
    }

    try:
        r = requests.post(GOOGLE_APPS_SCRIPT_URL, data=form_data, timeout=5)
        if r.status_code != 200:
            #st.warning("⚠️ Could not log interaction (Google Script error).")
            pass
    except Exception as e:
        #st.warning("⚠️ Could not log interaction (network error).")
        pass

# --- Display session history ---
if st.session_state.qa_history:
    with st.expander("📜 View your Q&A history this session"):
        for i, (q, a) in enumerate(st.session_state.qa_history[::-1], 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            st.markdown("---")
