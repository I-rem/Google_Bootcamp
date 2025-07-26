import streamlit as st
from gemini_utils import get_patient_response
import streamlit.components.v1 as components

st.title("🗣️ Hasta ile Konuş")

if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

case = st.session_state.selected_case

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# JavaScript fonksiyonlarını tanımlayan HTML bileşeni
# speakText: Verilen metni tarayıcının ses sentezleyicisi ile okur.
# startSpeechRecognition: Mikrofonu açar ve konuşmayı metne dönüştürür.
speech_utils_js = """
<script>
    let voicesLoaded = false;
    let synth = window.speechSynthesis;

    // Seslerin yüklenmesini kontrol eden ve dinleyiciyi ayarlayan fonksiyon
    function loadVoices() {
        if (!synth) {
            console.error('SpeechSynthesis API tarayıcınızda mevcut değil. Seslendirme yapılamayacak.');
            return;
        }
        if (synth.getVoices().length > 0) {
            voicesLoaded = true;
            console.log("TTS Sesleri yüklendi.");
            // Streamlit'e seslerin yüklendiğini bildiren bir olay gönder
            if (window.parent) { // Streamlit iframe içinde çalışıyorsa
                window.parent.postMessage({ type: 'streamlit:setComponentValue', key: 'tts_status', value: 'loaded' }, '*');
            }
        } else {
            synth.onvoiceschanged = () => {
                voicesLoaded = true;
                console.log("TTS Sesleri 'onvoiceschanged' olayı sonrası yüklendi.");
                synth.onvoiceschanged = null; // Dinleyiciyi kaldır
                if (window.parent) {
                    window.parent.postMessage({ type: 'streamlit:setComponentValue', key: 'tts_status', value: 'loaded' }, '*');
                }
            };
        }
    }

    // Sayfa yüklendiğinde sesleri yüklemeye çalış
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        loadVoices();
    } else {
        window.addEventListener('DOMContentLoaded', loadVoices);
    }

    // Text-to-Speech (TTS) Function
    function speakText(text) {
        if (!synth) {
            console.warn('SpeechSynthesis API tarayıcınızda mevcut değil.');
            alert('Üzgünüm, tarayıcınız metin okuma özelliğini desteklemiyor.');
            return;
        }
        if (!voicesLoaded) {
            console.warn('Sesler henüz yüklenmedi. Lütfen birkaç saniye bekleyip tekrar deneyin veya tarayıcınızı yenileyin.');
            alert('Sesler henüz yüklenmedi. Lütfen birkaç saniye bekleyip tekrar deneyin.');
            loadVoices(); // Tekrar yüklemeyi dene
            return;
        }

        // Eğer konuşma devam ediyorsa durdur
        if (synth.speaking) {
            synth.cancel();
        }

        var utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'tr-TR'; // Türkçe dilini ayarla
        utterance.rate = 1.0; // Konuşma hızı (varsayılan 1.0)
        utterance.pitch = 1.0; // Konuşma perdesi (varsayılan 1.0)

        // Türkçe bir ses bulmaya çalış
        let turkishVoice = synth.getVoices().find(voice => voice.lang === 'tr-TR' || voice.lang.startsWith('tr'));
        if (turkishVoice) {
            utterance.voice = turkishVoice;
            console.log('Türkçe ses kullanılıyor:', turkishVoice.name);
        } else {
            console.warn('Türkçe ses bulunamadı, varsayılan ses kullanılacak.');
        }

        utterance.onend = function(event) {
            console.log('Metin seslendirme tamamlandı.');
        };
        utterance.onerror = function(event) {
            console.error('Metin seslendirme hatası:', event.error);
            alert('Seslendirme sırasında bir hata oluştu: ' + event.error);
        };

        try {
            synth.speak(utterance);
            console.log('Metin seslendiriliyor:', text);
        } catch (e) {
            console.error('Seslendirme başlatılırken hata:', e);
            alert('Seslendirme başlatılırken bir hata oluştu: ' + e.message);
        }
    }

    // Speech-to-Text (STT) Function
    function startSpeechRecognition(inputElementId) {
        // Tarayıcının SpeechRecognition API'sini destekleyip desteklemediğini kontrol et
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Üzgünüm, tarayıcınız konuşmadan metne dönüştürme (Speech-to-Text) özelliğini desteklemiyor. Lütfen Chrome veya Edge gibi modern bir tarayıcı kullanın.');
            console.warn('Tarayıcınız konuşmadan metne dönüştürme (Speech-to-Text) özelliğini desteklemiyor.');
            return;
        }

        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        var recognition = new SpeechRecognition();

        recognition.lang = 'tr-TR'; // Türkçe dilini ayarla
        recognition.interimResults = false; // Sadece nihai sonuçları al
        recognition.maxAlternatives = 1; // En iyi tahmini al

        var inputElement = document.getElementById(inputElementId);
        if (!inputElement) {
            console.error('Hedef giriş alanı bulunamadı:', inputElementId);
            return;
        }

        // Konuşma tanıma sonucu geldiğinde
        recognition.onresult = function(event) {
            var speechResult = event.results[0][0].transcript;
            inputElement.value = speechResult; // Metin giriş alanını güncelle

            // Streamlit'in input alanındaki değişikliği algılaması için bir 'input' olayı tetikle
            var inputEvent = new Event('input', { bubbles: true });
            inputElement.dispatchEvent(inputEvent);
        };

        // Konuşma tanıma sırasında hata oluştuğunda
        recognition.onerror = function(event) {
            console.error('Konuşma tanıma hatası:', event.error);
            alert('Konuşma tanıma sırasında bir hata oluştu: ' + event.error + '. Lütfen mikrofon izinlerinizi kontrol edin.');
        };

        // Konuşma tanıma sona erdiğinde
        recognition.onend = function() {
            console.log('Konuşma tanıma sona erdi.');
        };

        // Konuşma tanımayı başlat
        recognition.start();
        console.log('Dinliyorum...');
    }
</script>
"""
components.html(speech_utils_js, height=0) # JavaScript'i sayfaya enjekte et

# Seslerin yüklenip yüklenmediğini takip etmek için session_state kullan
if "tts_status" not in st.session_state:
    st.session_state.tts_status = "loading"

# JavaScript'ten gelen mesajları dinle
# Bu, seslerin yüklendiğini Streamlit'e bildirmek için kullanılır
st.components.v1.html(
    """
    <script>
        window.addEventListener('message', event => {
            if (event.data.type === 'streamlit:setComponentValue' && event.data.key === 'tts_status') {
                const value = event.data.value;
                console.log("Streamlit'e TTS durumu bildirildi: " + value);
            }
        });
    </script>
    """,
    height=0
)

# Seslerin yüklenme durumunu gösteren bir mesaj
if st.session_state.tts_status == "loading":
    st.info("Sesler yükleniyor... Lütfen bekleyin veya 'Seslendir' butonuna tekrar basmayı deneyin.")
else:
    st.success("Sesler yüklendi! Seslendirme özelliğini kullanabilirsiniz.")


# clear_on_submit=True parametresi ile formu gönderdikten sonra otomatik temizleme
with st.form("chat_form", clear_on_submit=True):
    # Hastaya soru sormak için metin giriş alanı
    user_input = st.text_input("Hastaya sorunuzu yazın:", key="chat_input")

    # Gönder butonu formun içinde kalır
    submitted = st.form_submit_button("Gönder")

# Sesli Soru Sor butonu formun dışında
if st.button("🎤 Sesli Soru Sor"):
    st.components.v1.html(
        f"""
        <script>
            startSpeechRecognition("chat_input");
        </script>
        """,
        height=0 # Görünür bir HTML elementi oluşturma
    )

if submitted and user_input:
    st.session_state.chat_history.append(("Siz", user_input))
    with st.spinner("Hasta yanıtlıyor..."): # Yanıt beklenirken spinner göster
        response = get_patient_response(case, user_input)
    st.session_state.chat_history.append(("Hasta", response))
    # Artık st.session_state.chat_input = "" satırına gerek yok, form otomatik temizlenecek.


st.markdown("### 🧾 Sohbet Geçmişi")
for i, (sender, message) in enumerate(st.session_state.chat_history):
    st.markdown(f"**{sender}:** {message}")
    if sender == "Hasta":
        # Her hasta mesajının yanına bir "Seslendir" butonu ekle
        # Butonun key'i benzersiz olmalı
        if st.button("🔊 Seslendir", key=f"speak_btn_{i}"):
            # JavaScript fonksiyonunu çağırmak için Streamlit'in özel JavaScript çalıştırma yeteneğini kullan
            st.components.v1.html(
                f"""
                <script>
                    speakText("{message.replace('"', '\\"')}"); // Tırnak işaretlerini kaçır
                </script>
                """,
                height=0 # Görünür bir HTML elementi oluşturma
            )

# Kullanıcıya sorun giderme ipuçları
st.info("""
**Ses gelmiyor mu? Şunları deneyebilirsiniz:**
1.  **Tarayıcı İzinleri:** Tarayıcınızın bu site için ses ve mikrofon kullanımına izin verdiğinden emin olun. Genellikle adres çubuğunun solundaki kilit simgesine tıklayarak kontrol edebilirsiniz.
2.  **Sistem Sesi:** Bilgisayarınızın veya cihazınızın sesinin açık olduğundan ve hoparlörlerinizin çalıştığından emin olun.
3.  **Tarayıcı Yenileme:** Sayfayı yenilemek (F5 veya Ctrl+R) bazen ses sentezi motorunun yüklenmesine yardımcı olabilir.
4.  **Farklı Tarayıcı:** Chrome veya Edge gibi modern bir tarayıcı kullanmayı deneyin. Bazı tarayıcılar Web Speech API'sini tam olarak desteklemeyebilir.
5.  **Türkçe Ses Desteği:** İşletim sisteminizde Türkçe metin okuma sesinin yüklü olduğundan emin olun. (Windows: Ayarlar > Saat ve Dil > Konuşma; macOS: Sistem Ayarları > Erişilebilirlik > Konuşma İçeriği)
6.  **Tarayıcı Konsolu Hataları:** Tarayıcınızda Geliştirici Araçları'nı (genellikle `F12` tuşu ile açılır) açın ve "Console" (Konsol) sekmesini kontrol edin. "Seslendir" butonuna bastığınızda burada herhangi bir hata mesajı (kırmızı renkte) veya uyarı (sarı renkte) olup olmadığını bana bildirin. Özellikle "SpeechSynthesis" veya "utterance" ile ilgili mesajlara dikkat edin.
""")
