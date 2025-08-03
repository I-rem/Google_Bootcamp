# 🩺 Beni Teşhis Et

https://github.com/user-attachments/assets/78fa1b4f-830c-4da9-a480-e6f7f827dd55

## Nedir Bu Uygulama?

**Beni Teşhis Et**, tıp fakültesi öğrencilerinin klinik düşünme becerilerini geliştirmesi için hazırlanmış, etkileşimli bir **hasta simülasyon** uygulamasıdır.

Uygulama, yapay zeka destekli sanal hastalarla diyalog kurmanıza, laboratuvar tetkikleri istemenize, tanınızı sunmanıza ve yapay zekadan detaylı geri bildirim almanıza olanak sağlar.

---





## 🚀 Özellikler

- **Yapay Zeka ile Hasta Simülasyonu**  
  Gerçekçi vakalarda sanal hastayla konuşabilir, klinik sorgulama yapabilirsiniz.

- **Laboratuvar Testleri**  
  Uygun tanıya ulaşmak için laboratuvar testleri isteyebilirsiniz.

- **Tanı ve Yapay Zeka Geri Bildirimi**  
  Tanınızı girin, yapay zeka hem doğruluğu hem de yaklaşımınızı analiz ederek puan ve geri bildirim versin.

- **İstatistikler ve Skor Takibi**  
  Geçmiş vaka performanslarınızı ve tanı doğruluk oranınızı görüntüleyin.

- **Kullanıcı Girişi / Kayıt Sistemi**  
  Kayıt olun, şifre sıfırlayın ve kişisel istatistiklerinizi koruyun.

- **Sesli Hasta Cevapları**  
  Hastanın verdiği cevaplar otomatik olarak sesli şekilde oynatılır.

---

## 🧠 Destekleyen Teknolojiler
- Streamlit

- Google Gemini API

- Supabase

- Python

# Kurulum
Hemen deneyin: https://beniteshiset.streamlit.app/

veya

1. **Projeyi klonlayın**

   `git clone https://github.com/I-rem/Google_Bootcamp.git`
   
   `cd Google_Bootcamp`
   
2. **Sanal ortam oluşturun ve bağımlılıkları yükleyin**
 
    `python -m venv .venv`
  
    `source .venv/bin/activate`  # Windows için: .venv\Scripts\activate
    
    `pip install -r requirements.txt`
  
3. `.streamlit/secrets.toml` **dosyasını oluşturun**

  ```bash
  [general]
  GEMINI_API_KEY = "your_google_gemini_api_key"
  SUPABASE_URL = "your_supabase_project_url"
  SUPABASE_KEY = "your_supabase_anon_or_service_key"
  ```

4. **Uygulamayı başlatın**

    `streamlit run app.py`

# Takım
## Takım İsmi
Team 15

## Takım Logosu

![image](https://github.com/user-attachments/assets/c94b2927-7b03-4be6-bc35-78d109b3735c)

# Takım Elemanları
- **İrem Ayşe Kayacıoğlu**: Scrum Master
- **Saadet Demir**: Product Owner
- **Zeynep Bilgili**: Developer
- **Kenan Güzel**: Developer

# Proje
## Ürün İsmi
BeniTeşhisEt
## Ürün Açıklaması
Tıp öğrencilerinin klinik düşünme, teşhis koyma ve tedavi planlama becerilerini geliştirmeleri için tasarlanmış, yapay zeka destekli bir hasta simülasyon uygulaması. Öğrenci doktor rolünde olurken, chatbot sanal hasta olarak semptomlarını anlatır, öğrenci soru sorabilir, tahlil isteyebilir ve vaka yönetimi pratiği yapabilir.
## Ürün Özellikleri
- Chatbot Hasta Simülasyonu: Öğrencinin sorularına göre hasta semptomlarını anlatan AI.
- Tahlil/Test Modülü: Öğrencinin istediği tetkiklerin sonuçlarını sunar.
- Eğitim Raporları: Öğrencinin performansını ve doğru/yanlış teşhislerini raporlar.
## Hedef Kitle

- Tıp Fakültesi öğrencileri
- TUS hazırlık kursları
- Medikal film/dizi meraklıları

# Süreç
## Backlog URL
[Trello Linkimiz](https://trello.com/b/9t5014dP/team-15)
## Sprint 1
- **Sprint Notları:** Takım üyelerinin final haftasında olduğu için ilk toplantımızı takım değiştirme haftasından sonra yapmaya karar verdik. Sprinting geç başlaması ve düzenin yeni oturması nedeniyle velocity'miz düşük kaldı. Pazar araştırılması yapıldı, takım üyelerinin tecrübeleri değerlendirildi, proje fikri belirlendi, roller atandı, toplantı düzeni belirlendi.
- **Sprint İçinde Tamamlanması Tahmin Edilen Puan:** 18 story points
- **Puan Tamamlama Mantığı:** Fibonacci ölçeği 5 kişilik bir ekiple haftada kişi başı ortalama 4 puan ile sprint başına 40 puan düşünüldü. Ancak ekipten bir kişinin eksilmesi ve Sprintin geç başlamasıyla hedefi daha gerçekçi olmak adına düşürdük.
- **Daily Scrum:** Daily toplantılar yerine günlük whatsapp konuşmaları ve Trello'da yapılan güncellemelerle o gün ve haftanın iş/blok durumunu takip etmeye karar verdik. 
![image](https://github.com/user-attachments/assets/57e7544f-1f6d-4feb-9eb2-ec5d712d62fa)
![image](https://github.com/user-attachments/assets/81b3ca94-5a01-4e22-8169-eaa12e13eea1)
![image](https://github.com/user-attachments/assets/8ac5e352-2c88-4a76-9f69-031fc43eeec8)

### Sprint Board
![image](https://github.com/user-attachments/assets/7daeae32-a1ba-46ac-a1cd-3ab0a81625f0)

### Ürün Durumu: Ekran Görüntüleri
#### Figma Tasarımları
![image](https://github.com/user-attachments/assets/6c5f983c-22aa-42b4-b804-0596e6a7eb19)
![image](https://github.com/user-attachments/assets/d297e0de-6c2e-4be7-ab51-5d5939475650)
![image](https://github.com/user-attachments/assets/3f896525-abeb-4fb0-a1a6-352624bb2cff)

### Sprint Review
User stories ve uygulamadan beklediklerimizi oturtmaya çalıştık. Oyunlaştırmayla ilgili çeşitli öğelerin eklenmesi tartışıldı. Şimdilik Scope dışı olduğuna karar verildi. Henüz ürün çıktımız olmadığı için sürece ve geleceğe odaklandık. 
### Sprint Retrospective
Sürece çok geç başladık ancak toplanabildiğimiz andan itibaren herkes aktif davrandı ve gayet çabuk karar alabildik. Daha sıkı çalışarak kaybolan zamanı telafi edebileceğimize karar verdik.
Her sprintin ilk pazartesi günü "Sprint Planning"'de bir araya gelip hedefleri kararlaştırmaya ve iş parçalarını birlikte puanlandıracağız. Paralel çalışabilmek için sorumluluklar kişi bazlı atanacak ve dailyler ile takip edilecek. Cuma günleri ürünün gelişimi değerlendirilecek ve 2. cumartesi Retrospective yapılacak.
## Sprint 2
- **Sprint Notları:**
Uygulamanın temel işlevselliğini oluşturuldu: vaka seçimi, hasta ile konuşma, laboratuvar sonuçları, ve yapay zeka entegrasyonunun.
- **Sprint İçinde Tamamlanması Tahmin Edilen Puan:** 25 story points
- **Puan Tamamlama Mantığı:**
  -  Ana sayfanın kullanıcıyı karşılaması                     1
  - Kullanıcının vaka listesinden vaka seçebilmesi            3
  - Kullanıcının hastayla basit konuşma gerçekleştirebilmesi  3
  - Laboratuvar testlerinin istenip sonuçlarının gösterilmesi 5
  - Streamlit ile çok sayfalı yapı kurulması                  3 
  - Gemini entegrasyonu ve prompt ile cevap üretilmesi        8 

- **Daily Scrum:** Dailyleri hem birkaç günde bir hem de haftalık özetler şeklinde trello ve whatsapp üzerinden gerçekleştirdik.
<img width="531" height="725" alt="image" src="https://github.com/user-attachments/assets/9c1ca4d3-5e60-4091-91bb-c12c6ed7a4ec" />
<img width="610" height="448" alt="image" src="https://github.com/user-attachments/assets/2c6f174a-1394-4476-b5a3-2ac59b7c8ba7" />
<img width="625" height="331" alt="image" src="https://github.com/user-attachments/assets/4ef55bfc-280c-4e35-a138-c943e53d8956" />
<img width="387" height="246" alt="image" src="https://github.com/user-attachments/assets/1b7f8fef-f085-49de-a578-73bb104f22ff" />
<img width="631" height="399" alt="image" src="https://github.com/user-attachments/assets/719b674a-854d-482b-9246-e39a376cdf3e" />

### Sprint Board
<img width="1424" height="668" alt="image" src="https://github.com/user-attachments/assets/a696c867-7604-4816-8119-cab5783d7608" />

### Ürün Durumu: Ekran Görüntüleri
<img width="507" height="772" alt="image" src="https://github.com/user-attachments/assets/3a7c732f-6db5-4235-85da-f0efca7659fe" />
<img width="795" height="305" alt="image" src="https://github.com/user-attachments/assets/b8abc9f1-a860-45fa-9b87-66b42be32707" />
<img width="1059" height="507" alt="image" src="https://github.com/user-attachments/assets/8e892477-2374-446d-91a5-aeb2fa8a0231" />
<img width="831" height="481" alt="image" src="https://github.com/user-attachments/assets/81985c4a-db37-409a-b087-13620e7c551c" />

### Sprint Review
Streamlit tercih edilerek temel fonksiyonlar gerçeklendi, kullanıcı etkileşimli temel yapılar hızlı kuruldu. Gemini entegre yapay hasta deneyimi başarılı oldu feature olarak sesli sohbet özelliği ön planda ancak öncelikle teknik hatalara ve vaka sayısı ve çeşidine odaklanılacak. 

Tanı gönderme bölümünde hatalar var, geribildirim bölümü ise henüz tamamlanmadı. Gemini kotasıyla ilgili bazı hatalar süreci yavaşlattı. Bu noktada hangi Gemini modelini seçeceğimiz, prompt tasarımını ne kadar detaylı yapacağımız konusunda deneme yanılma yonulma yoluyla çok şey öğrendik. Ayrıca geliştirme ortamıyla ilgili yaşadığınız sıkıntıların tekrar edilmemesi için bir kurulum rehberi yazılmasına karar verdik.

Vakaları ne şekilde sunacağımız en önemli toplantı konularımızdan biriydi. Kullanıcı kitlesine daha faydalı bir ürün olması için Poliklinik bölümlerine göre kategorileri ayırmaya ve her bölüm için en az bir vaka sunmaya karar verdik.

### Sprint Retrospective
Okul ve iş yoğunlukları Backlogun birikmesine sebep oluyor. Storyleri belirlerken daha dikkatli olmalıyız.
Bir önceki Sprinte göre daha yakın iletişimde kaldığımız bir süreç yönettik ve bu çıktıyı da olumlu etkiledi. Streamlit yapısı çok hızlı kuruldu. Kullanıcı deneyimi netleşti. Gemini modeli başarıyla entegre edildi.

Toplantı sıklıklarının ani bir gelişme olmadığı sürece aynı kalmasına karar verildi.
Weekly özetlerinin daha aktif kullanılmasına karar verildi.
## Sprint 3
- **Sprint Notları:** Eklenen özellikelr ile birlikte çok daha bütüncül hissetiriyor. Geribildirim ve tanı kontrol fonksiyonlarında ince ayarlar gerekli. Kota ve hızla ilgili sorunlar süreci yavaşlattı. Branchleri merge etmeden önce çok beklememiz conflictlerle daha fazla uğraşmamıza sebep oldu.
  
- **Sprint İçinde Tamamlanması Tahmin Edilen Puan:** 29 story points
- **Puan Tamamlama Mantığı:**
  -  AI geri bildirimi     5
  - Klinik skor            5
  - Sesli yanıt            3
  - Login sistemi          8
  - Veri tabanı taşıma     3 
  - Vaka sınıflandırması   3
- **Daily Scrum:**
<img width="617" height="273" alt="image" src="https://github.com/user-attachments/assets/cd7a29d6-73f7-4149-8312-d5a451baa833" />
<img width="503" height="122" alt="image" src="https://github.com/user-attachments/assets/124f3a3d-90f6-4346-a099-d7ff49971b49" />
<img width="611" height="367" alt="image" src="https://github.com/user-attachments/assets/4d8bcd57-86e1-4c19-af7a-74478cd56088" />

### Sprint Board
<img width="1129" height="641" alt="image" src="https://github.com/user-attachments/assets/84edd2cf-0e35-4753-82bf-2309619547af" />

### Ürün Durumu: Ekran Görüntüleri
<img width="935" height="780" alt="image" src="https://github.com/user-attachments/assets/478806f6-01c3-446f-bbb2-b82f4292d29f" />
<img width="740" height="797" alt="image" src="https://github.com/user-attachments/assets/753eb8bb-724a-4499-aa28-a95d34e43538" />
<img width="751" height="295" alt="image" src="https://github.com/user-attachments/assets/edc22988-1045-4103-8575-54c6b7e08145" />
<img width="760" height="308" alt="image" src="https://github.com/user-attachments/assets/4c13bd6c-97af-4e1e-aa43-32d169010183" />

### Sprint Review

Tanı verildikten sonra yapay zeka, geri bildirim ve puanlama yapabiliyor. 

Klinik sorgulama kalitesi, tanının doğruluğu ve alınan testler de analiz ediliyor. 

Supabase ile veriler kalıcı olarak kaydedilmeye başlandı. 

Sesli okuma ve sesli giriş sayesinde etkileşim doğallaştırıldı. 

Giriş yapmayan kullanıcılar engelleniyor; kullanıcı oturumu destekleniyor.
### Sprint Retrospective
Yapay zekanın geri bildirim kalitesi beklentilerin üstünde.

Supabase kayıt sistemi çok zorlamadı.

Sesli girdi için doğal hissettiren bir çözüm bulmakta zorlandık.

Vaka çeşidi memnun edici.

Yeni fonksiyonlar üzerinde çok zaman harcadığımız için kullanıcı deneyimine yeterince odaklanamadık.
