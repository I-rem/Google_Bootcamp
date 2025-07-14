import streamlit as st
import random

st.title("🗣️ Hasta ile Konuş")

if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

case = st.session_state.selected_case

# Simulate patient replies using symptom/history
def simulate_patient_reply(question):
    q = question.lower()
    if "ne zamandır" in q:
        return f"{case['history']}"
    elif any(kw in q for kw in ["bulantı", "kusma", "ateş", "iştah"]):
        symptoms = ", ".join(case['symptoms'])
        return f"Evet, şu belirtilerim var: {symptoms}."
    elif "şikayet" in q or "neden geldiniz" in q:
        return case["complaint"]
    else:
        return random.choice([
            "Bu konuda emin değilim.",
            "Biraz daha açıklar mısınız?",
            "Belirtilerimi tam anlayamıyorum, tekrar sorabilir misiniz?"
        ])

# Initialize chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input form
with st.form("chat_form"):
    user_input = st.text_input("Soru", key="chat_input")
    submitted = st.form_submit_button("Gönder")

if submitted and user_input:
    st.session_state.chat_history.append(("Siz", user_input))
    response = simulate_patient_reply(user_input)
    st.session_state.chat_history.append(("Hasta", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")
