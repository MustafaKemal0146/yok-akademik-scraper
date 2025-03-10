import yok_importer
import os
import re
from colorama import Fore, init

# Colorama'yı başlat
init(autoreset=True)

def extract_id_from_url(url):
    """URL'den YÖK Akademik ID'sini çıkarır"""
    pattern = r"authorId=([A-F0-9]{16})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def fetch_academic_data(yokak_id, visited_ids, depth=0, max_depth=2):
    """Fetch academic data for a given YÖK Akademik ID and its collaborators recursively."""
    if yokak_id in visited_ids:
        print(Fore.YELLOW + f"{yokak_id} ID'li akademisyen zaten işlendi.")
        return
    
    # Maksimum derinliğe ulaşıldıysa daha fazla işbirlikçi verisi çekme
    if max_depth is not None and depth >= max_depth:
        print(Fore.YELLOW + f"Maksimum derinliğe ({max_depth}) ulaşıldı. {yokak_id} için işbirlikçi verisi çekilmeyecek.")
        return

    visited_ids.add(yokak_id)
    max_depth_str = str(max_depth) if max_depth is not None else "∞"
    print(Fore.CYAN + f"\nYÖK Akademik ID: {yokak_id} için veri çekme işlemi başlatılıyor... (Derinlik: {depth}/{max_depth_str})")
    
    importer = yok_importer.YOKimporter(yokak_id)
    importer.setup_driver()

    academic_info = importer.fetch_academic_info()
    if academic_info is None:
        print(Fore.RED + f"{yokak_id} ID'li akademisyen için bilgi bulunamadı.")
        return

    collaborators = importer.fetch_collaborators()
    books = importer.fetch_books()
    articles = importer.fetch_articles()
    proceedings = importer.fetch_proceedings()
    projects = importer.fetch_projects()
    lessons = importer.get_lessons()
    administrative_duties = importer.get_administrative_duties()
    external_experiences = importer.get_external_experiences()
    awards = importer.get_awards()
    memberships = importer.get_memberships()
    patents = importer.get_patents()
    theses = importer.get_theses()
    artistic_activities = importer.get_artistic_activities()

    data = {
        'academic_info': academic_info,
        'collaborators': collaborators,
        'books': books,
        'articles': articles,
        'proceedings': proceedings,
        'projects': projects,
        'lessons': lessons,
        'administrative_duties': administrative_duties,
        'external_experiences': external_experiences,
        'awards': awards,
        'memberships': memberships,
        'patents': patents,
        'theses': theses,
        'artistic_activities': artistic_activities
    }

    json_filename = f"{yokak_id}_info.json"
    importer.save_to_json(data, json_filename)

    # Fetch data for collaborators
    for collaborator in collaborators:
        fetch_academic_data(collaborator['yokak_id'], visited_ids, depth + 1, max_depth)

def main():
    print(Fore.CYAN + "=" * 70)
    print(Fore.CYAN + "YÖK Akademik Veri Çekme Aracı")
    print(Fore.CYAN + "=" * 70)
    
    while True:
        print("\nLütfen aşağıdaki seçeneklerden birini girin:")
        print("1. YÖK Akademik ID ile arama")
        print("2. YÖK Akademik URL ile arama")
        print("3. Sonsuz Mod")
        print("4. Çıkış")
        
        choice = input("\nSeçiminiz (1-4): ")
        
        if choice == "1":
            yokak_id = input("\nLütfen YÖK Akademik ID'sini girin (örn: 1873F8613625992F): ").strip()
            if len(yokak_id) != 16 or not all(c in "0123456789ABCDEF" for c in yokak_id):
                print(Fore.RED + "Geçersiz YÖK Akademik ID formatı. ID 16 karakter uzunluğunda ve hexadecimal olmalıdır.")
                continue
        elif choice == "2":
            url = input("\nLütfen YÖK Akademik URL'sini girin: ").strip()
            yokak_id = extract_id_from_url(url)
            if not yokak_id:
                print(Fore.RED + "Geçersiz URL formatı. URL'de authorId parametresi bulunamadı.")
                continue
        elif choice == "3":
            yokak_id = input("\nLütfen başlangıç YÖK Akademik ID'sini girin (örn: 1873F8613625992F): ").strip()
            if len(yokak_id) != 16 or not all(c in "0123456789ABCDEF" for c in yokak_id):
                print(Fore.RED + "Geçersiz YÖK Akademik ID formatı. ID 16 karakter uzunluğunda ve hexadecimal olmalıdır.")
                continue
            
            print(Fore.CYAN + "\n--- Derinlik Sınırlaması Hakkında Bilgi ---")
            print("Derinlik, akademisyenler arasındaki ilişki ağında ne kadar ileri gidileceğini belirler:")
            print("• Derinlik 0: Sadece başlangıç akademisyeni için veri çekilir")
            print("• Derinlik 1: Başlangıç akademisyeni ve onun işbirlikçileri için veri çekilir")
            print("• Derinlik 2: Yukarıdakilere ek olarak, işbirlikçilerin işbirlikçileri için veri çekilir")
            print("• Derinlik 3+: Her seviye için bir adım daha ileri gidilir")
            print(Fore.YELLOW + "Not: Yüksek derinlik değerleri, işlem süresini önemli ölçüde artırabilir.")
            
            limit_depth = input("\nDerinlik sınırlaması olsun mu? (e/h): ").strip().lower()
            max_depth = None
            
            if limit_depth == 'e':
                try:
                    max_depth = int(input("Maksimum derinlik seviyesini girin (önerilen: 2-3, örn: 2): "))
                    if max_depth < 0:
                        print(Fore.YELLOW + "Derinlik negatif olamaz. Varsayılan olarak 2 kullanılacak.")
                        max_depth = 2
                    print(Fore.CYAN + f"Maksimum derinlik {max_depth} olarak ayarlandı.")
                    
                    # Tahmini akademisyen sayısını hesapla (varsayılan olarak her akademisyenin 5 işbirlikçisi olduğunu varsayalım)
                    estimated_count = 0
                    for i in range(max_depth + 1):
                        estimated_count += 5 ** i
                    print(Fore.YELLOW + f"Tahmini işlenecek akademisyen sayısı: ~{estimated_count} (her akademisyenin ortalama 5 işbirlikçisi olduğu varsayılarak)")
                    
                except ValueError:
                    print(Fore.YELLOW + "Geçersiz derinlik değeri. Varsayılan olarak 2 kullanılacak.")
                    max_depth = 2
            else:
                print(Fore.RED + "Dikkat: Sınırsız derinlik seçtiniz!")
                print(Fore.YELLOW + "Bu işlem:")
                print("• Çok uzun sürebilir (saatler veya günler)")
                print("• Sistem kaynaklarını tüketebilir")
                print("• YÖK Akademik sunucusuna aşırı yük bindirebilir")
                print("• Çok büyük miktarda veri üretebilir")
                
                confirm = input("Yine de devam etmek istiyor musunuz? (e/h): ").strip().lower()
                if confirm != 'e':
                    print(Fore.YELLOW + "İşlem iptal edildi. Varsayılan olarak derinlik 2 kullanılacak.")
                    max_depth = 2
                else:
                    print(Fore.RED + "Sınırsız derinlik modu etkinleştirildi. İşlem çok uzun sürebilir.")
                    max_depth = 3  # Sınırsız derinlik yerine 3 değerini kullanacağız
                    print(Fore.YELLOW + f"Derinlik seviyesi 3 olarak ayarlandı.")
                    
                    # Tahmini akademisyen sayısını hesapla
                    estimated_count = 0
                    for i in range(max_depth + 1):
                        estimated_count += 5 ** i
                    print(Fore.YELLOW + f"Tahmini işlenecek akademisyen sayısı: ~{estimated_count} (her akademisyenin ortalama 5 işbirlikçisi olduğu varsayılarak)")
            
            visited_ids = set()
            fetch_academic_data(yokak_id, visited_ids, 0, max_depth)
            continue
        elif choice == "4":
            print(Fore.YELLOW + "Programdan çıkılıyor...")
            break
        else:
            print(Fore.RED + "Geçersiz seçim. Lütfen 1-4 arasında bir değer girin.")
            continue

        # JSON dosyasının var olup olmadığını kontrol et
        json_filename = f"{yokak_id}_info.json"
        if os.path.exists(json_filename):
            overwrite = input(Fore.YELLOW + f"{json_filename} dosyası zaten mevcut. Üzerine yazmak istiyor musunuz? (e/h): ")
            if overwrite.lower() != 'e':
                print(Fore.YELLOW + "İşlem iptal edildi.")
                continue

        try:
            fetch_academic_data(yokak_id, set(), 0, 2)  # Maksimum 2 derinlik
        except Exception as e:
            print(Fore.RED + f"HATA: {yokak_id} ID'li akademisyen için işlem sırasında hata oluştu: {e}")
            continue

if __name__ == "__main__":
    main()
