import streamlit as st
from gemini_utils import get_patient_response

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
    with st.spinner("Yanıt bekleniyor..."):
        try:
            st.session_state.chat_history.append(("Siz", user_input))
            response = get_patient_response(case, user_input)

            if not response or "Hata" in response:
                st.session_state.chat_history.append(("Hasta", "❌ Hasta şu anda yanıt veremiyor."))
            else:
                st.session_state.chat_history.append(("Hasta", response))
        except Exception as e:
            st.session_state.chat_history.append(("Sistem", f"⚠️ Hata: {e}"))

st.markdown("### 🧾 Sohbet Geçmişi")
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")

if st.button("Test Gemini Yanıtı"):
    with st.spinner("Gemini deneniyor..."):
        test = get_patient_response(case, "Ne zamandır şikayetiniz var?")
        if test and "Hata" not in test:
            st.success("✅ Yanıt alındı!")
            st.write(test)
        else:
            st.error("❌ Yanıt alınamadı veya hata oluştu.")
            st.write(test)
