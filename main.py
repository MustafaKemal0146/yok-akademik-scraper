from yok_scraper import YOKScraper
import sys
from colorama import init, Fore
from pyfiglet import Figlet
import os
import platform

init(autoreset=True)

def clear_screen():
    """İşletim sistemine göre terminal ekranını temizler"""
    if platform.system() == 'Windows':
        os.system('cls')
    else:  # Linux ve MacOS için
        os.system('clear')

def print_banner():
    f = Figlet(font='big')
    print(Fore.CYAN + "=" * 70)
    print(Fore.RED + f.renderText('YOK WEB'))
    print(Fore.GREEN + f.renderText('SCRAPER'))
    print(Fore.CYAN + "=" * 70)
    print(Fore.YELLOW + "\n" + " " * 20 + "YÖK Akademik Veri Çekme Aracı v1.3.2" + "\n")

def main():
    try:
        clear_screen()  # Terminal ekranını temizle
        print_banner()
        
        print(Fore.CYAN + "Örnek URL: https://akademik.yok.gov.tr/AkademikArama/view/searchResultviewAuthor.jsp?authorId=XXXX")
        url = (sys.argv[1] if len(sys.argv) > 1 else 
               input(Fore.YELLOW + "\nLütfen YÖK Akademik profil URL'sini girin: "))
        
        with YOKScraper(url) as scraper:
            results = scraper.scrape_all()
            
            if results:
                scraper.save_to_word(results)
                scraper.save_to_json(results)
                print(Fore.GREEN + "\nİşlem tamamlandı! Dosyalar oluşturuldu.")
            
    except Exception as e:
        print(Fore.RED + f"\nHata: {e}")
    
    finally:
        input(Fore.YELLOW + "\nKapatmak için Enter'a basın...")

if __name__ == "__main__":
    main() 
