import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Beni Teşhis Et", layout="wide")

st.title("🩺 Beni Teşhis Et")
st.markdown("""
Hoş geldiniz! Bu uygulama, tıp öğrencilerinin klinik vaka çözümleme becerilerini geliştirmeleri için tasarlanmıştır. 
**Sol menüden** bir vaka seçerek çözmeye başlayabilirsiniz.
""")
