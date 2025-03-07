# YÖK Akademik Web Scraper FİNAL

Bu proje, YÖK Akademik platformundan akademisyenlerin bilgilerini otomatik olarak çeken ve JSON formatında kaydeden bir Python uygulamasıdır.

[![Hits](https://hits.sh/github.com/MustafaKemal0146/yok-akademik-scraper.svg?style=for-the-badge&color=0089e9)](https://hits.sh/github.com/MustafaKemal0146/yok-akademik-scraper/)

## 🚀 Özellikler

- Akademik görev bilgilerini çekme
- Öğrenim bilgilerini çekme
- Yayınlanmış kitapları listeleme
- Akademik makaleleri detaylı bilgileriyle çekme
- Konferans bildirilerini listeleme
- Proje bilgilerini çekme
- Verilen dersleri çekme
- İdari görevleri çekme
- Üniversite dışı deneyimleri çekme
- Alınan ödülleri çekme
- Üyelik bilgilerini çekme
- Patent bilgilerini çekme
- Yönetilen tezleri çekme
- Sanatsal aktiviteleri çekme
- Sonsuz mod ile birlikte çalışılan kişilerin verilerini çekme
- Tüm bilgileri düzenli bir Word dokümanı ve JSON olarak kaydetme
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

2. Program otomatik olarak verileri çekecek ve JSON formatında bir dosya oluşturacaktır:
   - `academic_info.json`: JSON formatında yapılandırılmış veri

3. Program çalıştırıldığında aşağıdaki seçenekler sunulacaktır:
   - **1. YÖK Akademik ID ile arama**: Doğrudan bir YÖK Akademik ID girerek veri çekme işlemi başlatılır.
   - **2. YÖK Akademik URL ile arama**: Bir YÖK Akademik URL'si girerek veri çekme işlemi başlatılır.
   - **3. Sonsuz Mod**: Başlangıç olarak bir YÖK Akademik ID girilir ve bu ID'ye bağlı tüm işbirlikçilerin verileri de çekilir. (sadece id ile arama)
   - **4. Çıkış**: Programdan çıkılır.

## 📄 Çıktı Formatı

JSON dosyası aşağıdaki bölümleri içerir:

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

6. **Projeler**
   - Başlık
   - Katılımcılar
   - Yer
   - Tür
   - Durum
   - Süre
   - Bütçe
   - Özet

7. **Dersler**
   - Dönem
   - Ders Adı
   - Dil
   - Saat

8. **İdari Görevler**
   - Yıl
   - Pozisyon
   - Kurum
   - Bölüm

9. **Üniversite Dışı Deneyimler**
   - Yıl
   - Sektör
   - Kurum
   - Pozisyon

10. **Ödüller**
    - Yıl
    - Başlık
    - Kurum
    - Tür
    - Ülke

11. **Üyelikler**
    - Organizasyon
    - Pozisyon
    - Yıl

12. **Patentler**
    - Başlık
    - Başvuru Sahipleri
    - Buluş Sahipleri
    - Tür
    - Sınıf
    - Özet

13. **Tezler**
    - Yıl
    - Yazar
    - Başlık
    - Üniversite

14. **Sanatsal Aktiviteler**
    - Tür
    - Başlık
    - Yer
    - Düzenleyen(ler)
    - Tarih

## ⚠️ Önemli Notlar

- Program Chrome tarayıcısını arka planda çalıştırır
- İnternet bağlantınızın stabil olduğundan emin olun
- YÖK Akademik'in yapısı değişirse program güncellenmeye ihtiyaç duyabilir
- Çok sayıda istek atılması durumunda YÖK Akademik geçici olarak erişimi kısıtlayabilir
- Progress bar sayesinde işlemin hangi aşamada olduğunu takip edebilirsiniz
- Optimize edilmiş yapı sayesinde daha hızlı veri çekimi yapılmaktadır
- JSON çıktısı sayesinde veriler başka sistemlerde de kullanılabilir
- Renkli konsol çıktıları ile işlem durumu daha net görülebilir

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

 
