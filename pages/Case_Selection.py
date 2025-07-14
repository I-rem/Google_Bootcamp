import streamlit as st

st.title("📋 Vaka Seçimi")

# Dummy patient data
cases = [
    {"id": 1, "age": 25, "gender": "Kadın", "complaint": "Karın ağrısı"},
    {"id": 2, "age": 60, "gender": "Erkek", "complaint": "Göğüs ağrısı"},
    {"id": 3, "age": 40, "gender": "Kadın", "complaint": "Nefes darlığı"},
]

st.markdown("Lütfen bir vaka seçin:")

for case in cases:
    if st.button(f"Vaka {case['id']}: {case['age']} yaşında {case['gender']} - {case['complaint']}"):
        st.session_state.selected_case = case
        st.success(f"Vaka {case['id']} seçildi!")

if "selected_case" in st.session_state:
    st.markdown("### Seçilen Vaka:")
    st.json(st.session_state.selected_case)
