# Case_Selection.py (Merged)
import os
import unicodedata
import re
import streamlit as st

if "username" not in st.session_state:
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

username = st.session_state["username"]

st.title("📋 Vaka Seçimi")

from cases import cases_by_department

# Fonksiyon: Bölüm adını dosya adı formatına çevirme
def slugify_department_name(department_name):
    department_name = re.sub(r'\s*\(.*\)', '', department_name).strip()
    normalized_name = unicodedata.normalize('NFKD', department_name).encode('ascii', 'ignore').decode('utf-8')
    slug = normalized_name.lower().replace(' ', '_')
    slug = re.sub(r'[^a-z0-9_]', '', slug)
    return slug

st.markdown("### Bir Bölüm Seçin:")

num_cols = 4
cols = st.columns(num_cols)

if "selected_department_card" not in st.session_state:
    st.session_state.selected_department_card = None

ASSETS_DIR = "assets"
IMAGE_EXTENSION = "png"

for i, department_name in enumerate(cases_by_department.keys()):
    with cols[i % num_cols]:
        image_filename = f"{slugify_department_name(department_name)}.{IMAGE_EXTENSION}"
        image_path = os.path.join(ASSETS_DIR, image_filename)

        if os.path.exists(image_path):
            st.image(image_path, caption=department_name, width=100)
        else:
            st.warning(f"Resim bulunamadı: '{image_filename}'.")
            st.write(department_name)

        if st.button(f"Vakaları Gör", key=f"select_dept_{department_name}"):
            st.session_state.selected_department_card = department_name
            st.rerun()

if st.session_state.selected_department_card:
    selected_department_name = st.session_state.selected_department_card
    st.subheader(f"{selected_department_name} Bölümü Vakaları:")

    cases_in_department = cases_by_department[selected_department_name]
    case_complaints = [case["complaint"] for case in cases_in_department]

    default_case_index = 0
    if "selected_case" in st.session_state and st.session_state.selected_case in cases_in_department:
        try:
            default_case_index = case_complaints.index(st.session_state.selected_case["complaint"])
        except ValueError:
            default_case_index = 0

    selected_complaint = st.selectbox(
        "Bir vaka seçin:", 
        case_complaints, 
        index=default_case_index
    )

    if selected_complaint:
        selected_case = next(case for case in cases_in_department if case["complaint"] == selected_complaint)

        st.session_state.selected_case = selected_case
        st.session_state.chat_history = []
        st.session_state.ordered_tests = []
        st.session_state.submitted_diagnosis = None
        st.session_state.ai_feedback = None
        st.session_state.score = None

        st.subheader(f"Vaka : {selected_case['id']} - {selected_case['complaint']}")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Yaş:** {selected_case['age']}")
            st.markdown(f"**Cinsiyet:** {selected_case['gender']}")
            st.markdown(f"**Şikayet:** {selected_case['complaint']}")
            st.markdown(f"**Öykü:** {selected_case['history']}")
