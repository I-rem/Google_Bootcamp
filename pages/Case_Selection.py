import streamlit as st

st.title("📋 Vaka Seçimi")

# Define rich patient cases
cases = [
    {
        "id": 1,
        "age": 25,
        "gender": "Kadın",
        "complaint": "Karın ağrısı",
        "history": "Hasta 2 gündür süren sağ alt kadran ağrısı şikayetiyle başvurmuş.",
        "symptoms": ["bulantı", "iştahsızlık", "ateş"],
        "lab_results": {
            "Tam Kan Sayımı": "Hb: 13.5, WBC: 14.2 (↑), PLT: 250k",
            "CRP": "48 mg/L (↑)",
            "USG": "Appendiks çapı > 6mm, çevresel ödem",
        },
        "diagnosis": "Akut apandisit",
    },
    {
        "id": 2,
        "age": 60,
        "gender": "Erkek",
        "complaint": "Göğüs ağrısı",
        "history": "Aniden başlayan, sol kola yayılan göğüs ağrısı. Hipertansiyon öyküsü var.",
        "symptoms": ["terleme", "nefes darlığı", "bulantı"],
        "lab_results": {
            "EKG": "ST elevasyonu V2-V4",
            "Troponin": "Pozitif",
            "EKO": "Anteriyor hipokinezi",
        },
        "diagnosis": "ST elevasyonlu miyokard enfarktüsü (STEMI)",
    },
]

# Show case buttons
st.markdown("Lütfen bir vaka seçin:")

for case in cases:
    if st.button(f"Vaka {case['id']}: {case['age']} yaşında {case['gender']} - {case['complaint']}"):
        st.session_state.selected_case = case
        st.session_state.chat_history = []  # reset chat
        st.session_state.ordered_tests = []  # reset labs
        st.success(f"Vaka {case['id']} seçildi!")

# Show selected case info
if "selected_case" in st.session_state:
    st.markdown("### Seçilen Vaka Bilgileri:")
    case = st.session_state.selected_case
    st.write(f"**Şikayet:** {case['complaint']}")
    st.write(f"**Öykü:** {case['history']}")
