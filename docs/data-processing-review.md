# Veri işleme ve yurt dışı aktarım incelemesi

İnceleme tarihi: 8 Ekim 2026. Bu belge, kamuya açık sağlayıcı koşulları ile
kodda uygulanan önlemleri kaydeder. Hesap sözleşmelerinin kabul edildiğini,
Türk standart sözleşmelerinin imzalandığını veya bildirim yapıldığını kanıtlamaz.
Hesap kanıtı olmayan satırlar açık kalır. İmzalı sözleşmeleri, hesap belgelerini,
imza yetkisi belgelerini ve anahtarları bu depoya yüklemeyin.

## Veri akışı ve uygulanan önlemler

Ziyaretçi formu → Vercel `/api/request-proposal` → Resend → işletme e-posta kutusu.
Formdaki kimlik, iletişim ve proje bilgileri teklif talebini yanıtlamak için kullanılır.
Site kodu ayrıca bir başvuru veritabanı oluşturmaz; bu, sağlayıcıların kayıt
tutmadığı anlamına gelmez. E-posta kutusu sağlayıcısı da ayrıca incelenmelidir.

- İşlev bölgesi `vercel.json` içinde `fra1` olarak seçildi. Canlı işlev bölgesi
  dağıtım ayrıntılarından doğrulanmalıdır. CDN, platform kayıtları, destek ve alt
  işleyenlerin tamamı için Almanya veya Türkiye veri yerleşimi garantisi değildir.
- Sunucu yalnız tanımlanmış alanları e-postaya koyar, alan ve istek boyutlarını
  sınırlar. Pasaport, kart veya sağlık bilgisi başlangıç formunda istenmez.
- Sayfa bağlamı site alan adıyla sınırlıdır; sorgu ve fragment bilgileri temizlenir.
  Zaman damgası sunucuda üretilir. Konu başlığı kişi ve şirket adını içermez.
- Uygulama hataları sağlayıcı yanıt gövdesini veya istisna mesajını kaydetmez.
  API yanıtları `no-store` kullanır; gönderim isteği 10 saniyede zaman aşımına uğrar.
- Analitik isteğe bağlıdır. Önceki çerez izni uygulaması ayrı olarak sürer;
  analitik izni düzenli yurt dışı aktarım güvencesinin yerine geçmez.

## Sağlayıcı koşulları ve hesapta doğrulanacak noktalar

| Sağlayıcı | Kamuya açık koşullar | Hesapta gereken kanıt ve durum |
| --- | --- | --- |
| Vercel | DPA Pro ve Enterprise işlemelerini kapsıyor; sözleşmeye girilmesi veya DPA'nın icrası ile bağlayıcı oluyor. Hobby ticari kullanım için uygun değil. | Aktif plan, proje sahibi tüzel kişi, geçerli sözleşme/DPA sürümü ve kabul kaydı henüz doğrulanmadı. |
| Vercel | Hobby ve deneme Pro için model eğitimi kullanılabilir; ücretli Pro varsayılanında kapalı. Team ayarlarından vazgeçilebiliyor. | Model eğitimi kapalı durumu, günlük saklama süresi, harici log drain alıcıları, erişim yetkileri ve dağıtım bölgesi henüz doğrulanmadı. |
| Resend | Plus Five Five, Inc. DPA'yı hizmet şartlarına dahil ediyor. Esas işleme ABD'de; DPA AB/Birleşik Krallık/İsviçre mekanizmaları içeriyor. | Gerçek hesap sahibi, hizmet şartları/DPA kabul kaydı, aktif plan ve Türkiye aktarımı için ayrıca uygun güvence henüz doğrulanmadı. |
| Resend | Yayımlanan Free/Pro/Scale e-posta ve log saklama süresi 30 gün; Enterprise esnek. | Hesaba uygulanan süre, yedekler, erken silme yöntemi ve sonraki alıcılar henüz doğrulanmadı. Gelen kutusu saklama süresi bundan bağımsızdır. |

Şirket hesabının `PMR TURİZM İNŞAAT TİCARET LİMİTED ŞİRKETİ` adına olduğu kontrol
edilmelidir; marka adı tek başına sözleşme tarafını doğrulamaz. Ticaret sicili ve
imza yetkisi ayrıca teyit edilmelidir. Plan yükseltme veya yeni abonelik yapılmadı.
Alt işleyen değişikliği bildirimlerinin alındığı da doğrulanmalıdır; Vercel DPA'sı
bildirim aboneliği için `privacy@vercel.com` ile iletişim kurulmasını öngörüyor.

Kaynaklar:

- [Vercel DPA](https://vercel.com/legal/dpa), §§1, 4, 7, 13; etkin tarih 31 Mart 2026.
- [Vercel hizmet şartları](https://vercel.com/legal/terms), §§3 ve 4.
- [Vercel işlev bölgesi yapılandırması](https://vercel.com/docs/functions/configuring-functions/region).
- [Resend DPA](https://resend.com/legal/dpa), giriş, §§4 ve 6.
- [Resend saklama ve GDPR açıklaması](https://resend.com/security/gdpr).
- [Resend alt işleyenleri](https://resend.com/legal/subprocessors).

## Türkiye'den düzenli aktarımın sözleşme incelemesi

KVKK m.9 bakımından veri işleme şartı ile yurt dışına aktarım güvencesi ayrı
değerlendirilir. Kurumun sayfası inceleme tarihinde yeterli koruma bulunan ülkeler
için henüz belirleme yapılmadığını bildiriyor. AB SCC veya GDPR DPA'sı tek başına
Türkiye standart sözleşmesinin imzalandığını kanıtlamaz. Rutin hosting ve e-posta
akışı, arızi aktarım istisnasıyla veya genel bir onay kutusuyla kapatılmamalıdır.

Şirketin veri sorumlusu, sağlayıcının veri işleyen olduğu bu akış için Standart
Sözleşme 2 değerlendirilmelidir. Sağlayıcının ayrı veri sorumlusu olduğu hesap ve
telemetri faaliyetleri ayrıca ele alınmalıdır. Seçilen güvencenin her aktarımı,
ilgili alt işleyenleri ve sonraki aktarımları kapsadığı teyit edilmelidir.

Standart sözleşme yolu seçilirse her iki tarafın geçerli imzası, imza tarihleri,
yetki belgeleri ve doldurulmuş ekler gerekir. Resmî metnin seçimlik alanları dışında
değişiklik yapılmaz; Türkçe metindeki imzalar önemlidir. İmzalar tamamlandıktan
sonra beş iş günü içinde Kuruma bildirim yapılmalı ve alındı kaydı saklanmalıdır.
Hesapta yalnız bir DPA bağlantısı görünmesi bu adımları karşılamaz.

- [KVKK yurt dışına aktarım açıklaması](https://www.kvkk.gov.tr/Icerik/2053/Yurtdisina-Aktarim).
- [Standart Sözleşme 2, resmî metin](https://www.kvkk.gov.tr/Icerik/7931/Kisisel-Verilerin-Yurt-Disina-Aktarilmasinda-Kullanilacak-Standart-Sozlesme-2-Veri-Sorumlusundan-Veri-Isleyene-).
- [KVKK imza ve bildirim kuralları](https://www.kvkk.gov.tr/Icerik/8170/Yurt-Disina-Kisisel-Veri-Aktariminda-Kullanilacak-Standart-Sozlesmelerde-Dikkat-Edilmesi-Gereken-Hususlara-Iliskin-Kamuoyu-Duyurusu).

## İncelemenin tamamlanması için kayıtlar

1. Her iki hesapta şirket, plan, DPA/sözleşme sürümü ve kabul kanıtını özel
   şirket kayıtlarına alın; sağlayıcıdan eksik kanıtları isteyin.
2. Sağlayıcıların Türkiye standart sözleşmesini kabul ve imza sürecini yazılı
   teyit edin. Desteklenmiyorsa uygun diğer güvenceyi veya bu akış için alternatif
   sağlayıcıyı değerlendirin; mevcut düzeni uygun kabul etmeyin.
3. Resmî eklerde gerçek veri kategorileri, amaç, süre, ülkeler, alt işleyenler,
   silme, erişim ve güvenlik tedbirlerini sağlayıcıyla birlikte doğrulayın.
4. Seçilen mekanizmanın imza/bildirim kanıtını tamamlayın. Google Analytics,
   işletme e-posta kutusu ve kullanılan diğer alıcıları ayrıca kapsayın.
5. Canlı bölgeyi, model eğitiminin kapalı olduğunu, en kısa uygun saklama süresini,
   erişim sınırlarını ve hak talebi için silme prosedürünü hesapta kontrol edin.
6. Kanıtlar tamamlanınca aydınlatma metnindeki aktarım bilgisini somut düzenleme
   ile güncelleyin. Bu belge tek başına hukuki uygunluk tamamlandı anlamına gelmez.

## Teknik doğrulama

`node --test tests/request-proposal.test.cjs` gerçek e-posta göndermeden sağlayıcıyı
taklit eder. Normal ve hesaplayıcı başvurusu, bağlam temizliği, geçersiz/büyük
istekler, honeypot, hata kayıtlarında veri sızıntısı ve HTTP yöntemi kontrol edilir.
`python3 tools/legal_pages.py` aydınlatma metnini yeniden üretir.
