import streamlit as st

st.title("🗣️ Hasta ile Konuş")

if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("Hastaya soru sorun:")

with st.form("chat_form"):
    user_input = st.text_input("Soru", key="chat_input")
    submitted = st.form_submit_button("Gönder")

if submitted and user_input:
    st.session_state.chat_history.append(("Siz", user_input))
    # Dummy response (to be replaced with Gemini)
    response = "Bu konuda biraz daha bilgi verebilir misiniz?"
    st.session_state.chat_history.append(("Hasta", response))

for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")
