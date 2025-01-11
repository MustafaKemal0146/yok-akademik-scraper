from yok_scraper import YOKScraper
import sys

def main():
    # Komut satırı argümanı verilmişse onu kullan, verilmemişse kullanıcıdan iste
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        print("YÖK Akademik Veri Çekme Programı")
        print("-" * 40)
        url = input("Lütfen YÖK Akademik profil URL'sini girin: ")
    
    try:
        # Scraper'ı başlat
        scraper = YOKScraper(url)
        
        # Tüm verileri çek
        results = scraper.scrape_all()
        
        print("\nVeriler Word dosyasına kaydediliyor...")
        
        # Verileri Word dosyasına kaydet
        scraper.save_to_word(results)
        
        # Verileri JSON dosyasına kaydet
        scraper.save_to_json(results)
        
        print("\nİşlem tamamlandı! academic_info.docx ve academic_info.json dosyaları oluşturuldu.")
        
    except Exception as e:
        print(f"\nHata oluştu: {e}")
    
    input("\nProgramı kapatmak için Enter'a basın...")

if __name__ == "__main__":
    main() 
