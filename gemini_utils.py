import google.generativeai as genai
import streamlit as st
import time

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def _generate_response(model_name, prompt):
    try:
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(prompt, generation_config={
            "temperature": 0.7,
            "max_output_tokens": 256,
            "top_p": 0.95
        })
        return response.text.strip()
    except Exception as e:
        return f"__ERROR__: {e}"

def get_patient_response(case, question):
    prompt = f"""
Sen bir hasta simülasyonusun. Doktor sana sorular soracak ve yalnızca aşağıdaki vaka bilgilerine göre cevap vereceksin:

- Yaş: {case['age']}
- Cinsiyet: {case['gender']}
- Şikayet: {case['complaint']}
- Öykü: {case['history']}
- Semptomlar: {', '.join(case['symptoms'])}

Doktor: \"{question}\"

Lütfen sadece hasta perspektifinden, kısa, açık ve doğal bir cevap ver.
"""

    fast_model = "gemini-2.0-flash"
    fallback_model = "gemini-1.5-flash"

    response = _generate_response(fast_model, prompt)

    # Fallback if error or quota
    if response.startswith("__ERROR__"):
        if "quota" in response.lower() or "limit" in response.lower():
            st.warning("⚠️ Hızlı modelde kota aşıldı. Yavaş modele geçiliyor...")
            time.sleep(1)
            response = _generate_response(fallback_model, prompt)
        else:
            return f"❌ Hata: {response}"

    return response or "❗ Yanıt alınamadı."

def is_diagnosis_correct_ai(user_diagnosis, correct_diagnosis):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
Sen bir klinik eğitmen olarak, aşağıdaki iki tanının aynı hastalığı tarif edip etmediğini değerlendiriyorsun.

- Öğrencinin yazdığı tanı: \"{user_diagnosis}\"
- Doğru tanı: \"{correct_diagnosis}\"

Bu iki tanı **klinik olarak eşdeğer** mi?

Yalnızca \"EVET\" ya da \"HAYIR\" yaz. Açıklama yapma.
"""
        response = model.generate_content(prompt)
        return response.text.strip().lower().startswith("evet")
    except:
        return False

def get_clinical_score_ai(case, chat_history):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        questions = [q for sender, q in chat_history if sender == "Siz"]
        prompt = f"""
Sen bir klinik eğitmensin. Aşağıdaki hasta vakası ve öğrencinin hastaya sorduğu sorulara göre,
öğrencinin **klinik sorgulama yaklaşımını** değerlendir.

### Vaka:
- Yaş: {case['age']}
- Cinsiyet: {case['gender']}
- Şikayet: {case['complaint']}
- Öykü: {case['history']}
- Semptomlar: {', '.join(case['symptoms'])}

### Öğrencinin soruları:
{chr(10).join(f"- {q}" for q in questions)}

Lütfen öğrencinin yaklaşımını **100 üzerinden** puanla. Sadece sayı döndür.
"""
        response = model.generate_content(prompt)
        score_str = response.text.strip()
        score = int("".join(filter(str.isdigit, score_str)))
        return max(0, min(100, score))
    except:
        return None
    
def get_ai_feedback(case, chat_history):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        questions = [q for sender, q in chat_history if sender == "Siz"]
        prompt = f"""
Sen bir klinik eğitim asistanısın. Aşağıdaki hasta vakası ve öğrenci tarafından hastaya sorulan sorular temelinde, öğrenciye geri bildirim ver:

- Vakayı anlama becerisi
- Sorduğu soruların tıbbi kalitesi
- Eksik kalan kritik noktalar
- Hastayla iletişim ve empati düzeyi

### Vaka Bilgisi:
- Yaş: {case['age']}
- Cinsiyet: {case['gender']}
- Şikayet: {case['complaint']}
- Öykü: {case['history']}
- Belirtiler: {', '.join(case['symptoms'])}

### Öğrencinin Hastaya Sorduğu Sorular:
{chr(10).join(f"- {q}" for q in questions)}

Lütfen açık, yapıcı ve eğitici bir geri bildirim yaz. Puan verme veya sonuç yok, sadece detaylı geri bildirim ver.
"""

        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "🛑 Geri bildirim alınamadı."

    except Exception as e:
        return f"❗ AI Geri Bildirim Hatası: {e}"
