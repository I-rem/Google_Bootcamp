import streamlit as st

st.title("✅ Tanı Gönder")

if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

correct_diagnosis = "Appendisit"  # Dummy

with st.form("diagnosis_form"):
    diagnosis = st.text_input("Tanınızı yazınız:")
    submitted = st.form_submit_button("Gönder")

if submitted: # Should probably get gemini involved here too
    st.session_state.submitted_diagnosis = diagnosis
    if diagnosis.lower().strip() == correct_diagnosis.lower():
        st.success("Doğru tanı!")
    else:
        st.error("Yanlış tanı. Doğru cevap: " + correct_diagnosis)
