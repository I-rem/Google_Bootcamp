import streamlit as st
import json
from streamlit_lottie import st_lottie
from user_auth import (
    authenticate, register, user_exists,
    verify_security_answer, reset_password
)
from db import init_db

# Veritabanını başlat
init_db()

# Sayfa ayarları
st.set_page_config(page_title="Beni Teşhis Et", layout="wide", page_icon="🩺")

# Lottie animasyonu yükleyici
def load_lottie_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# Animasyonu yükle
lottie_json = load_lottie_file("animations/search users.json")

# Session state ayarları
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "redirected" not in st.session_state:
    st.session_state.redirected = False

# Giriş yapan kullanıcıyı göster
if st.session_state.logged_in:
    st.sidebar.markdown(f"👤 Giriş yapan: **{st.session_state.username}**")

# Menü seçimi
if st.session_state.logged_in:
    menu = st.sidebar.selectbox("Menü", ["Ana Sayfa", "Çıkış"])
else:
    menu = st.sidebar.selectbox("Menü", ["Giriş Yap", "Kayıt Ol", "Şifre Sıfırla"])

# Giriş yaptıysa sayfaya yönlendir
if st.session_state.logged_in and not st.session_state.redirected:
    st.session_state.redirected = True
    st.switch_page("pages/Vaka_Seçimi.py")

# Giriş ekranı
def show_login():
    st.title("                                                             Giriş Yap                                         ")
    st_lottie(lottie_json, height=250)  # 🔥 Animasyonu burada gösteriyoruz

    username = st.text_input("Kullanıcı Adı", key="login_username")
    password = st.text_input("Şifre", type="password", key="login_password")
    if st.button("Giriş"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Hoşgeldiniz, {username}!")
            st.switch_page("pages/Vaka_Seçimi.py")
        else:
            st.error("Kullanıcı adı veya şifre yanlış!")

# Kayıt ekranı
def show_register():
    st.title("📝 Kayıt Ol")
    new_username = st.text_input("Yeni Kullanıcı Adı", key="reg_username")
    new_password = st.text_input("Şifre", type="password", key="reg_password")
    security_answer = st.text_input("Güvenlik Sorusu: En sevdiğiniz renk nedir?", key="reg_sec_answer")

    if st.button("Kayıt Ol"):
        if not new_username or not new_password or not security_answer:
            st.error("Lütfen tüm alanları doldurun.")
        elif user_exists(new_username):
            st.error("Bu kullanıcı adı zaten alınmış.")
        else:
            if register(new_username, new_password, security_answer):
                st.success("Kayıt başarılı! Giriş yapılıyor...")
                st.session_state.logged_in = True
                st.session_state.username = new_username
                st.switch_page("pages/Case_Selection.py")
            else:
                st.error("Kayıt yapılamadı, lütfen tekrar deneyin.")

# Şifre sıfırlama ekranı
def show_reset_password():
    st.title("🔑 Şifre Sıfırlama")
    username = st.text_input("Kullanıcı Adınız", key="reset_username")
    security_answer = st.text_input("Güvenlik Sorusu Cevabınız:", key="reset_sec_answer")
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

# Ana sayfa
def show_landing():
    st.title("🩺 Beni Teşhis Et")
    st.markdown(f"Hoşgeldiniz, **{st.session_state.username}**! Klinik vaka çözümleme pratiğine başlayabilirsiniz.")
    st.markdown("**Sol menüden** bir vaka seçerek başlayabilirsiniz.")
    if st.button("Çıkış Yap"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.redirected = False
        st.rerun()

# Sayfa yönlendirme
if st.session_state.logged_in:
    if menu == "Ana Sayfa":
        show_landing()
    elif menu == "Çıkış":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.redirected = False
        st.rerun()
else:
    if menu == "Giriş Yap":
        show_login()
    elif menu == "Kayıt Ol":
        show_register()
    elif menu == "Şifre Sıfırla":
        show_reset_password()
