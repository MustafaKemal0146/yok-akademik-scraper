import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import re
import base64
from colorama import Fore, Style, init
from tqdm import tqdm
import time
import sys
import os
from datetime import datetime
from selenium.webdriver.chrome.options import Options

# YÖK Akademik Personel direkt bilgi sayfası ana URL şablonu
base_url = "https://akademik.yok.gov.tr/AkademikArama/AkademisyenGorevOgrenimBilgileri?islem=direct&authorId="

# Hız birimi arasına boşluk eklemek için bar_format'i güncelle
# bar_fmt = "{l_bar}{bar}|{n_fmt:>4}/{total_fmt:<4}[{elapsed}<{remaining}, {rate_fmt}{postfix}]"
bar_fmt = "{l_bar}{bar}|{n_fmt:>4}:{total_fmt:<4}[{elapsed}<{remaining}]"

ubook = " adet" # " kitap birimi"
ujson = " satr" # " JSON birimi"
msglen = 40     # İlerleme çubuğunda gösterilecek maksimum karakter sayısı
pstr = "... "   # İlerleme çubuğunda uzun mesajları kesme beliteci
nstr = "    "   # İlerleme çubuğunda kısa mesajları boşlukla doldurma belirteci

pbar_color = [
    "#CC8F96",  # Darkened Pastel Red
    "#CCB28F",  # Darkened Pastel Orange
    "#CCCC8F",  # Darkened Pastel Yellow
    "#96CC9F",  # Darkened Pastel Green
    "#96B3CC",  # Darkened Pastel Blue
    "#B3B3CC",  # Darkened Lavender
    "#CCABB0",  # Darkened Pastel Pink
    "#9EB39E",  # Darkened Pastel Mint
    "#C0B06C",  # Darkened Khaki
    "#C4B38F",  # Darkened Wheat
    "#A9A9A9",  # Darkened Light Grey
    "#B3CCCC",  # Darkened Light Cyan
    "#CC939E",  # Muted Coral
    "#9FB3CC",  # Muted Sky Blue
    "#CC9FA6",  # Muted Rose
    "#B3CC96"   # Muted Olive Green
]

# Colorama'yı başlat
init(autoreset=True)

# Chrome tarayıcı boyutu
chrome_width, chrome_height = 1900, 1000

class YOKimporter:
    def __init__(self, yokak_id):
        """
        YÖK Akademik Scraper sınıfını başlatır
        Args:
            pList: Akademisyenin YÖK Akademik Profil ID'si
        """       
        if not yokak_id or len(yokak_id) != 16:
            raise ValueError("Geçersiz YÖK Akademik ID'si")
        
        url = base_url + yokak_id
        self.url = url
        self.driver = None
        self.wait = None
        
        print(Fore.CYAN + f"YÖK Akademik ID: {yokak_id}" + Style.RESET_ALL)
        
    def __del__(self):
        """Destructor: Kaynakları temizle"""
        if self.driver:
            try:
                self.driver.quit()
                print(Fore.YELLOW + "Tarayıcı kapatıldı." + Style.RESET_ALL)
            except:
                pass

    def setup_driver(self):
        """Selenium webdriver'ı başlatır ve gerekli ayarları yapar"""
        try:
            # Önce Chrome ile deneyelim
            try:
                print(Fore.YELLOW + "Chrome tarayıcısı ile deneniyor..." + Style.RESET_ALL)
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--headless=new')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--remote-debugging-port=9222')
                chrome_options.add_argument('--log-level=3')  # Sadece kritik hataları göster
                chrome_options.add_argument(f'--window-size={chrome_width},{chrome_height}')
            
            # Performans optimizasyonları
                chrome_options.add_argument('--disable-extensions')
                chrome_options.add_argument('--disable-infobars')
                chrome_options.add_argument('--disable-notifications')
                chrome_options.add_argument('--disable-logging')
                chrome_options.add_argument('--disable-web-security')
                chrome_options.add_argument('--dns-prefetch-disable')
                
                # USB hatalarını gizlemek için
                chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

                service = ChromeService(executable_path=ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print(Fore.GREEN + "Chrome tarayıcısı başarıyla başlatıldı." + Style.RESET_ALL)
            except Exception as chrome_error:
                print(Fore.YELLOW + f"Chrome başlatılamadı: {chrome_error}" + Style.RESET_ALL)
                
                # Chrome başarısız olursa Edge ile deneyelim
                try:
                    print(Fore.YELLOW + "Edge tarayıcısı ile deneniyor..." + Style.RESET_ALL)
                    edge_options = webdriver.EdgeOptions()
                    edge_options.add_argument('--headless')
                    edge_options.add_argument(f'--window-size={chrome_width},{chrome_height}')
                    
                    service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
                    self.driver = webdriver.Edge(service=service, options=edge_options)
                    print(Fore.GREEN + "Edge tarayıcısı başarıyla başlatıldı." + Style.RESET_ALL)
                except Exception as edge_error:
                    print(Fore.RED + f"Edge başlatılamadı: {edge_error}" + Style.RESET_ALL)
                    print(Fore.RED + "Desteklenen tarayıcılardan hiçbiri başlatılamadı. Lütfen Chrome veya Edge tarayıcılarından birinin yüklü olduğundan emin olun." + Style.RESET_ALL)
                    raise Exception("Tarayıcı başlatılamadı")
            
            self.wait = WebDriverWait(self.driver, 10)
            
            # YÖK Akademik sayfasına git
            self.driver.get(f"{self.url}")
            time.sleep(2)  # Sayfanın yüklenmesi için bekle
            
            return True
        except Exception as e:
            print(Fore.RED + f"HATA: Tarayıcı sürücüsü başlatılamadı: {e}" + Style.RESET_ALL)
            raise

    def fetch_academic_info(self):
        """
        Akademisyenin görev ve öğrenim bilgilerini çeker
        Returns:
            academic_info: Akademik bilgileri içeren sözlük
        """
        try:
            # YÖK Akademik sayfasını açın
            self.driver.get(self.url)
            time.sleep(3)
            
            academic_info = {
                'profile': {},
                'duties': [],
                'education': []
            }
            
            # Profil bilgilerini çek
            try:
                img_tag = self.driver.find_element(By.CSS_SELECTOR, "img.img-circle")
            except NoSuchElementException:
                print(Fore.RED + f"HATA: Akademisyen bulunamadı. Lütfen URL'i ve ID'yi kontrol ediniz:\n{self.url}")
                return  None # Bu çalışmayı sonlandır

            # researcher_id ve yokak_id span etiketlerinin görünürlüğünü geçici olarak değiştir
            self.driver.execute_script("document.querySelector('span#spid').style.visibility = 'visible';")
            self.driver.execute_script("document.querySelector('span#spid2').style.visibility = 'visible';")
            
            researcher_id = self.driver.find_element(By.CSS_SELECTOR, "span#spid").text.strip()
            yokak_id = self.driver.find_element(By.CSS_SELECTOR, "span#spid2").text.strip()
            orcid_text = self.driver.find_element(By.CSS_SELECTOR, "span.greenOrcid p").text.strip()
            orcid = orcid_text.split(':', 1)[1].strip() if orcid_text else 'N/A'
            profile_table = self.driver.find_element(By.CSS_SELECTOR, "#authorlistTb")
            td_elements = profile_table.find_elements(By.CSS_SELECTOR, "td")[1]
            title = td_elements.find_element(By.CSS_SELECTOR, "h6").text.strip()
            name_surname = td_elements.find_element(By.CSS_SELECTOR, "h4").text.strip()
            text_elements = td_elements.text.split("\n")
            institution_parts = text_elements[2].split("/")
            university = institution_parts[0].strip() if len(institution_parts) > 0 else 'N/A'
            faculty = institution_parts[1].strip() if len(institution_parts) > 1 else 'N/A'
            department = institution_parts[2].strip() if len(institution_parts) > 2 else 'N/A'
            division = institution_parts[3].strip() if len(institution_parts) > 3 else 'N/A'
            
            # Uzmanlık alanları listesini oluştur
            expertise_list = []
            expertise_html = td_elements.get_attribute('innerHTML')
            soup = BeautifulSoup(expertise_html, 'html.parser')
            # span tagları içindeki uzmanlık alanları
            for span_tag in soup.find_all('span'):
                if span_tag.text.strip():
                    expertise_list.append(span_tag.text.strip())
            # span tagı dışında kalan uzmanlık alanları
            expertise_texts = []
            for element in soup.contents:
                if isinstance(element, str):
                    expertise_texts.append(element.strip())
            # texts listesinin son elemanını al ve ", " ile böl
            last_element = expertise_texts[-1].split(", ")
            # expertise_list'e ekle
            expertise_list.extend(last_element)

            # Resmi base64 formatında kaydet
            img_base64_str = img_tag.get_attribute("src")
            img_alt = f"{img_tag.get_attribute('alt')} ({orcid_text})"

            academic_info['profile'] = {
                'yokak_id': yokak_id,
                'title': title,
                'name_surname': name_surname,
                'researcher_id': researcher_id,
                'orcid': orcid,
                'institution': {
                    'university': university,
                    'faculty': faculty,
                    'department': department,
                    'division': division
                },
                'expertise': expertise_list,
                'picture': {
                    'img_base64_str': img_base64_str,
                    'alt': img_alt
                }
            }
            print("")
            print(Fore.YELLOW + f"Araştırmacı ({researcher_id}) : {title} {name_surname} profil bilgileri çekilecek..\n")
            
            # Akademik Görevler
            duties = self.driver.find_elements(By.CSS_SELECTOR, "div.col-md-6:nth-child(1) ul.timeline li")
            pbar = tqdm(duties, desc="Görevleri işleniyor ", unit=ubook, colour=pbar_color[0], bar_format=bar_fmt)
            current_year = None
            
            for idx, duty in enumerate(pbar):
                try:
                    # Başlık kontrolü
                    if "Akademik Görevler" in duty.text:
                        continue
                        
                    # Yıl etiketi
                    year = duty.find_elements(By.CSS_SELECTOR, "span.bg-light-blue")
                    if year:
                        current_year = year[0].text.strip()
                        continue
                    
                    # Görev bilgileri
                    position = duty.find_elements(By.CSS_SELECTOR, "div.timeline-footer a.btn-success")
                    institution = duty.find_elements(By.CSS_SELECTOR, "div.timeline-item h4")
                    department = duty.find_elements(By.CSS_SELECTOR, "div.timeline-item h5")
                    
                    if position and institution:
                        duty_text = f"{current_year} - {position[0].text.strip()} - {institution[0].text.strip()}"
                        if department:
                            duty_text += f" - {department[0].text.strip()}"
                        academic_info['duties'].append({
                            'year': current_year,
                            'position': position[0].text.strip(),
                            'institution': institution[0].text.strip(),
                            'department': department[0].text.strip() if department else 'N/A'
                        })
                        xstr = pstr if len(duty_text) > msglen else nstr
                        pbar.set_description(f"Görevleri işleniyor : {duty_text[:msglen]:<{msglen}}{xstr}")
                except Exception as e:
                    print(Fore.RED + f"HATA: Görev çekilemedi! (Duty {idx + 1:2d}): {e}")
            
            # Öğrenim Bilgileri
            education = self.driver.find_elements(By.CSS_SELECTOR, "div.col-md-6:nth-child(2) ul.timeline li")
            pbar = tqdm(education, desc="Öğrenimi işleniyor  ", unit=ubook, colour=pbar_color[1], bar_format=bar_fmt)
            current_year = None
            
            for idx, edu in enumerate(pbar):
                try:
                    # Başlık kontrolü
                    if "Öğrenim Bilgisi" in edu.text:
                        continue
                        
                    # Yıl etiketi
                    year = edu.find_elements(By.CSS_SELECTOR, "span.bg-light-blue")
                    if year:
                        current_year = year[0].text.strip()
                        continue
                    
                    # Öğrenim bilgileri
                    degree = edu.find_elements(By.CSS_SELECTOR, "div.timeline-footer a.btn-info")
                    institution = edu.find_elements(By.CSS_SELECTOR, "div.timeline-item h4")
                    department = edu.find_elements(By.CSS_SELECTOR, "div.timeline-item h5")
                    thesis = edu.find_elements(By.CSS_SELECTOR, "div.timeline-item h6")
                    
                    if degree and institution:
                        edu_text = f"{current_year} - {degree[0].text.strip()} - {institution[0].text.strip()}"
                        if department:
                            edu_text += f" - {department[0].text.strip()}"
                        if thesis:
                            thesis_text = thesis[0].text.strip().replace("Tez adı: ", "")
                            edu_text += f" - {thesis_text}"
                        academic_info['education'].append({
                            'year': current_year,
                            'degree': degree[0].text.strip(),
                            'institution': institution[0].text.strip(),
                            'department': department[0].text.strip() if department else 'N/A',
                            'thesis': thesis_text if thesis else 'N/A'
                        })
                        xstr = pstr if len(edu_text) > msglen else nstr
                        pbar.set_description(f"Öğrenimi işleniyor  : {edu_text[:msglen]:<{msglen}}{xstr}")
                except Exception as e:
                    print(Fore.RED + f"HATA: Öğrenim bilgisi çekilemedi! (Education {idx + 1:2d}): {e}")
            
            return academic_info
        except Exception as e:
            print(Fore.RED + f"HATA: Akademik bilgiler çekilirken hata: {e}")
            return None

    def fetch_collaborators(self):
        """
        Akademisyenin birlikte çalıştığı kişilerin listesini çeker
        Returns:
            collaborators: Birlikte çalışılan kişilerin bilgilerini içeren liste
        """
        try:
            # YÖK Akademik sayfasını açın
            self.driver.get(self.url)
            time.sleep(3)
            
            # "Birlikte çalıştığı kişiler" linkine tıklayın
            collaborators_link = self.driver.find_element(By.XPATH, '//a[@href="viewAuthorGraphs.jsp"]')
            collaborators_link.click()
            
            # Sayfanın tamamen yüklenmesini bekleyin
            collaborators = []
            parent_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#graphContainer > svg'))
            )
            # 'g' etiketlerini bulun
            g_elements = parent_element.find_elements(By.TAG_NAME, 'g')

            # Birlikte çalışılan kişileri çekin
            pbar = tqdm(g_elements[2:], desc="Collabs işleniyor    ", unit=ubook, colour=pbar_color[2], bar_format=bar_fmt)
            for g in pbar:
                try:
                    name_surname = g.find_element(By.TAG_NAME, 'text').text.strip()
                    yokak_id = g.find_element(By.TAG_NAME, 'circle').get_attribute('fill').strip(' url(#)')
                    img_base64_str = g.find_element(By.TAG_NAME, 'image').get_attribute('xlink:href')
                    collabs_text = f"{yokak_id} - {name_surname}"
                    collaborators.append({
                        'name_surname': name_surname,
                        'yokak_id': yokak_id,
                        'img_base64_str': img_base64_str
                    })
                    xstr = pstr if len(collabs_text) > msglen else nstr
                    pbar.set_description(f"Collabs işleniyor   : {collabs_text[:msglen]:<{msglen}}{xstr}")
                except Exception as e:
                    print(Fore.RED + f"HATA: Birlikte çalışılan kişi bilgisi çekilemedi: {e}")
            
            return collaborators
        except Exception as e:
            print(Fore.RED + f"HATA: Birlikte çalışılan kişiler çekilirken hata: {e}")
            return []

    def fetch_books(self):
        """
        Akademisyenin kitaplarını çeker
        Returns:
            books: Kitap bilgilerini içeren liste
        """
        try:
            self.driver.get(self.url)
            # Sol menüdeki "Kitaplar" linkine tıklayın
            books_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'li#booksMenu a'))
            )
            books_link.click()

            # Kitapların yüklenmesini bekleyin
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.projects'))
            )
            
            # Kitapları çekin
            books = []
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'div.projects > div.row')
            pbar = tqdm(rows, desc="Kitaplar işleniyor  ", unit=ubook, colour=pbar_color[3], bar_format=bar_fmt)
            for idx, row in enumerate(pbar):
                try:
                    b_div = row.find_element(By.CSS_SELECTOR, 'div.col-lg-11.col-md-10.col-sm-10.col-xs-9')
                    
                    # Kitap adı
                    full_title = b_div.find_element(By.CSS_SELECTOR, 'strong').text.strip()
                    title_parts = full_title.split('. ', 1)
                    b_no = title_parts[0].strip() if len(title_parts) > 1 else 'N/A'
                    b_title = title_parts[1].strip() if len(title_parts) > 1 else full_title
                    
                    # Kitap bilgileri
                    p_tags = b_div.find_elements(By.CSS_SELECTOR, 'p')
                    if len(p_tags) < 2:
                        continue
                    
                    # İlk p tagı içindeki bilgiler
                    info_text = p_tags[0].text.strip()
                    info_parts = info_text.split(', ')
                    
                    b_authors = []
                    b_publication_place = 'N/A'
                    b_editor = 'N/A'
                    b_edition = 'N/A'
                    b_pages = 'N/A'
                    b_isbn = 'N/A'
                    b_chapter_name = 'N/A'
                    b_chapter_pages = 'N/A'
                    
                    for part in info_parts:
                        if 'Yayın Yeri:' in part:
                            b_publication_place = part.split(':')[1].strip()
                        elif 'Editör:' in part:
                            b_editor = part.split(':')[1].strip()
                        elif 'Basım sayısı:' in part:
                            b_edition = part.split(':')[1].strip()
                        elif 'Sayfa sayısı:' in part:
                            b_pages = part.split(':')[1].strip()
                        elif 'ISBN:' in part:
                            b_isbn = part.split(':')[1].strip()
                        elif 'Bölüm Sayfaları:' in part:
                            b_chapter_pages = part.split(':', 1)[1].strip()
                        else:
                            b_authors.extend([author.strip() for author in part.split(',')])
                    
                    # Yazar adı "Bölüm Adı:" ile başlıyorsa
                    if b_authors and b_authors[0].startswith("Bölüm Adı:"):
                        b_chapter_name = b_authors[0].split(":", 1)[1].strip()
                        b_authors = b_authors[1:]
                    
                    # İkinci p tagı içindeki bilgiler
                    span_tags = p_tags[1].find_elements(By.CSS_SELECTOR, 'span')
                    b_year = span_tags[0].text.strip() if len(span_tags) > 0 else 'N/A'
                    b_type = span_tags[1].text.strip() if len(span_tags) > 1 else 'N/A'
                    b_chapter = span_tags[2].text.strip() if len(span_tags) > 2 else 'N/A'
                    
                    # Kitap bilgilerini ekleyin
                    books.append({
                        'no': b_no,
                        'title': b_title,
                        'authors': b_authors,
                        'publication_place': b_publication_place,
                        'editor': b_editor,
                        'edition': b_edition,
                        'pages': b_pages,
                        'isbn': b_isbn,
                        'year': b_year,
                        'type': b_type,
                        'chapter': b_chapter,
                        'chapter_name': b_chapter_name,
                        'chapter_pages': b_chapter_pages
                    })
                    xstr = pstr if len(b_title) > msglen else nstr
                    pbar.set_description(f"Kitaplar işleniyor  : {b_title[:msglen]:<{msglen}}{xstr}")
                except Exception as e:
                    print(Fore.GREEN + f"HATA: Kitap çekilemedi! (Book {idx + 1:2d}): {e}")

            return books
        except Exception as e:
            print(Fore.RED + f"HATA: Bir hata oluştu: {e}")
            return []

    def fetch_articles(self):
        """
        Akademisyenin makalelerini çeker
        Returns:
            articles: Makale bilgilerini içeren liste
        """        
        try:
            self.driver.get(self.url)
            # Sol menüdeki "Makaleler" linkine tıklayın
            articles_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/div/div/div[2]/ul/li[3]/a'))
            )
            articles_link.click()

            # İlk tablonun yüklenmesini bekleyin
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '(//table)[1]/tbody'))
            )
            
            # İlk tablodaki makaleleri çekin
            articles = []
            rows = self.driver.find_elements(By.XPATH, '(//table)[1]/tbody/tr')
            pbar = tqdm(rows, desc="Makaleler işleniyor ", unit=ubook, colour=pbar_color[4], bar_format=bar_fmt)
            for idx, row in enumerate(pbar):
                try:
                    first_td = row.find_elements(By.XPATH, './/td')[0]
                    p_no = first_td.text.strip() if first_td else 'N/A'
                    
                    second_td = row.find_elements(By.XPATH, './/td')[1]
                    outer_html = second_td.get_attribute('outerHTML')
                    title_tag = second_td.find_element(By.XPATH, './/a[@data-toggle="modal"]')
                    p_title = title_tag.text.strip()

                    # <p></p> ile <p> arasındaki veriyi al
                    p_content = outer_html.split('<p></p>')[1].split('<p>')[0].strip()
                    parts = p_content.replace('\n, ', ' , ').split(' , ')
                    p_authors_html = parts[0].strip() if len(parts) > 0 else 'N/A'
                    p_event = parts[1].strip().replace('Yayın Yeri:', '').strip() if len(parts) > 1 else 'N/A'
                    p_year_info = parts[2].strip() if len(parts) > 2 else 'N/A'

                    # HTML etiketlerini kaldır ve yazarları ayır
                    soup = BeautifulSoup(p_authors_html, 'html.parser')
                    p_authors = [author.strip() for author in soup.get_text().split(',')]

                    # İkinci <p> etiketinin içeriğindeki <span> etiketlerini al
                    span_tags = second_td.find_elements(By.XPATH, './/p[2]/span')
                    p_scope = span_tags[0].text.strip() if len(span_tags) > 0 else 'N/A'
                    p_type = span_tags[1].text.strip() if len(span_tags) > 1 else 'N/A'
                    p_index = span_tags[2].text.strip() if len(span_tags) > 2 else 'N/A'
                    p_article_type = span_tags[3].text.strip() if len(span_tags) > 3 else 'N/A'
                    
                    # DOI için <a> etiketini al
                    doi_tags = second_td.find_elements(By.XPATH, './/p[2]/a')
                    p_doi = doi_tags[0].get_attribute('href') if doi_tags else 'N/A'

                    # Diğer özellikleri de ekleyin
                    articles.append({
                        'no': p_no,
                        'title': p_title,
                        'authors': p_authors,
                        'publication': p_event,
                        'year': p_year_info,
                        'scope': p_scope,
                        'type': p_type,
                        'index': p_index,
                        'article_type': p_article_type,
                        'doi': p_doi
                        # 'other_attributes': ...
                    })
                    xstr = pstr if len(p_title) > msglen else nstr
                    pbar.set_description(f"Makaleler işleniyor : {p_title[:msglen]:<{msglen}}{xstr}")
                except Exception as e:
                    print(Fore.RED + f"HATA: Makale çekilemedi! (Article {idx + 1:2d}): {e}")

            return articles
        except Exception as e:
            print(Fore.RED + f"HATA: Bir hata oluştu: {e}")
            return []

    def fetch_proceedings(self):
        """
        Akademisyenin bildirilerini çeker
        Returns:
            proceedings: Bildiri bilgilerini içeren liste
        """
        try:
            self.driver.get(self.url)
            # Sol menüdeki "Bildiriler" linkine tıklayın
            proceedings_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/div/div/div[2]/ul/li[4]/a'))
            )
            proceedings_link.click()

            # İlk tablonun yüklenmesini bekleyin
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '(//table)[1]/tbody'))
            )
            
            # İlk tablodaki bildirileri çekin
            proceedings = []
            rows = self.driver.find_elements(By.XPATH, '(//table)[1]/tbody/tr')
            pbar = tqdm(rows, desc="Bildiriler işleniyor:", unit=ubook, colour=pbar_color[5], bar_format=bar_fmt)
            for idx, row in enumerate(pbar):
                try:
                    first_td = row.find_elements(By.XPATH, './/td')[0]
                    p_no = first_td.text.strip() if first_td else 'N/A'
                    
                    second_td = row.find_elements(By.XPATH, './/td')[1]
                    outer_html = second_td.get_attribute('outerHTML')
                    title_tag = second_td.find_element(By.XPATH, './/a[@data-toggle="modal"]')
                    p_title = title_tag.text.strip()

                    # <p></p> ile <p> arasındaki veriyi al
                    p_content = outer_html.split('<p></p>')[1].split('<p>')[0].strip()
                    parts = p_content.replace('\n, ', ' , ').split(' , ')
                    p_authors_html = parts[0].strip() if len(parts) > 0 else 'N/A'
                    p_event = parts[1].strip().replace('Yayın Yeri:', '').strip() if len(parts) > 1 else 'N/A'
                    p_year_info = parts[2].strip() if len(parts) > 2 else 'N/A'

                    # HTML etiketlerini kaldır ve yazarları ayır
                    soup = BeautifulSoup(p_authors_html, 'html.parser')
                    p_authors = [author.strip() for author in soup.get_text().split(',')]

                    # Son yazar adında bulunan tarih bilgisini ayır
                    if p_authors:
                        p_authors[-1] = p_authors[-1].split('\n ')[0].strip()

                    # Etkinlik tarihi bilgisi
                    event_date_match = re.search(r'\n \((\d{2}\.\d{2}\.\d{4})\n-(\d{2}\.\d{2}\.\d{4})\n\)', p_authors_html)
                    if not event_date_match:
                        event_date_match = re.search(r'\n \((\d{2}\.\d{2}\.\d{4})\n\)', p_authors_html)
                        event_date = event_date_match.group(1) if event_date_match else 'N/A'
                    else:
                        event_date = f"{event_date_match.group(1)} - {event_date_match.group(2)}"

                    # İkinci <p> etiketinin içeriğindeki <span> etiketlerini al
                    span_tags = second_td.find_elements(By.XPATH, './/p[2]/span')
                    p_scope = span_tags[0].text.strip() if len(span_tags) > 0 else 'N/A'
                    p_type = span_tags[1].text.strip() if len(span_tags) > 1 else 'N/A'
                    p_index = span_tags[2].text.strip() if len(span_tags) > 2 else 'N/A'
                    p_article_type = span_tags[3].text.strip() if len(span_tags) > 3 else 'N/A'
                    
                    # DOI için <a> etiketini al
                    doi_tags = second_td.find_elements(By.XPATH, './/p[2]/a')
                    p_doi = doi_tags[0].get_attribute('href') if doi_tags else 'N/A'

                    # Diğer özellikleri de ekleyin
                    proceedings.append({
                        'no': p_no,
                        'title': p_title,
                        'authors': p_authors,
                        'event': p_event,
                        'year': p_year_info,
                        'event_date': event_date,
                        'scope': p_scope,
                        'type': p_type,
                        'index': p_index,
                        'article_type': p_article_type,
                        'doi': p_doi
                        # 'other_attributes': ...
                    })
                    xstr = pstr if len(p_title) > msglen else nstr
                    pbar.set_description(f"Bildiriler işleniyor: {p_title[:msglen]:<{msglen}}{xstr}")
                except Exception as e:
                    print(Fore.RED + f"HATA: Bildiri çekilemedi! (Proceeding {idx + 1:2d}): {e}")

            return proceedings
        except Exception as e:
            print(Fore.RED + f"HATA: Bir hata oluştu: {e}")
            return []

    def fetch_projects(self):
        """
        Akademisyenin projelerini çeker
        Returns:
            projects: Proje bilgilerini içeren liste
        """
        try:
            self.driver.get(self.url)
            # Sol menüdeki "Projeler" linkine tıklayın
            projects_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'li#projectMenu a'))
            )
            projects_link.click()

            # Projelerin yüklenmesini bekleyin
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.projects'))
            )

            # Projeleri çekin
            projects = []
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'div.projectmain')
            pbar = tqdm(rows, desc="Projeler işleniyor  ", unit=ubook, colour=pbar_color[6], bar_format=bar_fmt)
            for idx, row in enumerate(pbar):
                try:
                    # Proje sıra numarası
                    p_no = row.find_element(By.CSS_SELECTOR, 'span.badge').text.strip()
                    
                    # Proje adı
                    p_title = row.find_element(By.CSS_SELECTOR, 'span.baslika strong').text.strip()
                    
                    # Proje katkı sağlayıcıları
                    contributors = []
                    project_main_html = row.get_attribute('innerHTML')
                    soup = BeautifulSoup(project_main_html, 'html.parser')
                    
                    # a tagları içindeki katkı sağlayıcılar
                    for a_tag in soup.find_all('a'):
                        contributors.append(a_tag.text.strip())
                    
                    # a tagı dışında kalan katkı sağlayıcılar
                    texts = []
                    for element in soup.contents:
                        if isinstance(element, str):
                            texts.append(element.strip())
                    for text in texts:
                        if text not in contributors:
                            contributors.append(text)
                    
                    # contributors içindeki her bir elemanı "," ile parçalara böl ve boş olmayanları alarak listeyi yeniden oluştur
                    contributors = [item.strip() for sublist in contributors for item in sublist.split(',') if item.strip()]
                    
                    # Proje bilgileri
                    project_type_div = row.find_element(By.CSS_SELECTOR, 'div.projectType')
                    span_tags = project_type_div.find_elements(By.XPATH, './/span')
                    p_place = span_tags[0].text.strip() if len(span_tags) > 0 else 'N/A'
                    p_type = span_tags[1].text.strip() if len(span_tags) > 1 else 'N/A'
                    p_status = span_tags[2].text.strip() if len(span_tags) > 2 else 'N/A'
                    
                    # Proje tarih ve bütçe bilgileri
                    info_text = project_type_div.text.split(' , ')
                    p_duration = info_text[1].strip() if len(info_text) > 1 else 'N/A'
                    p_funding = info_text[2].strip() if len(info_text) > 2 else 'N/A'
                    
                    # Proje konusu
                    try:
                        p_abstract_element = row.find_element(By.XPATH, "..//*[contains(@id, 'projectAbstract_')]/p")
                        p_abstract = p_abstract_element.get_attribute('innerHTML')
                    except Exception as e:
                        p_abstract = 'N/A'
                    
                    # Proje bilgilerini ekleyin
                    projects.append({
                        'no': p_no,
                        'title': p_title,
                        'contributors': contributors,
                        'place': p_place,
                        'type': p_type,
                        'status': p_status,
                        'duration': p_duration,
                        'funding': p_funding,
                        'abstract': p_abstract
                    })
                    xstr = pstr if len(p_title) > msglen else nstr
                    pbar.set_description(f"Projeler işleniyor  : {p_title[:msglen]:<{msglen}}{xstr}")
                except Exception as e:
                    print(Fore.RED + f"HATA: Proje çekilemedi! (Project {idx + 1:2d}): {e}")

            return projects
        except Exception as e:
            print(Fore.RED + f"HATA: Bir hata oluştu: {e}")
            return []

    def get_lessons(self):
        """Akademisyenin verdiği dersleri çeker"""
        try:
            # Dersler sekmesine tıkla
            print(Fore.CYAN + "\n📚 Ders bilgileri çekiliyor...")
            lessons_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li#lessonMenu a")))
            lessons_tab.click()
            time.sleep(1)  # Menünün yüklenmesi için bekle
            
            # Eğitim seviyelerini dinamik olarak çek
            education_levels = {}
            level_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[data-toggle='collapse'][data-parent='#accordion']")
            for elem in level_elements:
                href = elem.get_attribute('href').split('#')[-1]
                level_name = elem.text.strip()
                education_levels[href] = {'id': href, 'name': level_name}
            
            all_lessons = {}
            total_lessons_count = 0
            
            # Her eğitim seviyesi için dersleri çek
            for level, info in education_levels.items():
                try:
                    # İlk seviye (collapse0) zaten açık olduğu için sadece diğerlerine tıkla
                    if info['id'] != 'collapse0':
                        try:
                            # Eğitim seviyesi başlığına tıkla
                            level_header = self.wait.until(EC.element_to_be_clickable(
                                (By.XPATH, f"//a[@data-toggle='collapse' and @href='#{info['id']}']")))
                            level_header.click()
                            time.sleep(1)  # Tablonun yüklenmesi için bekle
                        except Exception as e:
                            print(Fore.YELLOW + f"⚠️ UYARI: {info['name']} sekmesine tıklarken hata: {e}")
                    
                    lessons = []
                    
                    # Doğrudan CSS seçici ile tabloyu bul
                    try:
                        table_selector = f"#{info['id']} > div > table"
                        table = self.wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, table_selector)))
                        
                        # Tablo satırlarını al
                        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
                        
                        if len(rows) > 0:
                            print(Fore.CYAN + f"{info['name']} dersleri işleniyor...")
                            
                            # tqdm ile ilerleme çubuğu oluştur
                            for row in tqdm(rows, desc=f"{info['name']} dersleri", 
                                           bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                                           colour="green"):
                                try:
                                    cols = row.find_elements(By.TAG_NAME, "td")
                                    if len(cols) >= 4:
                                        lesson = {
                                            'term': cols[0].text.strip(),
                                            'name': cols[1].text.strip(),
                                            'language': cols[2].text.strip(),
                                            'hours': cols[3].text.strip()
                                        }
                                        lessons.append(lesson)
                                        # İlerleme çubuğu açıklamasını güncelle
                                        tqdm.write(f"{Fore.GREEN}✓ {lesson['name']} ({lesson['term']})", end="\r")
                                except Exception as e:
                                    tqdm.write(f"{Fore.RED}❌ HATA: Ders satırı çekilemedi: {e}")
                                    continue
                        else:
                            print(Fore.YELLOW + f"⚠️ {info['name']} tablosunda ders bulunamadı")
                    except Exception as e:
                        print(Fore.RED + f"❌ HATA: {info['name']} tablosu bulunamadı: {e}")
                    
                    all_lessons[level] = {
                        'name': info['name'],
                        'lessons': lessons
                    }
                    
                    total_lessons_count += len(lessons)
                    
                except Exception as e:
                    print(Fore.RED + f"❌ HATA: {info['name']} dersleri çekilemedi: {e}")
                    all_lessons[level] = {
                        'name': info['name'],
                        'lessons': []
                    }
            
            if total_lessons_count > 0:
                print(Fore.GREEN + f"\n✅ Toplam {total_lessons_count} ders başarıyla çekildi")
            else:
                print(Fore.YELLOW + f"\n⚠️ Hiç ders bulunamadı")
                
            return all_lessons
            
        except Exception as e:
            print(Fore.RED + f"❌ HATA: Dersler çekilirken hata: {e}")
            return {}

    def get_administrative_duties(self):
        """Akademisyenin idari görevlerini çeker"""
        try:
            # İdari Görevler sekmesine tıkla
            print(Fore.CYAN + "\n🏢 İdari görev bilgileri çekiliyor...")
            admin_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li#idariMenu a")))
            admin_tab.click()
            time.sleep(1.5)  # Menünün yüklenmesi için bekle
            print(Fore.CYAN + "✓ İdari görevler sekmesine tıklandı")
            
            # İdari görevleri içeren timeline'ı bul
            try:
                timeline = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ul.timeline")))
                
                # Timeline içindeki tüm li elementlerini al
                items = timeline.find_elements(By.TAG_NAME, "li")
                
                if len(items) > 0:
                    print(Fore.CYAN + f"İdari görevler bulundu, {len(items)} görev var")
                    
                    administrative_duties = []
                    current_year = None
                    
                    # tqdm ile ilerleme çubuğu oluştur
                    for item in tqdm(items, desc="İdari görevler", 
                                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                                    colour="yellow"):
                        try:
                            # Başlık kontrolü (İdari Görevler yazısını atla)
                            if "İdari Görevler" in item.text:
                                continue
                            
                            # Son öğeyi atla (saat simgesi)
                            if "fa-clock-o" in item.get_attribute("innerHTML"):
                                continue
                            
                            # Yıl etiketi kontrolü
                            year_span = item.find_elements(By.CSS_SELECTOR, "span.bg-light-blue")
                            if year_span and len(year_span) > 0:
                                current_year = year_span[0].text.strip()
                                continue
                            
                            # Görev bilgilerini al
                            position = item.find_elements(By.CSS_SELECTOR, "div.timeline-footer a.btn-success")
                            institution = item.find_elements(By.CSS_SELECTOR, "div.timeline-item h4")
                            department = item.find_elements(By.CSS_SELECTOR, "div.timeline-item h5")
                            
                            if position and len(position) > 0:
                                duty = {
                                    'year': current_year,
                                    'position': position[0].text.strip()
                                }
                                
                                if institution and len(institution) > 0:
                                    duty['institution'] = institution[0].text.strip()
                                
                                if department and len(department) > 0:
                                    duty['department'] = department[0].text.strip()
                                
                                administrative_duties.append(duty)
                                tqdm.write(f"{Fore.GREEN}✓ {duty['position']} ({duty['year']})", end="\r")
                        except Exception as e:
                            tqdm.write(f"{Fore.RED}❌ HATA: İdari görev satırı çekilemedi: {e}")
                            continue
                    
                    if administrative_duties:
                        print(Fore.GREEN + f"\n✅ Toplam {len(administrative_duties)} idari görev başarıyla çekildi")
                    else:
                        print(Fore.YELLOW + f"\n⚠️ Hiç idari görev bulunamadı")
                    
                    return administrative_duties
                else:
                    print(Fore.YELLOW + f"⚠️ İdari görev bulunamadı")
                    return []
                
            except Exception as e:
                print(Fore.RED + f"❌ HATA: İdari görevler timeline'ı bulunamadı: {e}")
                return []
            
        except Exception as e:
            print(Fore.RED + f"❌ HATA: İdari görevler çekilirken hata: {e}")
            return []

    def get_external_experiences(self):
        """Akademisyenin üniversite dışı deneyimlerini çeker"""
        try:
            # Üniversite Dışı Deneyim sekmesine tıkla
            print(Fore.CYAN + "\n🏭 Üniversite dışı deneyim bilgileri çekiliyor...")
            experience_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li#expeirenceMenu a")))
            experience_tab.click()
            time.sleep(1.5)  # Menünün yüklenmesi için bekle
            print(Fore.CYAN + "✓ Üniversite dışı deneyim sekmesine tıklandı")
            
            # Deneyimleri içeren container'ı bul
            try:
                container = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.container-fluid")))
                
                # Container içindeki tüm listrow elementlerini al
                experience_items = container.find_elements(By.CSS_SELECTOR, "div.listrow")
                
                if len(experience_items) > 0:
                    print(Fore.CYAN + f"Üniversite dışı deneyimler bulundu, {len(experience_items)} deneyim var")
                    
                    external_experiences = []
                    
                    # tqdm ile ilerleme çubuğu oluştur
                    for item in tqdm(experience_items, desc="Üniversite dışı deneyimler", 
                                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                                    colour="magenta"):
                        try:
                            # Deneyim bilgilerini al
                            year = item.find_elements(By.CSS_SELECTOR, "span.label.label-info")
                            sector = item.find_elements(By.CSS_SELECTOR, "span.label.label-primary")
                            institution = item.find_elements(By.CSS_SELECTOR, "h5.listRowTitle")
                            position = item.find_elements(By.CSS_SELECTOR, "div.listRowAuthor strong")
                            
                            experience = {}
                            
                            if year and len(year) > 0:
                                experience['year'] = year[0].text.strip()
                            
                            if sector and len(sector) > 0:
                                experience['sector'] = sector[0].text.strip()
                            
                            if institution and len(institution) > 0:
                                experience['institution'] = institution[0].text.strip()
                            
                            if position and len(position) > 0:
                                experience['position'] = position[0].text.strip()
                            
                            if experience:
                                external_experiences.append(experience)
                                tqdm.write(f"{Fore.GREEN}✓ {experience.get('position', 'Pozisyon belirtilmemiş')} - {experience.get('institution', 'Kurum belirtilmemiş')} ({experience.get('year', 'Yıl belirtilmemiş')})", end="\r")
                        except Exception as e:
                            tqdm.write(f"{Fore.RED}❌ HATA: Deneyim satırı çekilemedi: {e}")
                            continue
                    
                    if external_experiences:
                        print(Fore.GREEN + f"\n✅ Toplam {len(external_experiences)} üniversite dışı deneyim başarıyla çekildi")
                    else:
                        print(Fore.YELLOW + f"\n⚠️ Hiç üniversite dışı deneyim bulunamadı")
                    
                    return external_experiences
                else:
                    print(Fore.YELLOW + f"⚠️ Üniversite dışı deneyim bulunamadı")
                    return []
                
            except Exception as e:
                print(Fore.RED + f"❌ HATA: Üniversite dışı deneyimler container'ı bulunamadı: {e}")
                return []
            
        except Exception as e:
            print(Fore.RED + f"❌ HATA: Üniversite dışı deneyimler çekilirken hata: {e}")
            return []

    def get_awards(self):
        """Akademisyenin aldığı ödülleri çeker"""
        try:
            # Ödüller sekmesine tıkla
            print(Fore.CYAN + "\n🏆 Alınan ödül bilgileri çekiliyor...")
            awards_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li#awardMenu a")))
            awards_tab.click()
            time.sleep(1.5)  # Menünün yüklenmesi için bekle
            print(Fore.CYAN + "✓ Ödüller sekmesine tıklandı")
            
            # Ödülleri içeren timeline'ı bul
            try:
                timeline = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ul.timeline")))
                
                # Timeline içindeki tüm li elementlerini al (ödüller)
                award_items = timeline.find_elements(By.TAG_NAME, "li")
                
                if len(award_items) > 0:
                    print(Fore.CYAN + f"Ödüller bulundu, {len(award_items)} ödül var")
                    
                    awards = []
                    
                    # tqdm ile ilerleme çubuğu oluştur
                    for item in tqdm(award_items, desc="Ödüller", 
                                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                                    colour="cyan"):
                        try:
                            # Ödül bilgilerini al
                            year_badge = item.find_elements(By.CSS_SELECTOR, "div.timeline-badge")
                            award_title = item.find_elements(By.CSS_SELECTOR, "h4.timeline-title")
                            award_institution = item.find_elements(By.CSS_SELECTOR, "small.text-muted")
                            award_details = item.find_elements(By.CSS_SELECTOR, "div.timeline-body p")
                            
                            award = {}
                            
                            if year_badge and len(year_badge) > 0:
                                award['year'] = year_badge[0].text.strip()
                            
                            if award_title and len(award_title) > 0:
                                award['title'] = award_title[0].text.strip()
                            
                            if award_institution and len(award_institution) > 0:
                                award['institution'] = award_institution[0].text.strip()
                            
                            if award_details and len(award_details) > 0:
                                # Detay metnini işle (örn: "Üniversite, TÜRKİYE")
                                details_text = award_details[0].text.strip()
                                details_parts = details_text.split(',', 1)
                                
                                if len(details_parts) >= 1:
                                    award['type'] = details_parts[0].strip()
                                
                                if len(details_parts) >= 2:
                                    award['country'] = details_parts[1].strip()
                            
                            if award:
                                awards.append(award)
                                tqdm.write(f"{Fore.GREEN}✓ {award.get('title', 'Ödül adı belirtilmemiş')} ({award.get('year', 'Yıl belirtilmemiş')})", end="\r")
                        except Exception as e:
                            tqdm.write(f"{Fore.RED}❌ HATA: Ödül satırı çekilemedi: {e}")
                            continue
                    
                    if awards:
                        print(Fore.GREEN + f"\n✅ Toplam {len(awards)} ödül başarıyla çekildi")
                    else:
                        print(Fore.YELLOW + f"\n⚠️ Hiç ödül bulunamadı")
                    
                    return awards
                else:
                    print(Fore.YELLOW + f"⚠️ Ödül bulunamadı")
                    return []
                
            except Exception as e:
                print(Fore.RED + f"❌ HATA: Ödüller timeline'ı bulunamadı: {e}")
                return []
            
        except Exception as e:
            print(Fore.RED + f"❌ HATA: Ödüller çekilirken hata: {e}")
            return []

    def get_memberships(self):
        """Akademisyenin üyeliklerini çeker"""
        try:
            # Üyelikler sekmesine tıkla
            print(Fore.CYAN + "\n🔖 Üyelik bilgileri çekiliyor...")
            memberships_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li#memberMenu a")))
            memberships_tab.click()
            time.sleep(1.5)  # Menünün yüklenmesi için bekle
            print(Fore.CYAN + "✓ Üyelikler sekmesine tıklandı")
            
            # Üyelikleri içeren container'ı bul
            try:
                container = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.container-fluid")))
                
                # Container içindeki tüm bs-callout elementlerini al (üyelikler)
                membership_items = container.find_elements(By.CSS_SELECTOR, "div.bs-callout.bs-callout-warning")
                
                if len(membership_items) > 0:
                    print(Fore.CYAN + f"Üyelikler bulundu, {len(membership_items)} üyelik var")
                    
                    memberships = []
                    
                    # tqdm ile ilerleme çubuğu oluştur
                    for item in tqdm(membership_items, desc="Üyelikler", 
                                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                                    colour="green"):
                        try:
                            # Üyelik bilgilerini al
                            organization = item.find_elements(By.TAG_NAME, "h4")
                            details = item.find_elements(By.TAG_NAME, "p")
                            
                            membership = {}
                            
                            if organization and len(organization) > 0:
                                membership['organization'] = organization[0].text.strip()
                            
                            if details and len(details) > 0:
                                details_text = details[0].text.strip()
                                
                                # Pozisyon ve yıl bilgilerini ayır
                                # Genellikle format: "Pozisyon\nYıl" şeklinde
                                lines = details_text.split('\n')
                                
                                if len(lines) >= 1:
                                    membership['position'] = lines[0].strip()
                                
                                if len(lines) >= 2:
                                    membership['year'] = lines[1].strip()
                            
                            if membership:
                                memberships.append(membership)
                                tqdm.write(f"{Fore.GREEN}✓ {membership.get('organization', 'Organizasyon belirtilmemiş')} - {membership.get('position', 'Pozisyon belirtilmemiş')}", end="\r")
                        except Exception as e:
                            tqdm.write(f"{Fore.RED}❌ HATA: Üyelik satırı çekilemedi: {e}")
                            continue
                    
                    if memberships:
                        print(Fore.GREEN + f"\n✅ Toplam {len(memberships)} üyelik başarıyla çekildi")
                    else:
                        print(Fore.YELLOW + f"\n⚠️ Hiç üyelik bulunamadı")
                    
                    return memberships
                else:
                    print(Fore.YELLOW + f"⚠️ Üyelik bulunamadı")
                    return []
                
            except Exception as e:
                print(Fore.RED + f"❌ HATA: Üyelikler container'ı bulunamadı: {e}")
                return []
            
        except Exception as e:
            print(Fore.RED + f"❌ HATA: Üyelikler çekilirken hata: {e}")
            return []

    def get_patents(self):
        """Akademisyenin patentlerini çeker"""
        try:
            # Patentler sekmesine tıkla
            print(Fore.CYAN + "\n🔬 Patent bilgileri çekiliyor...")
            patents_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li#patentMenu a")))
            patents_tab.click()
            time.sleep(1.5)  # Menünün yüklenmesi için bekle
            print(Fore.CYAN + "✓ Patentler sekmesine tıklandı")
            
            # Patentleri içeren container'ı bul
            try:
                projects_container = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.projects")))
                
                # Container içindeki tüm patent elementlerini al
                patent_items = projects_container.find_elements(By.XPATH, "./div")
                
                if len(patent_items) > 0:
                    print(Fore.CYAN + f"Patentler bulundu, {len(patent_items)} patent var")
                    
                    patents = []
                    
                    # tqdm ile ilerleme çubuğu oluştur
                    for item in tqdm(patent_items, desc="Patentler", 
                                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                                    colour="blue"):
                        try:
                            # Patent bilgilerini al
                            title_elem = item.find_elements(By.CSS_SELECTOR, "h5.projectTitle strong")
                            authors_elem = item.find_elements(By.CSS_SELECTOR, "div.projectAuthor")
                            type_elem = item.find_elements(By.CSS_SELECTOR, "span.label.label-info")
                            class_elem = item.find_elements(By.CSS_SELECTOR, "span.label.label-success")
                            
                            # Özet için collapse ID'sini bul
                            abstract_id = None
                            abstract_btn = item.find_elements(By.CSS_SELECTOR, "a.btn[data-toggle='collapse']")
                            if abstract_btn and len(abstract_btn) > 0:
                                abstract_id = abstract_btn[0].get_attribute("data-target").replace("#", "")
                            
                            abstract_elem = None
                            if abstract_id:
                                abstract_elem = item.find_elements(By.CSS_SELECTOR, f"#{abstract_id} p")
                            
                            patent = {}
                            
                            if title_elem and len(title_elem) > 0:
                                patent['title'] = title_elem[0].text.strip()
                            
                            if authors_elem and len(authors_elem) > 0:
                                authors_text = authors_elem[0].text.strip()
                                
                                # Patent başvuru sahiplerini ve buluş sahiplerini ayır
                                if "Patent Başvuru Sahipleri" in authors_text:
                                    applicants_part = authors_text.split("Patent Başvuru Sahipleri")[1].split("Patent Buluş Sahipleri")[0]
                                    applicants = applicants_part.replace(":", "").strip()
                                    patent['applicants'] = applicants
                                
                                if "Patent Buluş Sahipleri" in authors_text:
                                    inventors_part = authors_text.split("Patent Buluş Sahipleri")[1]
                                    inventors = inventors_part.replace(":", "").strip()
                                    patent['inventors'] = inventors
                            
                            if type_elem and len(type_elem) > 0:
                                patent['type'] = type_elem[0].text.strip()
                            
                            if class_elem and len(class_elem) > 0:
                                patent['class'] = class_elem[0].text.strip()
                            
                            if abstract_elem and len(abstract_elem) > 0:
                                patent['abstract'] = abstract_elem[0].text.strip()
                            
                            if patent:
                                patents.append(patent)
                                tqdm.write(f"{Fore.GREEN}✓ {patent.get('title', 'Patent adı belirtilmemiş')}", end="\r")
                        except Exception as e:
                            tqdm.write(f"{Fore.RED}❌ HATA: Patent satırı çekilemedi: {e}")
                            continue
                    
                    if patents:
                        print(Fore.GREEN + f"\n✅ Toplam {len(patents)} patent başarıyla çekildi")
                    else:
                        print(Fore.YELLOW + f"\n⚠️ Hiç patent bulunamadı")
                    
                    return patents
                else:
                    print(Fore.YELLOW + f"⚠️ Patent bulunamadı")
                    return []
                
            except Exception as e:
                print(Fore.RED + f"❌ HATA: Patentler container'ı bulunamadı: {e}")
                return []
            
        except Exception as e:
            print(Fore.RED + f"❌ HATA: Patentler çekilirken hata: {e}")
            return []

    def get_theses(self):
        """Akademisyenin yönettiği tezleri doğrudan tablodan çeker"""
        try:
            print(Fore.CYAN + "\n📖 Yönetilen tez bilgileri çekiliyor...")
            thesis_tab = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li#thesisMenu a")))
            thesis_tab.click()
            time.sleep(1.5)

            theses = []
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) == 4:
                    theses.append({
                        'year': cols[0].text.strip(),
                        'author': cols[1].text.strip(),
                        'title': cols[2].text.strip(),
                        'university': cols[3].text.strip()
                    })

            print(Fore.GREEN + f"\n✅ Toplam {len(theses)} tez başarıyla çekildi")
            return theses

        except Exception as e:
            print(Fore.RED + f"❌ HATA: Yönetilen tezler çekilirken hata: {e}")
            return []

    def get_artistic_activities(self):
        """Akademisyenin sanatsal aktivitelerini çeker"""
        try:
            print(Fore.CYAN + "\n🎨 Sanatsal aktiviteler çekiliyor...")
            art_tab = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li#artMenu a")))
            art_tab.click()
            time.sleep(1.5)

            activities = []
            rows = self.driver.find_elements(By.CSS_SELECTOR, "div.listrow")
            for row in rows:
                activity_type = row.find_element(By.CSS_SELECTOR, "div.listRowType span.label-primary").text.strip()
                title = row.find_element(By.CSS_SELECTOR, "h5.listRowTitle").text.strip()
                place = row.find_element(By.CSS_SELECTOR, "div.listRowAuthor strong").text.replace('Yer:', '').strip()
                organizer = row.find_element(By.CSS_SELECTOR, "div.listRowAuthor").text.split('Düzenleyen(ler):')[-1].strip()
                date = row.find_elements(By.CSS_SELECTOR, "div.listRowAuthor span.label-info")[-1].text.strip()

                activities.append({
                    'type': activity_type,
                    'title': title,
                    'place': place,
                    'organizer': organizer,
                    'date': date
                })

            print(Fore.GREEN + f"\n✅ Toplam {len(activities)} sanatsal aktivite başarıyla çekildi")
            return activities

        except Exception as e:
            print(Fore.RED + f"❌ HATA: Sanatsal aktiviteler çekilirken hata: {e}")
            return []

    def save_to_json(self, data, filename='academic_info.json'):
        """Verileri JSON formatında kaydeder"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(Fore.GREEN + f"\nVeriler başarıyla kaydedildi: {filename}")
            return True
        except Exception as e:
            print(Fore.RED + f"\nJSON kaydetme hatası: {e}")
            return False
