import streamlit as st
from ui_helpers import render_sidebar, render_header

render_sidebar()
render_header("Vaka İstatistikleri", icon="📊")

if "completed_cases" not in st.session_state or len(st.session_state.completed_cases) == 0:
    st.info("Henüz tamamladığınız bir vaka yok.")
    st.stop()

total = len(st.session_state.completed_cases)
correct = sum(1 for c in st.session_state.completed_cases if c["is_correct"])
avg_score = sum(c["score"] for c in st.session_state.completed_cases) / total

st.markdown(f"**✅ Doğru Tanılar:** {correct} / {total}")
st.markdown(f"**📈 Ortalama Skor:** {round(avg_score)} / 100")
st.divider()

for i, case in enumerate(st.session_state.completed_cases[::-1]):
    st.markdown(f"### 🧾 Vaka {case['case_id']}")
    st.markdown(f"- **Şikayet:** {case['complaint']}")
    st.markdown(f"- **Tanınız:** {case['user_diagnosis']}")
    st.markdown(f"- **Doğru Tanı:** {case['correct_diagnosis']}")
    st.markdown(f"- **Durum:** {'✅ Doğru' if case['is_correct'] else '❌ Yanlış'}")
    st.markdown(f"- **Skor:** {case['score']} / 100")
    st.markdown("---")
