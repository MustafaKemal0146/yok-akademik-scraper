# YÖK Akademik Veri Çekme Aracı

Bu proje, YÖK Akademik platformundan akademisyenlerin bilgilerini otomatik olarak çeken ve düzenli bir Word dokümanı olarak kaydeden bir Python uygulamasıdır.

## 🚀 Özellikler

- Akademik görev bilgilerini çekme
- Öğrenim bilgilerini çekme
- Yayınlanmış kitapları listeleme
- Akademik makaleleri detaylı bilgileriyle çekme
- Konferans bildirilerini listeleme
- Tüm bilgileri düzenli bir Word dokümanı olarak kaydetme
- Her kategoriyi ayrı sayfalarda gösterme
- Otomatik Chrome driver yönetimi

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

1. `main.py` dosyasında akademisyenin YÖK Akademik URL'sini belirtin:
```python
url = "https://akademik.yok.gov.tr/AkademikArama/AkademisyenGorevOgrenimBilgileri?islem=direct&authorId=XXXXXXXXXXXX"
```

2. Programı çalıştırın:
```bash
python main.py
```

3. Program otomatik olarak verileri çekecek ve `academic_info.docx` adında bir Word dosyası oluşturacaktır.

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
   - Dergi
   - Yıl
   - İndeks bilgisi
   - DOI

5. **Bildiriler**
   - Başlık
   - Yazarlar
   - Konferans bilgisi
   - Yıl
   - Tür

## ⚠️ Önemli Notlar

- Program Chrome tarayıcısını arka planda çalıştırır
- İnternet bağlantınızın stabil olduğundan emin olun
- YÖK Akademik'in yapısı değişirse program güncellenmeye ihtiyaç duyabilir
- Çok sayıda istek atılması durumunda YÖK Akademik geçici olarak erişimi kısıtlayabilir

## 🔄 Güncelleme Geçmişi

- v1.0.0 (2024-01): İlk sürüm
  - Temel veri çekme özellikleri
  - Word dokümanı oluşturma
  - Hata yönetimi

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
