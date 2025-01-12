from yok_scraper import YOKScraper
import sys
from colorama import init, Fore, Style

# Colorama'yı başlat
init(autoreset=True)

def main():
    # Komut satırı argümanı verilmişse onu kullan, verilmemişse kullanıcıdan iste
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        print(Fore.GREEN + Style.BRIGHT + "\nYÖK Akademik Veri Çekme Programı")
        print(Fore.GREEN + Style.BRIGHT + "-" * 40)
        print(Fore.CYAN + "Örnek URL: https://akademik.yok.gov.tr/AkademikArama/view/searchResultviewAuthor.jsp?authorId=XXXX")
        url = input(Fore.YELLOW + "\nLütfen YÖK Akademik profil URL'sini girin: ")
    
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
        
        print(Fore.GREEN + "\nİşlem tamamlandı! academic_info.docx ve academic_info.json dosyaları oluşturuldu.")
        
    except Exception as e:
        print(Fore.RED + f"\nHata oluştu: {e}")
    
    input(Fore.YELLOW + "\nProgramı kapatmak için Enter'a basın...")

if __name__ == "__main__":
    main() 
