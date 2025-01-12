from yok_scraper import YOKScraper
import sys
from colorama import init, Fore, Style
from pyfiglet import Figlet

# Colorama'yı başlat
init(autoreset=True)

def print_banner():
    f = Figlet(font='big')
    print(Fore.CYAN + "=" * 70)
    print(Fore.RED + Style.BRIGHT + f.renderText('YOK WEB'))
    print(Fore.GREEN + Style.BRIGHT + f.renderText('SCRAPER'))
    print(Fore.CYAN + "=" * 70)
    print(Fore.YELLOW + Style.BRIGHT + "\n" + " " * 20 + "YÖK Akademik Veri Çekme Aracı v1.3.0" + "\n")

def main():
    # Banner'ı göster
    print_banner()
    
    # Komut satırı argümanı verilmişse onu kullan, verilmemişse kullanıcıdan iste
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
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
