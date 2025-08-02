import streamlit as st
from streamlit_lottie import st_lottie
import json
from gemini_utils import get_patient_response

# Giriş kontrolü
if not st.session_state.get("logged_in", False):
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

username = st.session_state["username"]
st.title(" Hasta ile Konuş")

# Lottie animasyonunu yükleme
def load_lottie_animation(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_chatbot = load_lottie_animation("animations/chatbot.json")

# Animasyonu göster
st_lottie(lottie_chatbot, speed=1, height=200, key="chatbot")

# Vaka kontrolü
if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

case = st.session_state.selected_case

# Sohbet geçmişi
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sesli yanıt
def speak_text(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text.replace('"', '\\"')}");
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0, width=0)

# Chat formu
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
                speak_text(response)  # Hastanın cevabını sesli okut
        except Exception as e:
            st.session_state.chat_history.append(("Sistem", f"⚠️ Hata: {e}"))

# Sohbet geçmişi
st.markdown("### 🧾 Sohbet Geçmişi")
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")

# Gemini testi
if st.button("Test Gemini Yanıtı"):
    with st.spinner("Gemini deneniyor..."):
        test = get_patient_response(case, "Ne zamandır şikayetiniz var?")
        if test and "Hata" not in test:
            st.success("✅ Yanıt alındı!")
            st.write(test)
        else:
            st.error("❌ Yanıt alınamadı veya hata oluştu.")
            st.write(test)
