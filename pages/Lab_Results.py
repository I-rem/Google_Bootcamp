import streamlit as st

st.title("🧪 Laboratuvar Sonuçları")

if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

# Dummy lab tests
lab_tests = {
    "Tam Kan Sayımı": "Hb: 13.5 g/dL, WBC: 8.2, PLT: 250k",
    "CRP": "4.2 mg/L",
    "BUN/Kreatinin": "BUN: 15, Cr: 0.9",
}

if "ordered_tests" not in st.session_state:
    st.session_state.ordered_tests = []

st.markdown("İsteyebileceğiniz testler:")

for test, result in lab_tests.items():
    if test not in st.session_state.ordered_tests:
        if st.button(f"{test} iste"):
            st.session_state.ordered_tests.append(test)

st.markdown("### Sonuçlar:")
for test in st.session_state.ordered_tests:
    st.markdown(f"**{test}:** {lab_tests[test]}")
