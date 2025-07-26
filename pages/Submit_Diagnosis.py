import streamlit as st

st.title("✅ Tanı Gönder")

if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

# Seçilen vakanın doğru tanısını dinamik olarak al
case = st.session_state.selected_case
correct_diagnosis = case.get("diagnosis", "Tanı belirtilmemiş") # Eğer tanı yoksa varsayılan bir değer ata

with st.form("diagnosis_form"):
    diagnosis = st.text_input("Tanınızı yazınız:")
    submitted = st.form_submit_button("Gönder")

if submitted:
    st.session_state.submitted_diagnosis = diagnosis
    # Kullanıcının girdiği tanıyı, seçilen vakanın doğru tanısı ile karşılaştır
    if diagnosis.lower().strip() == correct_diagnosis.lower().strip():
        st.success("Doğru tanı! Tebrikler.")
    else:
        st.error(f"Yanlış tanı. Doğru cevap: **{correct_diagnosis}**")
