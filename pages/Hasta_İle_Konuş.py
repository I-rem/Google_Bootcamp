import streamlit as st
from streamlit_lottie import st_lottie
import json
from gemini_utils import get_patient_response

# Giriş kontrolü
if not st.session_state.get("logged_in", False):
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

username = st.session_state["username"]
st.title("🗣️ Hasta ile Konuş")

# Lottie animasyonu
def load_lottie_animation(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_chatbot = load_lottie_animation("animations/chatbot.json")
st_lottie(lottie_chatbot, speed=1, height=200, key="chatbot")

# Vaka kontrolü
if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

case = st.session_state.selected_case

# Sohbet geçmişi
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Girdi alanı
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

# Sesli yanıt
def speak_text(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text.replace('"', '\\"')}");
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0, width=0)

# Yanıt işleme fonksiyonu
def handle_submission():
    user_input = st.session_state.chat_input.strip()
    if not user_input:
        return

    st.session_state.chat_history.append(("Siz", user_input))
    try:
        response = get_patient_response(case, user_input)
        if not response or "Hata" in response:
            st.session_state.chat_history.append(("Hasta", "❌ Hasta şu anda yanıt veremiyor."))
        else:
            st.session_state.chat_history.append(("Hasta", response))
            speak_text(response)
    except Exception as e:
        st.session_state.chat_history.append(("Sistem", f"⚠️ Hata: {e}"))

    # 🧹 Input temizliği (widget render'ından sonra çalışır!)
    st.session_state.chat_input = ""

# Chat formu
with st.form("chat_form"):
    st.text_input("Hastaya sorunuzu yazın:", key="chat_input")
    submitted = st.form_submit_button("Gönder", on_click=handle_submission)

# Sohbet geçmişi
st.markdown("### 🧾 Sohbet Geçmişi")
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")
