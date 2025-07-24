from db import init_db
init_db()

import streamlit as st

st.set_page_config(page_title="Beni Teşhis Et", layout="wide", page_icon="🩺")

st.markdown("# 🩺 Beni Teşhis Et")
st.markdown("""
Hoş geldiniz! Bu uygulama, tıp öğrencilerinin klinik vaka çözümleme becerilerini geliştirmeleri için tasarlanmıştır.

Sol menüden bir vaka seçerek simülasyona başlayabilirsiniz.
""")

with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3374/3374949.png", width=120)
    with col2:
        st.markdown("### 🚀 Hazır Özellikler")
        st.markdown("- 📋 Vaka Seçimi\n- 🤖 AI ile Hasta Konuşması\n- 🧪 Laboratuvar Testleri\n- ✅ Tanı Gönderimi\n- 🧠 AI Geri Bildirim ve Skor")
