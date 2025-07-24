import streamlit as st
from gemini_utils import get_patient_response

st.title("\U0001F9E0 Geri Bildirim")

if "selected_case" not in st.session_state or not st.session_state.get("submitted_diagnosis"):
    st.warning("Lütfen önce bir vaka seçin ve tanınızı gönderin.")
    st.stop()


case = st.session_state.selected_case

user_diag = st.session_state.submitted_diagnosis.lower().strip()
correct_diag = case["diagnosis"].lower().strip()

st.markdown(f"### \U0001F4DD Tanınız: **{st.session_state.submitted_diagnosis}**")

if user_diag == correct_diag or st.session_state.get("ai_diagnosis_correct"):
    st.success("\U0001F947 Doğru tanı koydunuz!")
else:
    st.error("❌ Yanlış tanı.")
    st.info(f"✅ Doğru Tanı: **{case['diagnosis']}**")

st.markdown("### \U0001F50D Tanıya Genel Bakış")
st.markdown(f"""
- **Şikayet:** {case['complaint']}
- **Öykü:** {case['history']}
- **Semptomlar:** {', '.join(case['symptoms'])}
""")

st.markdown("Bu belirtiler, bu tanıyı desteklemektedir.")

st.markdown("---")
st.markdown("### \U0001F3C6 Klinik Yaklaşım Skorunuz")

if "score" in st.session_state:
    st.metric(label="AI Skor", value=f"{st.session_state.score} / 100")
    for key, val in st.session_state.score_breakdown.items():
        st.markdown(f"- **{key}**: {val} puan")
else:
    st.info("Skor hesaplanmamış. Lütfen önce tanınızı gönderin.")

st.markdown("---")
st.markdown("### \U0001F916 Yapay Zeka Geri Bildirimi")

if "ai_feedback" in st.session_state:
    st.markdown(st.session_state.ai_feedback)
else:
    st.info("AI geri bildirimi henüz hesaplanmamış.")