# YÖK Akademik Web Scraper v1.4.0

Bu proje, YÖK Akademik platformundan akademisyenlerin bilgilerini otomatik olarak çeken ve düzenli bir Word dokümanı ve JSON olarak kaydeden bir Python uygulamasıdır.

[![Hits](https://hits.sh/github.com/MustafaKemal0146/yok-akademik-scraper.svg?style=for-the-badge&color=0089e9)](https://hits.sh/github.com/MustafaKemal0146/yok-akademik-scraper/)

## 🚀 Özellikler

- Akademik görev bilgilerini çekme
- Öğrenim bilgilerini çekme
- Yayınlanmış kitapları listeleme
- Akademik makaleleri detaylı bilgileriyle çekme
- Konferans bildirilerini listeleme
- Tüm bilgileri düzenli bir Word dokümanı olarak kaydetme
- Her kategoriyi ayrı sayfalarda gösterme
- Otomatik Chrome driver yönetimi
- İlerleme çubuğu ile işlem takibi
- Optimize edilmiş veri çekme hızı
- Geliştirilmiş hata yönetimi
- JSON formatında veri çıktısı
- Geliştirilmiş yazar bilgisi çekimi
- Daha doğru bildiri ve makale ayrıştırma
- Renkli konsol çıktıları ve banner tasarımı

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- Google Chrome tarayıcısı
- İnternet bağlantısı

## ⚙️ Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/mustafakemal0146/yok-akademik-scraper.git
cd yok-akademik-scraper
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

## 🎯 Kullanım

1. Programı iki şekilde çalıştırabilirsiniz:

```bash
# 1. URL'yi doğrudan komut satırından vererek:
python main.py https://akademik.yok.gov.tr/AkademikArama/AkademisyenGorevOgrenimBilgileri?islem=direct&authorId=XXXXXXXXXXXX

# 2. Program içinden URL girerek:
python main.py
```

2. Program otomatik olarak verileri çekecek ve iki dosya oluşturacaktır:
   - `academic_info.docx`: Word formatında rapor
   - `academic_info.json`: JSON formatında yapılandırılmış veri

## 📄 Çıktı Formatı

Word dokümanı aşağıdaki bölümleri içerir:

1. **Akademik Görevler**
   - Tarih
   - Unvan
   - Kurum
   - Bölüm

2. **Öğrenim Bilgileri**
   - Derece
   - Kurum
   - Bölüm
   - Tez bilgisi (varsa)

3. **Kitaplar**
   - Başlık
   - Yazarlar
   - Yayınevi
   - Basım bilgileri

4. **Makaleler**
   - Başlık
   - Yazarlar
   - Yayın Yeri
   - Yıl
   - Etiketler
   - DOI

5. **Bildiriler**
   - Başlık
   - Yazarlar
   - Yayın Yeri
   - Yıl
   - Tür

## ⚠️ Önemli Notlar

- Program Chrome tarayıcısını arka planda çalıştırır
- İnternet bağlantınızın stabil olduğundan emin olun
- YÖK Akademik'in yapısı değişirse program güncellenmeye ihtiyaç duyabilir
- Çok sayıda istek atılması durumunda YÖK Akademik geçici olarak erişimi kısıtlayabilir
- Progress bar sayesinde işlemin hangi aşamada olduğunu takip edebilirsiniz
- Optimize edilmiş yapı sayesinde daha hızlı veri çekimi yapılmaktadır
- JSON çıktısı sayesinde veriler başka sistemlerde de kullanılabilir
- Renkli konsol çıktıları ile işlem durumu daha net görülebilir

## 🔄 Güncelleme Geçmişi

- v1.0.0 (2024-01): İlk sürüm
  - Temel veri çekme özellikleri
  - Word dokümanı oluşturma
  - Hata yönetimi
- v1.1.0 (2024-02): Performans Güncellemesi
  - Progress bar eklendi (işlem durumu gösterimi)
  - Chrome tarayıcı optimizasyonları yapıldı
  - Veri çekme hızı artırıldı
  - Yayın yeri ve yıl bilgisi çekimi iyileştirildi
  - Gereksiz resim yüklemeleri devre dışı bırakıldı
  - Bekleme süreleri optimize edildi
  - Daha detaylı konsol çıktıları eklendi
- v1.2.0 (2024-02): Veri Çekimi İyileştirmeleri
  - JSON formatında veri çıktısı eklendi
  - Yazar bilgisi çekimi geliştirildi
  - BeautifulSoup ile daha doğru HTML ayrıştırma
  - Renkli konsol çıktıları eklendi
  - Bildiri ve makale ayrıştırma mantığı iyileştirildi
- v1.3.0 (2024-03): Arayüz ve Performans Geliştirmeleri
  - Renkli banner tasarımı eklendi
  - Terminal ekranı otomatik temizleme özelliği eklendi
  - Bildiri türü ve sunum şekli ayrı gösterim özelliği eklendi
  - Context manager (with statement) desteği eklendi
  - Chrome driver optimizasyonları yapıldı
  - Sayfa yükleme stratejisi iyileştirildi
  - Bellek kullanımı optimize edildi
  - Konsol arayüzü yenilendi
  - İlerleme çubukları renklendi
  - Hata mesajları renklendirildi
  - Genel performans iyileştirmeleri yapıldı
- v1.3.1 (2024-03): Arayüz ve Performans Geliştirmeleri
  - Renkli banner tasarımı eklendi
  - Terminal ekranı otomatik temizleme özelliği eklendi
  - Bildiri türü ve sunum şekli ayrı gösterim özelliği eklendi
  - Context manager (with statement) desteği eklendi
  - Chrome driver optimizasyonları yapıldı
  - Sayfa yükleme stratejisi iyileştirildi
  - Bellek kullanımı optimize edildi
  - Konsol arayüzü yenilendi
  - İlerleme çubukları renklendi
  - Hata mesajları renklendirildi
  - Genel performans iyileştirmeleri yapıldı
- v1.3.2 (2024-03): Veri Çekme İyileştirmeleri
  - Proje bilgileri çekme özelliği eklendi
  - Proje detayları (başlık, katılımcılar, tarih, bütçe vb.) ayrıştırma
  - Word raporuna projeler bölümü eklendi
  - JSON çıktısına projeler dahil edildi
  - Öğrenim bilgileri formatı iyileştirildi
  - Bildiri türü ve sunum şekli ayrı gösterim özelliği eklendi
  - Genel performans iyileştirmeleri yapıldı
- v1.4.0 (2024-04): Kapsamlı Veri Çekimi Güncellemesi
  - Verilen dersler çekme özelliği eklendi
  - Önlisans, lisans ve yüksek lisans dersleri ayrı ayrı listeleme
  - Ders detayları (dönem, ders adı, dili, saat) ayrıştırma
  - Word raporuna dersler bölümü eklendi
  - JSON çıktısına dersler dahil edildi
  - Her eğitim seviyesi için ayrı tablo formatı
  - Otomatik sekme geçişleri eklendi
  - Veri çekme sırası optimize edildi
  - Hata yönetimi geliştirildi
  - Genel performans iyileştirmeleri yapıldı

## 🤝 Katkıda Bulunma

1. Bu projeyi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

## 👥 İletişim

- GitHub: [@mustafakemal0146](https://github.com/mustafakemal0146)
- E-posta: ismustafakemal0146@gmail.com

## 🙏 Teşekkürler

Bu projeyi geliştirirken kullanılan açık kaynak kütüphanelerin geliştiricilerine teşekkürler:

- Selenium
- BeautifulSoup4
- python-docx
- pandas
- ve diğerleri...

Ve ayrıca bu proje fikrini veren ve geliştirmemde yardımcı olan Doçent Doktor Musa ÇIBUK hocama teşekkür ederim.

 
