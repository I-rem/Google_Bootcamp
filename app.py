import streamlit as st
from user_auth import (
    authenticate, register, user_exists,
    verify_security_answer, reset_password
)
from db import init_db

init_db()

st.set_page_config(page_title="Beni Teşhis Et", layout="wide", page_icon="🩺")

# Oturum durumu için session_state başlangıç
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

menu = st.sidebar.selectbox("Menü", ["Giriş Yap", "Kayıt Ol", "Şifre Sıfırla"])

def show_login():
    st.title("👤 Giriş Yap")
    username = st.text_input("Kullanıcı Adı", key="login_username")
    password = st.text_input("Şifre", type="password", key="login_password")
    if st.button("Giriş"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Hoşgeldiniz, {username}!")
        else:
            st.error("Kullanıcı adı veya şifre yanlış!")

def show_register():
    st.title("📝 Kayıt Ol")
    new_username = st.text_input("Yeni Kullanıcı Adı", key="reg_username")
    new_password = st.text_input("Şifre", type="password", key="reg_password")
    security_answer = st.text_input("Güvenlik Sorusu: En sevdiğiniz renk nedir? (Şifre sıfırlamak için)", key="reg_sec_answer")
    if st.button("Kayıt Ol"):
        if not new_username or not new_password or not security_answer:
            st.error("Lütfen tüm alanları doldurun.")
        elif user_exists(new_username):
            st.error("Bu kullanıcı adı zaten alınmış.")
        else:
            if register(new_username, new_password, security_answer):
                st.success("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
            else:
                st.error("Kayıt yapılamadı, lütfen tekrar deneyin.")

def show_reset_password():
    st.title("🔑 Şifre Sıfırlama")
    username = st.text_input("Kullanıcı Adınız", key="reset_username")
    security_answer = st.text_input("Güvenlik Sorusu Cevabınız: En sevdiğiniz renk nedir?", key="reset_sec_answer")
    new_password = st.text_input("Yeni Şifre", type="password", key="reset_new_password")
    if st.button("Şifreyi Sıfırla"):
        if not username or not security_answer or not new_password:
            st.error("Lütfen tüm alanları doldurun.")
        elif not user_exists(username):
            st.error("Böyle bir kullanıcı bulunamadı.")
        elif verify_security_answer(username, security_answer):
            if reset_password(username, new_password):
                st.success("Şifreniz başarıyla değiştirildi! Giriş yapabilirsiniz.")
            else:
                st.error("Şifre sıfırlama başarısız oldu, lütfen tekrar deneyin.")
        else:
            st.error("Güvenlik sorusu cevabı yanlış.")

def show_diagnosis_page():
    st.markdown("# 🩺 Beni Teşhis Et")
    st.markdown(f"Hoşgeldiniz, **{st.session_state.username}**! Bu uygulama, tıp öğrencilerinin klinik vaka çözümleme becerilerini geliştirmeleri için tasarlanmıştır.")
    st.markdown("""
    **Sol menüden** bir vaka seçerek çözmeye başlayabilirsiniz.
    """)

    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3374/3374949.png", width=120)
        with col2:
            st.markdown("### 🚀 Hazır Özellikler")
            st.markdown("- 📋 Vaka Seçimi\n- 🤖 AI ile Hasta Konuşması\n- 🧪 Laboratuvar Testleri\n- ✅ Tanı Gönderimi\n- 🧠 AI Geri Bildirim ve Skor")

    if st.button("Çıkış Yap"):
        st.session_state.logged_in = False
        st.session_state.username = ""

# Sayfa içeriği session_state durumuna göre gösteriliyor
if st.session_state.logged_in:
    show_diagnosis_page()
else:
    if menu == "Giriş Yap":
        show_login()
    elif menu == "Kayıt Ol":
        show_register()
    elif menu == "Şifre Sıfırla":
        show_reset_password()