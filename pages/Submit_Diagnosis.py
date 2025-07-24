from supabase_client import insert_case_result
import streamlit as st
from gemini_utils import (
    get_ai_feedback,
    is_diagnosis_correct_ai,
    get_clinical_score_ai
)

st.title("✅ Tanı Gönder")

if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

case = st.session_state.selected_case
correct_diagnosis = case["diagnosis"].strip().lower()

if "submitted_diagnosis" in st.session_state:
    st.success("Tanınız zaten gönderildi. Geri bildirim sayfasına geçebilirsiniz.")

with st.form("diagnosis_form"):
    diagnosis = st.text_input("\U0001F4CC Tanınızı yazınız:", value="", placeholder="Örn: Apandisit")
    submitted = st.form_submit_button("Gönder")

if submitted:
    user_diagnosis = diagnosis.strip().lower()
    st.session_state.submitted_diagnosis = user_diagnosis

    with st.spinner("Tanınız değerlendiriliyor..."):
        is_correct = is_diagnosis_correct_ai(user_diagnosis, correct_diagnosis)

    if is_correct:
        st.success("\U0001F389 Tanınız klinik olarak doğru!")
    else:
        st.error("❌ Tanınız tam olarak doğru değil.")
        st.info(f"✅ Beklenen Tanı: **{case['diagnosis']}**")

    with st.spinner("\U0001F9E0 Yapay zeka geri bildirimi ve skor hesaplanıyor..."):
        st.session_state.ai_feedback = get_ai_feedback(
    case,
    st.session_state.chat_history,
    st.session_state.ordered_tests
)


        ai_score = get_clinical_score_ai(case, st.session_state.chat_history)
        st.session_state.score = ai_score
        st.session_state.score_breakdown = {"AI Klinik Yaklaşım Skoru": ai_score}

    insert_case_result({
    "case_id": case["id"],
    "complaint": case["complaint"],
    "user_diagnosis": user_diagnosis,
    "correct_diagnosis": case["diagnosis"],
    "is_correct": is_correct,
    "score": st.session_state.score
})

    st.success("\U0001F50D Değerlendirme tamamlandı! Sol menüden geri bildiriminizi inceleyebilirsiniz.")


#record = {
#    "case_id": case["id"],
#    "complaint": case["complaint"],
#    "user_diagnosis": user_diagnosis,
#    "correct_diagnosis": case["diagnosis"],
#    "is_correct": is_correct,
 #   "score": st.session_state.score
#}

#if "completed_cases" not in st.session_state:
#    st.session_state.completed_cases = []

#st.session_state.completed_cases.append(record)
