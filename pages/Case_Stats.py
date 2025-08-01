import streamlit as st
from supabase_client import fetch_all_results
from ui_helpers import render_sidebar, render_header

render_sidebar()
render_header("Vaka İstatistikleri", icon="📊")

# Veritabanından verileri çek
try:
    results = fetch_all_results()
except Exception as e:
    st.error(f"❌ Supabase bağlantı hatası: {e}")
    st.stop()

# Handle empty state
if not results:
    st.info("Henüz kayıtlı vaka çözümünüz yok.")
    st.stop()

# Özet istatistikler
total_cases = len(results)
correct_cases = sum(1 for row in results if row["is_correct"])
avg_score = sum(row["score"] for row in results) / total_cases

# Metrics
st.markdown("### 📊 Genel Performans")
col1, col2 = st.columns(2)
col1.metric("✅ Doğru Tanı Sayısı", f"{correct_cases} / {total_cases}")
col2.metric("📈 Ortalama Skor", f"{round(avg_score)} / 100")
st.divider()

# Detailed case records
st.markdown("### 🧾 Geçmiş Vaka Kayıtları")

for row in results:
    st.markdown(f"""
    #### 🧪 Vaka {row['case_id']}
    - 🩺 **Şikayet:** {row['complaint']}
    - 📝 **Tanınız:** `{row['user_diagnosis']}`
    - ✅  **Doğru Tanı:** `{row['correct_diagnosis']}`
    - 🎯 **Sonuç:** {"✅ Doğru" if row['is_correct'] else "❌ Yanlış"}
    - 🏆 **Skor:** {row['score']} / 100
    - ⏱️ **Tarih:** {row['timestamp']}
    """)
    st.markdown("---")
    
st.markdown(f"### 📌 Özet")
col1, col2 = st.columns(2)
col1.metric("✅ Doğru Tanı Sayısı", f"{correct} / {total}")
col2.metric("📈 Ortalama Skor", f"{round(avg_score)} / 100")
st.divider()
