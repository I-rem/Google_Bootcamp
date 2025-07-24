import streamlit as st
from cases import cases

st.title("📋 Vaka Seçimi")
st.markdown("Lütfen bir vaka seçin:")
for case in cases:
    if st.button(f"Vaka {case['id']}: {case['age']} y, {case['gender']} - {case['complaint']}"):
        st.session_state.selected_case = case
        st.session_state.chat_history = []
        st.session_state.ordered_tests = []
        st.session_state.submitted_diagnosis = None
        st.session_state.ai_feedback = None
        st.session_state.score = None
        st.success(f"Vaka {case['id']} seçildi!")



if "selected_case" in st.session_state:
    st.markdown("### Seçilen Vaka Bilgileri:")
    case = st.session_state.selected_case
    st.write(f"**Şikayet:** {case['complaint']}")
    st.write(f"**Öykü:** {case['history']}")
