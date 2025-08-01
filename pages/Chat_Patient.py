import streamlit as st
from gemini_utils import get_patient_response
if "username" not in st.session_state:
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

username = st.session_state["username"]


st.title("🗣️ Hasta ile Konuş")

if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

case = st.session_state.selected_case

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form("chat_form"):
    user_input = st.text_input("Hastaya sorunuzu yazın:", key="chat_input")
    submitted = st.form_submit_button("Gönder")

if submitted and user_input:
    st.session_state.chat_history.append(("Siz", user_input))
    response = get_patient_response(case, user_input)
    st.session_state.chat_history.append(("Hasta", response))

st.markdown("### 🧾 Sohbet Geçmişi")
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")
