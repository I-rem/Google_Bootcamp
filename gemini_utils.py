import streamlit as st
import google.generativeai as genai

# Configure Gemini with your key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_patient_response(case, question):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")


        prompt = f"""
Sen bir hasta simülasyonusun. Doktor sana sorular soracak ve yalnızca aşağıdaki vaka bilgilerine göre cevap vereceksin:

- Yaş: {case['age']}
- Cinsiyet: {case['gender']}
- Şikayet: {case['complaint']}
- Öykü: {case['history']}
- Semptomlar: {', '.join(case['symptoms'])}

Doktor: "{question}"

Lütfen kısa, gerçekçi ve sadece hastaya ait cevabı ver.
"""

        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        return f"❗ Hata oluştu: {e}"
