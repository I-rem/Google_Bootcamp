import streamlit as st

def render_sidebar():
    st.sidebar.title("🔍 Navigasyon")
    st.sidebar.info("👩‍⚕️ Lütfen soldan bir vaka seçin ve adımları takip edin.")

def render_header(title: str, icon: str = "📄"):
    st.markdown(f"## {icon} {title}")
    st.divider()
