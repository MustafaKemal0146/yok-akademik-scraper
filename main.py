from yok_scraper import YOKScraper

def main():
    print("YÖK Akademik Veri Çekme Programı")
    print("-" * 40)
    
    # Kullanıcıdan URL al
    url = input("Lütfen YÖK Akademik profil URL'sini girin: ")
    
    print("\nVeriler çekiliyor...")
    
    try:
        # Scraper'ı başlat
        scraper = YOKScraper(url)
        
        # Tüm verileri çek
        results = scraper.scrape_all()
        
        print("\nVeriler Word dosyasına kaydediliyor...")
        
        # Verileri Word dosyasına kaydet
        scraper.save_to_word(results)
        
        print("\nİşlem tamamlandı! academic_info.docx dosyası oluşturuldu.")
        
    except Exception as e:
        print(f"\nHata oluştu: {e}")
    
    input("\nProgramı kapatmak için Enter'a basın...")

if __name__ == "__main__":
    main() 
