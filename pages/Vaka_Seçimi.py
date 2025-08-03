import os
import unicodedata
import re
import streamlit as st
from streamlit_lottie import st_lottie
import json
from cases import cases_by_department

# Giriş kontrolü
if not st.session_state.get("logged_in", False):
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

st.title("📋 Vaka Seçimi")

# Animasyon
def load_lottie_animation(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

st_lottie(load_lottie_animation("animations/Child selector.json"), height=250)

# Yardımcı fonksiyon
def slugify(text):
    text = re.sub(r'\s*\(.*\)', '', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return text.replace(" ", "_")

# Department seçimi
st.markdown("### 🏥 Bir bölüm seçin:")

num_cols = 3
cols = st.columns(num_cols)

if "selected_department_card" not in st.session_state:
    st.session_state.selected_department_card = None

ASSETS_DIR = "assets"
EXT = "png"

# Kart şeklinde bölüm seçimi
for i, dept in enumerate(cases_by_department.keys()):
    with cols[i % num_cols]:
        img_path = os.path.join(ASSETS_DIR, f"{slugify(dept)}.{EXT}")
        if os.path.exists(img_path):
            st.image(img_path, width=120, caption=dept)
        else:
            st.markdown(f"**{dept}**")

        if st.button("Vaka Seç", key=dept):
            st.session_state.selected_department_card = dept
            st.session_state.selected_case = None  # sıfırla
            st.rerun()

# Vaka gösterimi
if st.session_state.selected_department_card:
    dept = st.session_state.selected_department_card
    cases = cases_by_department[dept]

    st.subheader(f"🩺 {dept} Bölümü Vakaları")
    
    for i, case in enumerate(cases):
        with st.expander(f"{case['complaint']}"):
            st.markdown(f"- **Yaş:** {case['age']}")
            st.markdown(f"- **Cinsiyet:** {case['gender']}")
            st.markdown(f"- **Öykü:** {case['history']}")
            st.markdown(f"- **Semptomlar:** {', '.join(case['symptoms'])}")

            if st.button("Bu vakayı seç", key=f"select_case_{i}"):
                st.session_state.selected_case = case
                st.session_state.chat_history = []
                st.session_state.ordered_tests = []
                st.session_state.submitted_diagnosis = None
                st.session_state.ai_feedback = None
                st.session_state.score = None
                st.success(f"✅ Vaka {case['id']} seçildi!")
