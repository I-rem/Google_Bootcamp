import streamlit as st
import os
import unicodedata # Türkçe karakterleri dönüştürmek için
import re # Regex işlemleri için

st.title("📋 Vaka Seçimi")

# Vakaları bölümlere göre gruplandırılmış olarak tanımla 
cases_by_department = {
    "Genel Cerrahi": [
        {
            "id": 1,
            "age": 25,
            "gender": "Kadın",
            "complaint": "Karın ağrısı",
            "history": "Hasta 2 gündür süren sağ alt kadran ağrısı şikayetiyle başvurmuş.",
            "symptoms": ["bulantı", "iştahsızlık", "ateş"],
            "lab_results": {
                "Tam Kan Sayımı": "Hb: 13.5, WBC: 14.2 (↑), PLT: 250k",
                "CRP": "48 mg/L (↑)",
                "USG": "Appendiks çapı > 6mm, çevresel ödem",
            },
            "diagnosis": "Akut apandisit",
        },
        {
            "id": 2,
            "age": 60,
            "gender": "Erkek",
            "complaint": "Göğüs ağrısı",
            "history": "Aniden başlayan, sol kola yayılan göğüs ağrısı. Hipertansiyon öyküsü var.",
            "symptoms": ["terleme", "nefes darlığı", "bulantı"],
            "lab_results": {
                "EKG": "ST elevasyonu V2-V4",
                "Troponin": "Pozitif",
                "EKO": "Anteriyor hipokinezi",
            },
            "diagnosis": "ST elevasyonlu miyokard enfarktüsü (STEMI)",
        },
        {
            "id": 3,
            "age": 40,
            "gender": "Kadın",
            "complaint": "Sağ üst kadran ağrısı",
            "history": "Yağlı yemek sonrası başlayan, sırta vuran ağrı şikayetiyle başvurdu.",
            "symptoms": ["bulantı", "kusma"],
            "lab_results": {
                "USG": "Safra kesesinde taşlar, duvar kalınlaşması",
                "Karaciğer Fonksiyon Testleri": "Normal",
            },
            "diagnosis": "Akut kolesistit",
        },
        {
            "id": 4,
            "age": 55,
            "gender": "Erkek",
            "complaint": "Rektal kanama",
            "history": "Hasta son 3 aydır aralıklı rektal kanama ve dışkılama alışkanlığında değişiklik şikayetleriyle başvurmuş.",
            "symptoms": ["kilo kaybı", "kabızlık/ishal nöbetleri"],
            "lab_results": {
                "Kolonoskopi": "Rektumda polipoid kitle",
                "Biyopsi": "Adenokarsinom",
            },
            "diagnosis": "Kolorektal Kanser",
        },
        {
            "id": 5,
            "age": 35,
            "gender": "Erkek",
            "complaint": "Kasıkta şişlik",
            "history": "Hasta 6 aydır sağ kasıkta özellikle ayakta durunca veya öksürünce belirginleşen şişlik şikayetiyle başvurmuş.",
            "symptoms": ["ağrı", "rahatsızlık"],
            "lab_results": {
                "Fizik Muayene": "Sağ inguinal bölgede redükte edilebilir şişlik",
            },
            "diagnosis": "İnguinal Herni",
        },
    ],
    "Nöroloji": [
        {
            "id": 101,
            "age": 45,
            "gender": "Kadın",
            "complaint": "Baş ağrısı ve görme bozukluğu",
            "history": "Hasta 1 haftadır süren şiddetli baş ağrısı, çift görme ve sol gözde bulanık görme şikayetleriyle başvurmuş. Daha önce benzer şikayeti olmamış.",
            "symptoms": ["bulantı", "kusma", "fotofobi"],
            "lab_results": {
                "Beyin MRG": "Sella bölgesinde kitle lezyonu",
                "Görüş Alanı Testi": "Bitemporal hemianopsi",
            },
            "diagnosis": "Hipofiz adenomu",
        },
        {
            "id": 102,
            "age": 70,
            "gender": "Erkek",
            "complaint": "Konuşma güçlüğü ve sağ tarafta güçsüzlük",
            "history": "Hasta sabah uyandığında aniden başlayan konuşma güçlüğü ve sağ kol ve bacakta güçsüzlük fark etmiş.",
            "symptoms": ["yüzde düşme", "denge kaybı"],
            "lab_results": {
                "Beyin BT": "Sol serebral hemisferde iskemik alan",
                "Karotis USG": "Sol karotis arterde %80 stenoz",
            },
            "diagnosis": "İskemik inme",
        },
        {
            "id": 103,
            "age": 30,
            "gender": "Kadın",
            "complaint": "Vücudun çeşitli yerlerinde uyuşma ve güçsüzlük",
            "history": "Hasta son 3 aydır aralıklı olarak sağ bacakta güçsüzlük, sol kolda uyuşma ve görme bulanıklığı şikayetleriyle başvurmuş.",
            "symptoms": ["yorgunluk", "denge bozukluğu"],
            "lab_results": {
                "Beyin ve Spinal MRG": "Demiyelinizan plaklar",
                "LP (Lomber Ponksiyon)": "Oligoklonal bantlar pozitif",
            },
            "diagnosis": "Multipl Skleroz (MS)",
        },
        {
            "id": 104,
            "age": 20,
            "gender": "Erkek",
            "complaint": "Tekrarlayan kas seğirmeleri ve kas krampları",
            "history": "Hasta 1 yıldır tekrarlayan kas seğirmeleri, güçsüzlük ve kas krampları şikayetleriyle başvurmuş. Yutma güçlüğü de başlamış.",
            "symptoms": ["konuşma bozukluğu", "kilo kaybı"],
            "lab_results": {
                "EMG": "Yaygın denervasyon ve reinervasyon bulguları",
                "Kas Biyopsisi": "Normal",
            },
            "diagnosis": "Amiyotrofik Lateral Skleroz (ALS)",
        },
        {
            "id": 105,
            "age": 68,
            "gender": "Kadın",
            "complaint": "Ellerde titreme ve hareketlerde yavaşlama",
            "history": "Hasta son 2 yıldır sağ elinde istirahat tremoru, hareketlerde yavaşlama ve denge bozukluğu şikayetleriyle başvurmuş.",
            "symptoms": ["yüzde maske ifadesi", "yürüyüş bozukluğu"],
            "lab_results": {
                "Beyin MRG": "Normal",
                "Dopamin Transporter SPECT (DaTscan)": "Dopaminerjik nöron kaybı ile uyumlu",
            },
            "diagnosis": "Parkinson Hastalığı",
        },
    ],
    "Kadın Doğum": [
        {
            "id": 201,
            "age": 30,
            "gender": "Kadın",
            "complaint": "Vajinal kanama ve karın ağrısı",
            "history": "Hasta 8 haftalık gebe. Son 2 gündür hafif vajinal kanama ve alt karın bölgesinde kramp tarzı ağrıları var.",
            "symptoms": ["adet gecikmesi", "halsizlik"],
            "lab_results": {
                "Beta-hCG": "Beklenenden düşük değerler ve artışta yavaşlama",
                "Pelvik USG": "İntrauterin gebelik kesesi izlenmedi, sağ adneksiyel bölgede kitle",
            },
            "diagnosis": "Ektopik gebelik",
        },
        {
            "id": 202,
            "age": 28,
            "gender": "Kadın",
            "complaint": "Düzensiz adet kanamaları",
            "history": "Hasta ergenliğinden beri düzensiz adet kanamaları, kilo alma ve yüzde tüylenme şikayetleriyle başvurmuş.",
            "symptoms": ["akne", "saç dökülmesi"],
            "lab_results": {
                "Hormon Paneli": "LH/FSH oranı yüksek, testosteron yüksek",
                "Pelvik USG": "Overlerde multiple küçük kistler",
            },
            "diagnosis": "Polikistik Over Sendromu (PKOS)",
        },
        {
            "id": 203,
            "age": 35,
            "gender": "Kadın",
            "complaint": "Aşırı adet kanaması ve kasık ağrısı",
            "history": "Hasta son 6 aydır aşırı miktarda ve uzun süren adet kanamaları, kasık ağrısı ve kansızlık şikayetleriyle başvurmuş.",
            "symptoms": ["yorgunluk", "halsizlik"],
            "lab_results": {
                "Pelvik USG": "Uterusta intramural myom",
                "Tam Kan Sayımı": "Hb: 8.0 (↓)",
            },
            "diagnosis": "Uterin Myom",
        },
        {
            "id": 204,
            "age": 22,
            "gender": "Kadın",
            "complaint": "Vajinal akıntı ve kaşıntı",
            "history": "Hasta son 3 gündür artan, kötü kokulu, yeşilimsi vajinal akıntı ve şiddetli kaşıntı şikayetleriyle başvurmuş.",
            "symptoms": ["yanma", "ilişki sırasında ağrı"],
            "lab_results": {
                "Vajinal Akıntı Mikroskopisi": "Trichomonas vaginalis",
            },
            "diagnosis": "Trichomoniasis",
        },
        {
            "id": 205,
            "age": 42,
            "gender": "Kadın",
            "complaint": "Menopoz semptomları",
            "history": "Hasta son 1 yıldır adet düzensizlikleri, sıcak basmaları, gece terlemeleri ve uyku sorunları şikayetleriyle başvurmuş.",
            "symptoms": ["sinirlilik", "vajinal kuruluk"],
            "lab_results": {
                "Hormon Paneli": "FSH yüksek, Estradiol düşük",
            },
            "diagnosis": "Menopoz",
        },
    ],
    "Dahiliye (İç Hastalıkları)": [
        {
            "id": 301,
            "age": 50,
            "gender": "Erkek",
            "complaint": "Aşırı susuzluk ve sık idrara çıkma",
            "history": "Hasta son birkaç aydır aşırı susuzluk, sık idrara çıkma ve kilo kaybı şikayetleriyle başvurmuş. Ailede diyabet öyküsü var.",
            "symptoms": ["yorgunluk", "bulanık görme"],
            "lab_results": {
                "Açlık Kan Şekeri": "250 mg/dL (↑)",
                "HbA1c": "9.5% (↑)",
                "İdrar Tahlili": "Glikoz pozitif",
            },
            "diagnosis": "Tip 2 Diyabetes Mellitus",
        },
        {
            "id": 302,
            "age": 65,
            "gender": "Kadın",
            "complaint": "Nefes darlığı ve bacaklarda şişlik",
            "history": "Hasta son 1 aydır artan nefes darlığı, özellikle geceleri ve bacaklarda şişlik şikayetleriyle başvurmuş. Hipertansiyon ve koroner arter hastalığı öyküsü var.",
            "symptoms": ["öksürük", "çarpıntı"],
            "lab_results": {
                "Akciğer Grafisi": "Kardiyomegali, pulmoner konjesyon",
                "EKO": "Sol ventrikül ejeksiyon fraksiyonu düşük",
                "BNP": "Yüksek",
            },
            "diagnosis": "Konjestif Kalp Yetmezliği",
        },
        {
            "id": 303,
            "age": 45,
            "gender": "Erkek",
            "complaint": "Sarılık ve karın ağrısı",
            "history": "Hasta son 2 haftadır gözlerinde ve cildinde sarılık, koyu renkli idrar ve sağ üst karın ağrısı şikayetleriyle başvurmuş. Alkol kullanımı öyküsü var.",
            "symptoms": ["iştahsızlık", "bulantı"],
            "lab_results": {
                "Karaciğer Fonksiyon Testleri": "Bilirubinler (↑↑), ALT, AST (↑)",
                "Batın USG": "Karaciğerde siroz bulguları",
            },
            "diagnosis": "Alkolik Hepatit",
        },
        {
            "id": 304,
            "age": 30,
            "gender": "Kadın",
            "complaint": "Yorgunluk ve kilo alma",
            "history": "Hasta son 6 aydır sürekli yorgunluk, kilo alma, üşüme ve saç dökülmesi şikayetleriyle başvurmuş.",
            "symptoms": ["kabızlık", "cilt kuruluğu"],
            "lab_results": {
                "Tiroid Fonksiyon Testleri": "TSH yüksek, Serbest T4 düşük",
                "Tiroid USG": "Tiroid bezinde diffüz büyüme",
            },
            "diagnosis": "Hipotiroidi (Hashimoto Tiroiditi)",
        },
        {
            "id": 305,
            "age": 70,
            "gender": "Erkek",
            "complaint": "Ateş, öksürük ve nefes darlığı",
            "history": "Hasta son 3 gündür yüksek ateş, balgamlı öksürük ve artan nefes darlığı şikayetleriyle başvurmuş. KOAH öyküsü var.",
            "symptoms": ["göğüs ağrısı", "titreme"],
            "lab_results": {
                "Akciğer Grafisi": "Sağ alt lobda konsolidasyon",
                "CRP": "120 mg/L (↑↑)",
                "Kan Kültürü": "Pozitif (Streptococcus pneumoniae)",
            },
            "diagnosis": "Pnömoni",
        },
    ],
    "Kardiyoloji": [
        {
            "id": 401,
            "age": 55,
            "gender": "Erkek",
            "complaint": "Göğüs ağrısı ve nefes darlığı",
            "history": "Hasta eforla artan, sol kola yayılan göğüs ağrısı ve nefes darlığı şikayetiyle başvurmuş. Sigara öyküsü var.",
            "symptoms": ["çarpıntı", "yorgunluk"],
            "lab_results": {
                "EKG": "ST depresyonu",
                "Efor Testi": "Pozitif",
                "Koroner Anjiyografi": "Üç damar hastalığı",
            },
            "diagnosis": "Koroner arter hastalığı",
        },
        {
            "id": 402,
            "age": 40,
            "gender": "Kadın",
            "complaint": "Çarpıntı ve bayılma hissi",
            "history": "Hasta son 6 aydır aralıklı çarpıntı, göğüste sıkışma ve bayılma hissi şikayetleriyle başvurmuş. Ailede ani ölüm öyküsü var.",
            "symptoms": ["nefes darlığı", "baş dönmesi"],
            "lab_results": {
                "EKG": "Uzun QT sendromu",
                "Holter EKG": "Ventriküler taşikardi atakları",
            },
            "diagnosis": "Uzun QT Sendromu",
        },
        {
            "id": 403,
            "age": 75,
            "gender": "Erkek",
            "complaint": "Ayak bileklerinde şişlik ve nefes darlığı",
            "history": "Hasta son 3 aydır artan ayak bileklerinde şişlik, eforla artan nefes darlığı ve gece öksürüğü şikayetleriyle başvurmuş. Daha önce kalp krizi geçirmiş.",
            "symptoms": ["yorgunluk", "iştahsızlık"],
            "lab_results": {
                "EKO": "Sol ventrikül disfonksiyonu, ejeksiyon fraksiyonu %30",
                "Akciğer Grafisi": "Kardiyomegali, pulmoner ödem",
            },
            "diagnosis": "Kronik Kalp Yetmezliği",
        },
        {
            "id": 404,
            "age": 30,
            "gender": "Kadın",
            "complaint": "Baş dönmesi ve çarpıntı",
            "history": "Hasta ani başlayan baş dönmesi, çarpıntı ve göğüste rahatsızlık hissi şikayetleriyle acile başvurmuş. Daha önce benzer atakları olmuş.",
            "symptoms": ["terleme", "nefes darlığı"],
            "lab_results": {
                "EKG": "Supraventriküler taşikardi (SVT)",
            },
            "diagnosis": "Paroksismal Supraventriküler Taşikardi (PSVT)",
        },
        {
            "id": 405,
            "age": 60,
            "gender": "Erkek",
            "complaint": "Bacaklarda ağrı ve yürüme güçlüğü",
            "history": "Hasta son 6 aydır özellikle yürürken bacaklarında ağrı ve kramp şikayetleriyle başvurmuş. Dinlenince ağrı geçiyor. Sigara öyküsü var.",
            "symptoms": ["ayaklarda soğukluk", "ciltte solukluk"],
            "lab_results": {
                "Doppler USG": "Periferik arterlerde stenoz",
                "Ankle-Brakial İndeks (ABI)": "Düşük",
            },
            "diagnosis": "Periferik Arter Hastalığı",
        },
    ],
    "Ortopedi ve Travmatoloji": [
        {
            "id": 501,
            "age": 30,
            "gender": "Erkek",
            "complaint": "Diz ağrısı ve şişlik",
            "history": "Futbol oynarken dizine darbe alması sonucu ani başlayan ağrı ve şişlik şikayetiyle başvurmuş. Dizde kilitlenme hissi var.",
            "symptoms": ["hareket kısıtlılığı", "ses gelmesi"],
            "lab_results": {
                "Diz MRG": "Ön çapraz bağ rüptürü, menisküs yırtığı",
                "Röntgen": "Normal",
            },
            "diagnosis": "Ön Çapraz Bağ Yaralanması ve Menisküs Yırtığı",
        },
        {
            "id": 502,
            "age": 65,
            "gender": "Kadın",
            "complaint": "Kalça ağrısı ve yürüme güçlüğü",
            "history": "Hasta son 1 yıldır artan sağ kalça ağrısı ve yürüme güçlüğü şikayetiyle başvurmuş. Özellikle sabahları tutukluk oluyor.",
            "symptoms": ["topallama", "hareket kısıtlılığı"],
            "lab_results": {
                "Kalça Röntgeni": "Eklem aralığında daralma, osteofitler",
            },
            "diagnosis": "Kalça Osteoartriti",
        },
        {
            "id": 503,
            "age": 20,
            "gender": "Erkek",
            "complaint": "Omuz ağrısı ve hareket kısıtlılığı",
            "history": "Ağırlık kaldırırken ani başlayan omuz ağrısı ve kolunu yukarı kaldıramama şikayetiyle başvurmuş.",
            "symptoms": ["güçsüzlük", "gece ağrısı"],
            "lab_results": {
                "Omuz MRG": "Rotator manşet yırtığı",
            },
            "diagnosis": "Rotator Manşet Yırtığı",
        },
        {
            "id": 504,
            "age": 45,
            "gender": "Kadın",
            "complaint": "El bileği ağrısı ve uyuşma",
            "history": "Hasta son 3 aydır özellikle geceleri artan sağ el bileğinde ağrı, ilk üç parmakta uyuşma ve karıncalanma şikayetleriyle başvurmuş. Daktilo kullanıyor.",
            "symptoms": ["güçsüzlük", "cisimleri düşürme"],
            "lab_results": {
                "EMG/NCS": "Karpal Tünel Sendromu",
            },
            "diagnosis": "Karpal Tünel Sendromu",
        },
        {
            "id": 505,
            "age": 10,
            "gender": "Erkek",
            "complaint": "Ayak bileği burkulması",
            "history": "Basketbol oynarken ayağını burkması sonucu ani başlayan ağrı ve şişlik şikayetiyle acile başvurmuş.",
            "symptoms": ["morarma", "yürüme güçlüğü"],
            "lab_results": {
                "Ayak Bileği Röntgeni": "Kırık yok",
            },
            "diagnosis": "Ayak Bileği Burkulması (Ligament Yaralanması)",
        },
    ],
    "Dermatoloji": [
        {
            "id": 601,
            "age": 25,
            "gender": "Kadın",
            "complaint": "Yüzde ve sırtta sivilceler",
            "history": "Hasta ergenliğinden beri devam eden yüzde ve sırtta kırmızı, iltihaplı sivilceler şikayetiyle başvurmuş. Özgüvenini etkiliyor.",
            "symptoms": ["siyah noktalar", "yağlı cilt"],
            "lab_results": {},
            "diagnosis": "Akne Vulgaris",
        },
        {
            "id": 602,
            "age": 50,
            "gender": "Erkek",
            "complaint": "Vücutta kaşıntılı kırmızı lekeler",
            "history": "Hasta son 6 aydır vücudunun çeşitli yerlerinde özellikle dirseklerde ve dizlerde kaşıntılı, kırmızı, pullu lekeler şikayetiyle başvurmuş. Stresle artıyor.",
            "symptoms": ["tırnak değişiklikleri", "eklem ağrısı"],
            "lab_results": {
                "Deri Biyopsisi": "Psoriatik değişiklikler",
            },
            "diagnosis": "Psoriasis (Sedef Hastalığı)",
        },
        {
            "id": 603,
            "age": 8,
            "gender": "Kız",
            "complaint": "Vücutta kaşıntılı kabarcıklar",
            "history": "Çocuğun son 2 gündür vücudunda özellikle koltuk altı ve parmak aralarında şiddetli kaşıntılı, küçük kırmızı kabarcıklar ve tüneller şikayetiyle başvurulmuş. Aile bireylerinde de benzer şikayetler var.",
            "symptoms": ["gece kaşıntısı"],
            "lab_results": {
                "Deri Kazıntısı Mikroskopisi": "Sarcoptes scabiei (uyuz böceği)",
            },
            "diagnosis": "Skabiyez (Uyuz)",
        },
        {
            "id": 604,
            "age": 35,
            "gender": "Kadın",
            "complaint": "Güneş sonrası yüzde kızarıklık ve döküntü",
            "history": "Hasta güneşe maruz kaldıktan sonra yüzünde ve dekolte bölgesinde kızarıklık, küçük kabarcıklar ve kaşıntı şikayetiyle başvurmuş.",
            "symptoms": ["yanma hissi"],
            "lab_results": {},
            "diagnosis": "Polimorf Işık Erüpsiyonu",
        },
        {
            "id": 605,
            "age": 60,
            "gender": "Erkek",
            "complaint": "Ayakta tırnak kalınlaşması ve renk değişikliği",
            "history": "Hasta uzun süredir ayak tırnaklarında kalınlaşma, sararma ve kırılganlık şikayetiyle başvurmuş. Ayakkabı giyerken rahatsızlık duyuyor.",
            "symptoms": ["koku"],
            "lab_results": {
                "Tırnak Mantar Kültürü": "Pozitif (Dermatofit)",
            },
            "diagnosis": "Onikomikozis (Tırnak Mantarı)",
        },
    ],
    "Göz Hastalıkları": [
        {
            "id": 701,
            "age": 70,
            "gender": "Kadın",
            "complaint": "Bulanık görme ve ışık hassasiyeti",
            "history": "Hasta son 1 yıldır özellikle geceleri artan bulanık görme, ışık hassasiyeti ve renklerde soluklaşma şikayetleriyle başvurmuş.",
            "symptoms": ["çift görme", "hızlı gözlük değişimi ihtiyacı"],
            "lab_results": {
                "Göz Muayenesi": "Lenslerde opasite (katarakt)",
            },
            "diagnosis": "Katarakt",
        },
        {
            "id": 702,
            "age": 55,
            "gender": "Erkek",
            "complaint": "Gözde kızarıklık ve ağrı",
            "history": "Hasta ani başlayan sol gözde şiddetli ağrı, kızarıklık, bulanık görme ve ışık etrafında haleler görme şikayetiyle acile başvurmuş.",
            "symptoms": ["bulantı", "kusma"],
            "lab_results": {
                "Göz Tansiyonu Ölçümü": "Sol gözde yüksek intraoküler basınç (45 mmHg)",
            },
            "diagnosis": "Akut Açı Kapanması Glokomu",
        },
        {
            "id": 703,
            "age": 10,
            "gender": "Kız",
            "complaint": "Uzağı görememe",
            "history": "Çocuğun okulda tahtayı görmekte zorlandığı, gözlerini kısarak baktığı fark edilmiş. Baş ağrısı şikayeti de var.",
            "symptoms": ["göz yorgunluğu"],
            "lab_results": {
                "Görme Keskinliği Testi": "Uzak görmede azalma",
                "Refraksiyon": "Miyopi",
            },
            "diagnosis": "Miyopi (Uzağı Görememe)",
        },
        {
            "id": 704,
            "age": 60,
            "gender": "Kadın",
            "complaint": "Merkezi görmede bozulma",
            "history": "Hasta son 6 aydır özellikle okurken ve yüzleri tanırken zorlanma, merkezi görme alanında bulanıklık veya çarpıklık şikayetiyle başvurmuş. Sigara öyküsü var.",
            "symptoms": ["düz çizgilerin dalgalı görünmesi"],
            "lab_results": {
                "Oftalmoskopi": "Makulada drusen ve pigment değişiklikleri",
                "OCT (Optik Koherens Tomografi)": "Makulada atrofi",
            },
            "diagnosis": "Yaşa Bağlı Makula Dejenerasyonu (Kuru Tip)",
        },
        {
            "id": 705,
            "age": 30,
            "gender": "Erkek",
            "complaint": "Gözde batma, yanma ve kuruluk hissi",
            "history": "Hasta uzun saatler bilgisayar başında çalışıyor. Son 3 aydır gözlerinde batma, yanma, kızarıklık ve kuruluk hissi şikayetleriyle başvurmuş.",
            "symptoms": ["yabancı cisim hissi", "bulanık görme"],
            "lab_results": {
                "Schirmer Testi": "Göz yaşı salgısında azalma",
            },
            "diagnosis": "Kuru Göz Sendromu",
        },
    ],
    "Kulak Burun Boğaz (KBB)": [
        {
            "id": 801,
            "age": 7,
            "gender": "Erkek",
            "complaint": "Tekrarlayan kulak enfeksiyonları ve işitme kaybı",
            "history": "Çocuğun son 1 yıldır sık sık orta kulak enfeksiyonu geçirdiği ve işitmesinde azalma olduğu fark edilmiş. Geniz eti büyüklüğü öyküsü var.",
            "symptoms": ["burun tıkanıklığı", "horlama"],
            "lab_results": {
                "Otoskopi": "Timpanik membranda retraksiyon ve sıvı",
                "Timpanogram": "Tip B eğrisi",
            },
            "diagnosis": "Seröz Otitis Media (Kulakta Sıvı Birikimi)",
        },
        {
            "id": 802,
            "age": 40,
            "gender": "Kadın",
            "complaint": "Ses kısıklığı",
            "history": "Hasta son 3 aydır devam eden ses kısıklığı şikayetiyle başvurmuş. Şarkı söylüyor ve çok konuşuyor.",
            "symptoms": ["boğazda kuruluk", "ses yorgunluğu"],
            "lab_results": {
                "Laringoskopi": "Vokal kord nodülleri",
            },
            "diagnosis": "Vokal Kord Nodülleri (Şarkıcı Nodülü)",
        },
        {
            "id": 803,
            "age": 55,
            "gender": "Erkek",
            "complaint": "Burun tıkanıklığı ve horlama",
            "history": "Hasta uzun süredir devam eden burun tıkanıklığı, özellikle geceleri artan horlama ve ağız kuruluğu şikayetleriyle başvurmuş.",
            "symptoms": ["uyku apnesi", "gündüz yorgunluğu"],
            "lab_results": {
                "Nazal Endoskopi": "Nazal septum deviasyonu, konka hipertrofisi",
            },
            "diagnosis": "Nazal Septum Deviasyonu ve Konka Hipertrofisi",
        },
        {
            "id": 804,
            "age": 30,
            "gender": "Kadın",
            "complaint": "Baş dönmesi ve kulak çınlaması",
            "history": "Hasta ani başlayan, tekrarlayan şiddetli baş dönmesi atakları, kulakta çınlama, işitme kaybı ve dolgunluk hissi şikayetleriyle başvurmuş.",
            "symptoms": ["bulantı", "kusma"],
            "lab_results": {
                "Odyometri": "Tek taraflı sensörinöral işitme kaybı",
                "VNG (Videonistagmografi)": "Vestibüler disfonksiyon",
            },
            "diagnosis": "Meniere Hastalığı",
        },
        {
            "id": 805,
            "age": 25,
            "gender": "Erkek",
            "complaint": "Boğaz ağrısı ve yutma güçlüğü",
            "history": "Hasta son 3 gündür şiddetli boğaz ağrısı, yutma güçlüğü, ateş ve boyununda şişlik şikayetleriyle başvurmuş.",
            "symptoms": ["halsizlik", "bademciklerde beyazlık"],
            "lab_results": {
                "Boğaz Kültürü": "Streptococcus pyogenes",
            },
            "diagnosis": "Akut Tonsillit (Beta Hemolitik Streptokok)",
        },
    ],
    "Üroloji": [
        {
            "id": 901,
            "age": 60,
            "gender": "Erkek",
            "complaint": "Sık idrara çıkma ve idrar yapmada zorlanma",
            "history": "Hasta son 6 aydır sık idrara çıkma, gece idrara kalkma, idrar akışında zayıflama ve tam boşaltamama hissi şikayetleriyle başvurmuş.",
            "symptoms": ["damlama", "ani idrar hissi"],
            "lab_results": {
                "PSA": "Yüksek (10 ng/mL)",
                "Üroflowmetri": "Düşük akış hızı",
                "TRUS Biyopsi": "Prostat adenokarsinomu",
            },
            "diagnosis": "Prostat Kanseri",
        },
        {
            "id": 902,
            "age": 35,
            "gender": "Kadın",
            "complaint": "İdrar yaparken yanma ve sık idrara çıkma",
            "history": "Hasta ani başlayan idrar yaparken yanma, sık idrara çıkma ve alt karın ağrısı şikayetleriyle başvurmuş. Daha önce de benzer enfeksiyonlar geçirmiş.",
            "symptoms": ["bulanık idrar", "kötü kokulu idrar"],
            "lab_results": {
                "İdrar Tahlili": "Lökosit esteraz pozitif, nitrit pozitif",
                "İdrar Kültürü": "E. coli üremesi",
            },
            "diagnosis": "İdrar Yolu Enfeksiyonu (Sistit)",
        },
        {
            "id": 903,
            "age": 45,
            "gender": "Erkek",
            "complaint": "Şiddetli yan ağrısı",
            "history": "Hasta ani başlayan, sırta ve kasığa yayılan şiddetli yan ağrısı, bulantı ve kusma şikayetleriyle acile başvurmuş.",
            "symptoms": ["idrarda kan", "sık idrara çıkma"],
            "lab_results": {
                "Batın BT": "Sağ üreterde taş",
                "İdrar Tahlili": "Hematüri",
            },
            "diagnosis": "Üreter Taşı (Renal Kolik)",
        },
        {
            "id": 904,
            "age": 28,
            "gender": "Erkek",
            "complaint": "Testiste ağrı ve şişlik",
            "history": "Hasta son 2 gündür sol testiste ağrı, şişlik ve hassasiyet şikayetiyle başvurmuş. Ateşi de var.",
            "symptoms": ["idrar yaparken yanma"],
            "lab_results": {
                "Testis Doppler USG": "Sol epididimde inflamasyon bulguları",
                "İdrar Tahlili": "Normal",
            },
            "diagnosis": "Epididimit",
        },
        {
            "id": 905,
            "age": 70,
            "gender": "Kadın",
            "complaint": "İdrar kaçırma",
            "history": "Hasta öksürünce, hapşırınca veya gülerken istemsiz idrar kaçırma şikayetiyle başvurmuş. Birden fazla normal doğum öyküsü var.",
            "symptoms": ["ped kullanma ihtiyacı"],
            "lab_results": {
                "Ürodinamik Testler": "Stres inkontinansı",
            },
            "diagnosis": "Stres Üriner İnkontinans",
        },
    ],
    "Psikiyatri": [
        {
            "id": 1001,
            "age": 30,
            "gender": "Kadın",
            "complaint": "Sürekli endişe ve panik ataklar",
            "history": "Hasta son 6 aydır sürekli endişeli hissetme, uyku sorunları, kas gerginliği ve tekrarlayan panik ataklar şikayetleriyle başvurmuş. İş hayatında stresli bir dönemden geçiyor.",
            "symptoms": ["çarpıntı", "nefes darlığı", "ölüm korkusu"],
            "lab_results": {},
            "diagnosis": "Panik Bozukluk ve Yaygın Anksiyete Bozukluğu",
        },
        {
            "id": 1002,
            "age": 45,
            "gender": "Erkek",
            "complaint": "Depresif ruh hali ve ilgi kaybı",
            "history": "Hasta son 2 aydır sürekli mutsuz hissetme, daha önce zevk aldığı şeylere karşı ilgi kaybı, enerji düşüklüğü ve uyku/iştah değişiklikleri şikayetleriyle başvurmuş. İşini kaybetmiş.",
            "symptoms": ["konsantrasyon güçlüğü", "intihar düşünceleri"],
            "lab_results": {},
            "diagnosis": "Majör Depresif Bozukluk",
        },
        {
            "id": 1003,
            "age": 20,
            "gender": "Kadın",
            "complaint": "Tekrarlayan takıntılı düşünceler ve zorlantılı davranışlar",
            "history": "Hasta çocukluğundan beri temizlik konusunda aşırı takıntılı düşüncelere sahip olduğunu ve sürekli ellerini yıkama gibi zorlantılı davranışlar sergilediğini belirtiyor. Günlük hayatını etkiliyor.",
            "symptoms": ["kaygı", "zaman kaybı"],
            "lab_results": {},
            "diagnosis": "Obsesif Kompulsif Bozukluk (OKB)",
        },
        {
            "id": 1004,
            "age": 25,
            "gender": "Erkek",
            "complaint": "Gerçeklikten kopma ve şüphecilik",
            "history": "Hasta son 6 aydır başkalarının onu takip ettiğine dair paranoyak düşünceler, sesler duyma ve sosyal izolasyon şikayetleriyle başvurmuş. Kişisel hijyenine dikkat etmiyor.",
            "symptoms": ["konuşmada dağınıklık", "duygu küntlüğü"],
            "lab_results": {},
            "diagnosis": "Şizofreni",
        },
        {
            "id": 1005,
            "age": 35,
            "gender": "Kadın",
            "complaint": "Aşırı yeme atakları ve kilo alma",
            "history": "Hasta son 1 yıldır kontrolsüz aşırı yeme atakları geçirdiğini ve ardından suçluluk hissettiğini belirtiyor. Kilo alma endişesiyle sürekli diyet yapıyor ancak başarılı olamıyor.",
            "symptoms": ["vücut imajı sorunları", "depresyon"],
            "lab_results": {},
            "diagnosis": "Tıkınırcasına Yeme Bozukluğu",
        },
    ],
    "Çocuk Sağlığı ve Hastalıkları (Pediatri)": [
        {
            "id": 1101,
            "age": 2,
            "gender": "Erkek",
            "complaint": "Yüksek ateş ve döküntü",
            "history": "Çocuğun son 3 gündür yüksek ateşi olduğu, ardından vücudunda kırmızı, kaşıntılı döküntüler çıktığı belirtiliyor. Ailede suçiçeği öyküsü var.",
            "symptoms": ["halsizlik", "iştahsızlık"],
            "lab_results": {},
            "diagnosis": "Suçiçeği (Varisella)",
        },
        {
            "id": 1102,
            "age": 6,
            "gender": "Kız",
            "complaint": "Boğaz ağrısı ve ateş",
            "history": "Çocuğun son 2 gündür boğaz ağrısı, yutma güçlüğü ve ateş şikayetleriyle başvurulmuş. Okulda benzer vakalar var.",
            "symptoms": ["bademciklerde kızarıklık", "boyun lenf bezlerinde şişlik"],
            "lab_results": {
                "Boğaz Kültürü": "Streptococcus pyogenes",
            },
            "diagnosis": "Streptokoksik Farenjit",
        },
        {
            "id": 1103,
            "age": 1,
            "gender": "Kız",
            "complaint": "İshal ve kusma",
            "history": "Çocuğun son 1 gündür başlayan sık sulu ishal ve kusma şikayetleriyle başvurulmuş. Ateşi yok, ancak huzursuz ve iştahsız.",
            "symptoms": ["dehidrasyon belirtileri (ağız kuruluğu, gözlerde çökme)", "halsizlik"],
            "lab_results": {
                "Gaita Mikroskopisi": "Lökosit yok",
                "Gaita Kültürü": "Negatif",
            },
            "diagnosis": "Akut Gastroenterit (Viral)",
        },
        {
            "id": 1104,
            "age": 4,
            "gender": "Erkek",
            "complaint": "Nefes darlığı ve hırıltılı solunum",
            "history": "Çocuğun özellikle geceleri artan nefes darlığı, hırıltılı solunum ve öksürük şikayetleriyle başvurulmuş. Ailede astım öyküsü var.",
            "symptoms": ["göğüste sıkışma", "uyku bozukluğu"],
            "lab_results": {
                "Akciğer Grafisi": "Normal",
                "Solunum Fonksiyon Testleri": "Bronkodilatör sonrası düzelen obstrüksiyon",
            },
            "diagnosis": "Bronşiyal Astım",
        },
        {
            "id": 1105,
            "age": 9,
            "gender": "Kız",
            "complaint": "Karın ağrısı ve kabızlık",
            "history": "Çocuğun uzun süredir devam eden karın ağrısı ve haftada 2-3 kereden az dışkılama şikayetleriyle başvurulmuş. İştahsızlık ve kilo alamama da var.",
            "symptoms": ["şişkinlik", "dışkılama sırasında zorlanma"],
            "lab_results": {
                "Batın Röntgeni": "Kolonda gaita birikimi",
            },
            "diagnosis": "Fonksiyonel Kabızlık",
        },
    ],
}
# (cases_by_department sözlüğü yukarıdaki gibi devam ediyor)
# ...

# Fonksiyon: Bölüm adını dosya adı formatına çevirme
def slugify_department_name(department_name):
    # Parantez içindeki ifadeleri kaldır
    department_name = re.sub(r'\s*\(.*\)', '', department_name).strip()
    
    # Unicode karakterleri ASCII'ye çevir (örn: ç -> c, ö -> o)
    normalized_name = unicodedata.normalize('NFKD', department_name).encode('ascii', 'ignore').decode('utf-8')
    
    # Tüm harfleri küçük yap ve boşlukları alt çizgi ile değiştir
    slug = normalized_name.lower().replace(' ', '_')
    
    # Geçersiz karakterleri kaldır (sadece a-z, 0-9, _ kalır)
    slug = re.sub(r'[^a-z0-9_]', '', slug)
    
    return slug

st.markdown("### Bir Bölüm Seçin:")

# Her bölüm için resimli bir buton/kart oluşturma
num_cols = 4 # Her satırda kaç sütun olacağını belirle
cols = st.columns(num_cols)

# Session state'te seçili bölümü sakla
if "selected_department_card" not in st.session_state:
    st.session_state.selected_department_card = None

# Resimlerin bulunduğu klasör
ASSETS_DIR = "assets" 
# Resim uzantısı (tercihinize göre 'png' veya 'jpg' yapabilirsiniz)
IMAGE_EXTENSION = "png" 

for i, department_name in enumerate(cases_by_department.keys()):
    with cols[i % num_cols]: # Her bölümü kendi sütununa yerleştir
        # Bölüm adını dosya adı formatına çevir
        image_filename = f"{slugify_department_name(department_name)}.{IMAGE_EXTENSION}"
        image_path = os.path.join(ASSETS_DIR, image_filename)

        if os.path.exists(image_path): # Resim varsa ve yolu doğruysa
            st.image(image_path, caption=department_name, width=100)
        else:
            st.warning(f"Resim bulunamadı: '{image_filename}'. Varsayılan metin gösteriliyor.")
            st.write(department_name) # Resim yoksa sadece adı göster

        if st.button(f"Vakaları Gör", key=f"select_dept_{department_name}"):
            st.session_state.selected_department_card = department_name
            st.rerun() # Seçim yapıldığında sayfayı yeniden yükle

# Eğer bir bölüm seçilmişse, o bölümün vakalarını göster
if st.session_state.selected_department_card:
    selected_department_name = st.session_state.selected_department_card
    st.subheader(f"{selected_department_name} Bölümü Vakaları:")

    cases_in_department = cases_by_department[selected_department_name]
    
    # Create a list of case complaints to display in the selectbox
    case_complaints = [case["complaint"] for case in cases_in_department]
    
    # Select box for individual case
    # Varsayılan değeri, eğer daha önce bir vaka seçiliyse, o vaka olarak ayarla
    # Veya varsayılan olarak ilk vakayı seç
    default_case_index = 0
    if "selected_case" in st.session_state and st.session_state.selected_case in cases_in_department:
        # Eğer önceden seçili vaka varsa, onun index'ini bul
        try:
            default_case_index = case_complaints.index(st.session_state.selected_case["complaint"])
        except ValueError:
            default_case_index = 0 # Bulamazsa varsayılan
    
    selected_complaint = st.selectbox(
        "Bir vaka seçin:", 
        case_complaints, 
        index=default_case_index # Varsayılan seçimi ayarla
    )

    if selected_complaint:
        # Find the selected case
        selected_case = next(case for case in cases_in_department if case["complaint"] == selected_complaint)
        
        # Seçilen vakayı session state'e kaydet
        st.session_state.selected_case = selected_case

        # ---
        ## Vaka Detayları
        
        st.subheader(f"Vaka : {selected_case['id']} - {selected_case['complaint']}")

        # Using columns for better layout
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Yaş:** {selected_case['age']}")
            st.markdown(f"**Cinsiyet:** {selected_case['gender']}")
            st.markdown(f"**Şikayet:** {selected_case['complaint']}")
            st.markdown(f"**Öykü:** {selected_case['history']}")

       