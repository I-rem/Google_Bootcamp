import streamlit as st
import json
from streamlit_lottie import st_lottie

# 🔐 Giriş kontrolü
if not st.session_state.get("logged_in", False):
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

# 🎬 Animasyon yükleyici
def load_lottie_animation(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

st.title("🧠 Geri Bildirim")
st_lottie(load_lottie_animation("animations/Feedback.json"), height=150, key="feedback")

# Vaka kontrolü
if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

case = st.session_state.selected_case
case_id = case["id"]

# Session state kontrolleri
if "submitted_diagnoses" not in st.session_state or case_id not in st.session_state.submitted_diagnoses:
    st.warning("Bu vaka için henüz tanı gönderilmemiş.")
    st.stop()



# 🔎 Vaka Özeti
st.markdown("### 📄 Tanıya Genel Bakış")
st.markdown(f"""
- **Şikayet:** {case['complaint']}
- **Öykü:** {case['history']}
- **Semptomlar:** {', '.join(case['symptoms'])}
""")
st.markdown("Bu bilgiler doğru tanıyı destekleyen unsurlardır.")

# 🧠 Skor
st.markdown("---")
st.markdown("### 🧮 Klinik Yaklaşım Skorunuz")

score = st.session_state.get("score_dict", {}).get(case_id)
breakdown = st.session_state.get("score_breakdown_dict", {}).get(case_id)

if score is not None:
    st.metric(label="Yapay Zeka Skoru", value=f"{score} / 100")
    if breakdown:
        for key, val in breakdown.items():
            st.markdown(f"- **{key}**: {val} puan")
else:
    st.info("Skor henüz hesaplanmamış.")

# 🤖 Geri Bildirim
st.markdown("---")
st.markdown("### 🤖 Yapay Zeka Geri Bildirimi")

ai_feedback = st.session_state.get("ai_feedback", {}).get(case_id)
if ai_feedback:
    st.markdown(ai_feedback)
else:
    st.info("Geri bildirim bulunamadı.")
