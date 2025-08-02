import streamlit as st
from gemini_utils import (
    get_ai_feedback,
    is_diagnosis_correct_ai,
    get_clinical_score_ai
)
from supabase_client import insert_case_result
import json
from streamlit_lottie import st_lottie

# Başlık ve animasyon
st.title("✅ Tanı Gönder")

def load_lottie_animation(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

st_lottie(load_lottie_animation("animations/Doctor.json"), height=150, key="doctor")

# Giriş kontrolü
if not st.session_state.get("logged_in", False):
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

# Vaka kontrolü
if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

case = st.session_state.selected_case
case_id = case["id"]
correct_diagnosis = case.get("diagnosis", "").strip().lower()

# 🔐 Session state güvenli başlatma
if "submitted_diagnoses" not in st.session_state:
    st.session_state.submitted_diagnoses = {}
if "ai_feedback" not in st.session_state or st.session_state.ai_feedback is None:
    st.session_state.ai_feedback = {}
if "score_dict" not in st.session_state or st.session_state.score_dict is None:
    st.session_state.score_dict = {}
if "score_breakdown_dict" not in st.session_state or st.session_state.score_breakdown_dict is None:
    st.session_state.score_breakdown_dict = {}

# Zaten tanı gönderildiyse kullanıcıyı bilgilendir
if case_id in st.session_state.submitted_diagnoses:
    st.success("Bu vaka için tanı zaten gönderildi. Geri bildirim sayfasına geçebilirsiniz.")

# Tanı gönderme formu
with st.form("diagnosis_form"):
    diagnosis = st.text_input("📌 Tanınızı yazınız:", value="", placeholder="Örn: Apandisit")
    submitted = st.form_submit_button("Gönder")

# Tanı gönderildiyse:
if submitted:
    user_diagnosis = diagnosis.strip().lower()
    st.session_state.submitted_diagnoses[case_id] = user_diagnosis

    with st.spinner("Tanınız değerlendiriliyor..."):
        is_correct = is_diagnosis_correct_ai(user_diagnosis, correct_diagnosis)

    st.session_state.ai_diagnosis_correct = is_correct
    user_diag = st.session_state.submitted_diagnoses[case_id].strip().lower()
    correct_diag = case["diagnosis"].strip().lower()
    is_correct = st.session_state.get("ai_diagnosis_correct", False)

    # 🩺 Tanı karşılaştırması
    st.markdown(f"### 📌 Tanınız: **{user_diag.capitalize()}**")
    if is_correct or user_diag == correct_diag:
        st.success("🏆 Doğru tanı koydunuz!")
    else:
        st.error("❌ Tanınız hatalı.")
        st.info(f"✅ Doğru Tanı: **{case['diagnosis']}**")
    with st.spinner("🧠 Yapay zeka geri bildirimi ve skor hesaplanıyor..."):
        feedback = get_ai_feedback(case, st.session_state.chat_history, st.session_state.ordered_tests)
        st.session_state.ai_feedback[case_id] = feedback

        score = get_clinical_score_ai(case, st.session_state.chat_history)
        st.session_state.score_dict[case_id] = score
        st.session_state.score_breakdown_dict[case_id] = {"AI Klinik Yaklaşım Skoru": score}

    insert_case_result({
        "case_id": case_id,
        "complaint": case["complaint"],
        "user_diagnosis": user_diagnosis,
        "correct_diagnosis": case["diagnosis"],
        "is_correct": is_correct,
        "score": score
    })

    st.success("🔍 Değerlendirme tamamlandı! Sol menüden geri bildiriminizi inceleyebilirsiniz.")
