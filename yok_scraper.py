from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
from fpdf import FPDF
from fpdf.fonts import FontFace
from datetime import datetime
import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

class YOKScraper:
    def __init__(self, url):
        """
        YÖK Akademik Scraper sınıfını başlatır
        Args:
            url: Akademisyenin YÖK profil URL'i
        """
        self.url = url
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Selenium webdriver'ı başlatır ve gerekli ayarları yapar"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Tarayıcıyı arka planda çalıştır
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)  # 30 saniye bekle
        
    def get_academic_info(self):
        """
        Akademisyenin görev ve öğrenim bilgilerini çeker
        Returns:
            dict: Akademik bilgileri içeren sözlük
        """
        try:
            self.driver.get(self.url)
            time.sleep(3)
            
            academic_info = {
                'duties': [],
                'education': []
            }
            
            # Akademik Görevler
            duties = self.driver.find_elements(By.CSS_SELECTOR, "div.col-md-6:nth-child(1) ul.timeline li")
            current_year = None
            
            for duty in duties:
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
                        academic_info['duties'].append(duty_text)
                except Exception as e:
                    continue
            
            # Öğrenim Bilgileri
            education = self.driver.find_elements(By.CSS_SELECTOR, "div.col-md-6:nth-child(2) ul.timeline li")
            current_year = None
            
            for edu in education:
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
                            edu_text += f" - {thesis[0].text.strip()}"
                        academic_info['education'].append(edu_text)
                except Exception as e:
                    continue
                
            return academic_info
        except Exception as e:
            print(f"Akademik bilgiler çekilirken hata: {e}")
            return None

    def get_books(self):
        """
        Akademisyenin kitaplarını çeker
        Returns:
            list: Kitap bilgilerini içeren liste
        """
        try:
            # Kitaplar sekmesine tıkla
            books_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li#booksMenu a")))
            books_tab.click()
            time.sleep(5)
            
            books = []
            book_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.projects div.row")
            
            for book in book_elements:
                try:
                    title = book.find_element(By.CSS_SELECTOR, "strong").text.strip()
                    info = book.find_element(By.CSS_SELECTOR, "p").text.strip()
                    
                    # Bilgileri parçala
                    info_parts = info.split(',')
                    authors = info_parts[0].strip()
                    publisher = next((part.split(':')[1].strip() for part in info_parts if 'Yayın Yeri' in part), '')
                    
                    book_info = {
                        'title': title,
                        'authors': authors,
                        'publisher': publisher
                    }
                    books.append(book_info)
                except:
                    continue
                
            return books
        except Exception as e:
            print(f"Kitaplar çekilirken hata: {e}")
            return []

    def get_articles(self):
        """
        Akademisyenin makalelerini çeker
        Returns:
            list: Makale bilgilerini içeren liste
        """
        try:
            # Makaleler sekmesine tıkla
            articles_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li#articleMenu a")))
            articles_tab.click()
            print("Makaleler sekmesine tıklandı")
            time.sleep(5)
            
            articles = []
            article_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.tab-content div.tab-pane.active tr")
            print(f"Bulunan makale sayısı: {len(article_elements)}")
            
            for article in article_elements:
                try:
                    # Başlık
                    title = article.find_element(By.CSS_SELECTOR, "strong").text.strip()
                    
                    # Yazarlar - popoverData class'ına sahip a etiketlerini bul
                    author_elements = article.find_elements(By.CSS_SELECTOR, "a.popoverData")
                    authors = ', '.join([author.text.strip() for author in author_elements])
                    
                    # Yayın bilgileri
                    pub_info = article.find_element(By.CSS_SELECTOR, "td p:last-of-type").text.strip()
                    pub_parts = pub_info.split(',')
                    
                    # Dergi adı
                    journal = next((part.split(':')[1].strip() for part in pub_parts if 'Yayın Yeri:' in part), '')
                    
                    # Yıl
                    year = next((part.strip() for part in pub_parts if part.strip().isdigit()), '')
                    
                    # Makale türü ve indeks
                    labels = article.find_elements(By.CSS_SELECTOR, "span.label")
                    article_type = ''
                    index_type = ''
                    
                    for label in labels:
                        if 'label-default' in label.get_attribute('class'):
                            article_type = label.text.strip()
                        elif 'label-success' in label.get_attribute('class'):
                            index_type = label.text.strip()
                    
                    article_info = {
                        'title': title,
                        'authors': authors,
                        'journal': journal,
                        'year': year,
                        'type': article_type,
                        'index': index_type
                    }
                    articles.append(article_info)
                    
                except Exception as e:
                    print(f"Makale işlenirken hata: {e}")
                    continue
                
            return articles
            
        except Exception as e:
            print(f"Makaleler çekilirken hata: {e}")
            return []

    def get_proceedings(self):
        """
        Akademisyenin bildirilerini çeker
        Returns:
            list: Bildiri bilgilerini içeren liste
        """
        try:
            # Bildiriler sekmesine tıkla
            proceedings_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li#proceedingMenu a")))
            proceedings_tab.click()
            time.sleep(5)
            
            proceedings = []
            proceeding_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.tab-content div.tab-pane.active tr")
            
            for proceeding in proceeding_elements:
                try:
                    # Başlık
                    title = proceeding.find_element(By.CSS_SELECTOR, "strong").text.strip()
                    
                    # Yazarlar - popoverData class'ına sahip a etiketlerini bul
                    author_elements = proceeding.find_elements(By.CSS_SELECTOR, "a.popoverData")
                    authors = ', '.join([author.text.strip() for author in author_elements])
                    
                    # Konferans bilgileri
                    pub_info = proceeding.find_element(By.CSS_SELECTOR, "td p:last-of-type").text.strip()
                    pub_parts = pub_info.split(',')
                    
                    # Konferans adı
                    conference = next((part.split(':')[1].strip() for part in pub_parts if 'Yayın Yeri:' in part), '')
                    
                    # Yıl
                    year = next((part.strip() for part in pub_parts if part.strip().isdigit()), '')
                    
                    # Bildiri türü bilgisini al
                    labels = proceeding.find_elements(By.CSS_SELECTOR, "span.label")
                    proceeding_type = ''
                    
                    for label in labels:
                        if 'label-success' in label.get_attribute('class'):
                            proceeding_type = label.text.strip()
                    
                    proceeding_info = {
                        'title': title,
                        'authors': authors,
                        'conference': conference.replace('Yayın Yeri:', '').strip(),
                        'year': year,
                        'type': proceeding_type
                    }
                    proceedings.append(proceeding_info)
                    
                except Exception as e:
                    continue
                
            return proceedings
            
        except Exception as e:
            print(f"Bildiriler çekilirken hata: {e}")
            return []

    def get_presentations(self, html_content):
        presentations = []
        soup = BeautifulSoup(html_content, 'html.parser')
        container = soup.find('div', class_='container-fluid')
        if not container:
            print("Container for presentations not found.")
            return presentations

        all_tab = container.find('div', id='all')
        if not all_tab:
            print("Tab for all presentations not found.")
            return presentations

        rows = all_tab.find_all('tr')
        for row in rows:
            try:
                title = row.find('span', class_='baslika').find('strong').text.strip()
            except Exception as e:
                print(f"Title not found: {e}")
                continue

            try:
                authors = ', '.join([a.text.strip() for a in row.find_all('a', class_='popoverData')])
            except Exception as e:
                print(f"Authors not found: {e}")
                authors = ''

            try:
                pub_info = row.find('span', class_='baslika').find_next_sibling(text=True).strip()
            except Exception as e:
                print(f"Publication info not found: {e}")
                pub_info = ''

            try:
                labels = ', '.join([label.text.strip() for label in row.find_all('span', class_='label')])
            except Exception as e:
                print(f"Labels not found: {e}")
                labels = ''

            presentations.append({
                'title': title,
                'authors': authors,
                'publication_info': pub_info,
                'labels': labels
            })

        return presentations

    def get_articles_from_html(self, html_content):
        articles = []
        soup = BeautifulSoup(html_content, 'html.parser')
        tbody = soup.find('tbody', class_='searchable')
        if not tbody:
            print("Table body for articles not found.")
            return articles

        rows = tbody.find_all('tr')
        for row in rows:
            try:
                title_element = row.find('span', class_='baslika').find('strong').find('a')
                title = title_element.text.strip()
                link = title_element['href']
            except Exception as e:
                print(f"Title or link not found: {e}")
                continue

            try:
                authors = ', '.join([a.text.strip() for a in row.find_all('a', class_='popoverData')])
            except Exception as e:
                print(f"Authors not found: {e}")
                authors = ''

            try:
                pub_info = row.find('span', class_='baslika').find_next_sibling(text=True).strip()
                pub_parts = pub_info.split(',')
                publication_place = pub_parts[0].replace('Yayın Yeri:', '').strip()
                year = pub_parts[1].strip()
            except Exception as e:
                print(f"Publication info not found: {e}")
                publication_place = ''
                year = ''

            try:
                labels = ', '.join([label.text.strip() for label in row.find_all('span', class_='label')])
            except Exception as e:
                print(f"Labels not found: {e}")
                labels = ''

            try:
                doi_link = row.find('a', href=True, target='_blank')['href']
            except Exception as e:
                print(f"DOI link not found: {e}")
                doi_link = ''

            articles.append({
                'title': title,
                'link': link,
                'authors': authors,
                'publication_place': publication_place,
                'year': year,
                'labels': labels,
                'doi_link': doi_link
            })

        return articles

    def get_books_from_html(self, html_content):
        books = []
        soup = BeautifulSoup(html_content, 'html.parser')
        projects_div = soup.find('div', class_='projects')
        if not projects_div:
            print("Projects container for books not found.")
            return books

        rows = projects_div.find_all('div', class_='row')
        for row in rows:
            try:
                title = row.find('strong').text.strip()
            except Exception as e:
                print(f"Title not found: {e}")
                continue

            try:
                details = row.find('p').text.strip()
                details_parts = details.split(',')
                authors = details_parts[0].strip()
                publication_place = details_parts[1].replace('Yayın Yeri:', '').strip()
                edition = details_parts[2].replace('Basım sayısı:', '').strip()
                page_count = details_parts[3].replace('Sayfa sayısı:', '').strip()
                isbn = details_parts[4].replace('ISBN:', '').strip()
            except Exception as e:
                print(f"Details not found: {e}")
                authors = publication_place = edition = page_count = isbn = ''

            try:
                year = row.find('span', class_='label-info').text.strip()
            except Exception as e:
                print(f"Year not found: {e}")
                year = ''

            try:
                book_type = row.find('span', class_='label-primary').text.strip()
            except Exception as e:
                print(f"Book type not found: {e}")
                book_type = ''

            books.append({
                'title': title,
                'authors': authors,
                'publication_place': publication_place,
                'edition': edition,
                'page_count': page_count,
                'isbn': isbn,
                'year': year,
                'type': book_type
            })

        return books

    def scrape_all(self):
        """
        Tüm akademik bilgileri çeker ve sonuçları döndürür
        Returns:
            dict: Tüm akademik bilgileri içeren sözlük
        """
        try:
            self.setup_driver()
            
            results = {
                'profile_info': self.get_profile_info(),
                'academic_info': self.get_academic_info(),
                'books': self.get_books(),
                'articles': self.get_articles(),
                'proceedings': self.get_proceedings()
            }
            
            # Debug için verileri yazdır
            print("\nÇekilen veriler:")
            print("Profil Bilgileri:", results['profile_info'])
            print("Akademik Bilgiler:", results['academic_info'])
            print("\nKitaplar:", results['books'])
            print("\nMakaleler:", results['articles'])
            print("\nBildiriler:", results['proceedings'])
            
            return results
        finally:
            if self.driver:
                self.driver.quit()

    def get_profile_info(self):
        """
        Akademisyenin profil bilgilerini ve resmini çeker
        """
        try:
            profile = {}
            
            # Ad Soyad ve unvan
            name_element = self.driver.find_element(By.CSS_SELECTOR, "div.col-lg-6.col-md-6.col-sm-10.col-xs-12 h4")
            if name_element:
                profile['name'] = name_element.text.strip()
            
            # Kurum ve bölüm bilgisi
            department_element = self.driver.find_element(By.CSS_SELECTOR, "div.col-lg-6.col-md-6.col-sm-10.col-xs-12")
            if department_element:
                # İlk metin bloğunu al (h4'ten sonraki ilk text node)
                text_nodes = [node for node in department_element.find_elements(By.XPATH, "./text()")]
                if text_nodes:
                    department_text = text_nodes[0].text.strip()
                    profile['department_info'] = department_text
            
            # Temel alan ve uzmanlık alanları
            labels = self.driver.find_elements(By.CSS_SELECTOR, "div.col-lg-6.col-md-6.col-sm-10.col-xs-12 span.label")
            if labels:
                areas = []
                for label in labels:
                    label_class = label.get_attribute('class')
                    label_text = label.text.strip()
                    if 'label-success' in label_class:
                        areas.append(('Temel Alan', label_text))
                    elif 'label-primary' in label_class:
                        areas.append(('Uzmanlık Alanı', label_text))
                profile['areas'] = areas
            
            # Araştırma alanları
            research_areas = []
            research_text = department_element.text
            if research_text:
                # Son satırdan araştırma alanlarını çek
                lines = research_text.split('\n')
                for line in lines:
                    if any(keyword in line for keyword in ['Ağları', 'Zeka', 'İşleme']):
                        areas = [area.strip() for area in line.split(',')]
                        research_areas.extend(areas)
            profile['research_areas'] = research_areas
            
            # Profil resmi
            try:
                img_element = self.driver.find_element(By.CSS_SELECTOR, "div.col-lg-2.col-md-2.col-sm-2.col-xs-0.text-center img.img-circle")
                if img_element:
                    img_src = img_element.get_attribute('src')
                    if img_src.startswith('data:image'):
                        import base64
                        img_data = img_src.split(',')[1]
                        with open('profile_photo.jpg', 'wb') as f:
                            f.write(base64.b64decode(img_data))
                        profile['image_path'] = 'profile_photo.jpg'
            except Exception as e:
                print(f"Profil resmi çekilirken hata: {e}")
            
            return profile
        except Exception as e:
            print(f"Profil bilgileri çekilirken hata: {e}")
            return {}

    def save_to_word(self, data, filename='academic_info.docx'):
        """
        Verileri Word dosyasına kaydeder
        Args:
            data: Kaydedilecek veriler
            filename: Kaydedilecek dosya adı
        """
        doc = Document()
        
        # Başlık stilini ayarla
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(11)
        
        # Akademik Görevler
        if 'academic_info' in data and data['academic_info']:
            doc.add_heading('Akademik Görevler', level=1)
            if 'duties' in data['academic_info']:
                for duty in data['academic_info']['duties']:
                    doc.add_paragraph(duty)
            doc.add_page_break()
            
            # Öğrenim Bilgileri
            doc.add_heading('Öğrenim Bilgileri', level=1)
            if 'education' in data['academic_info']:
                for edu in data['academic_info']['education']:
                    doc.add_paragraph(edu)
            doc.add_page_break()
        
        # Kitaplar
        if 'books' in data and data['books']:
            doc.add_heading('Kitaplar', level=1)
            for book in data['books']:
                p = doc.add_paragraph()
                p.add_run(f"Başlık: {book['title']}").bold = True
                p.add_run(f"\nYazarlar: {book['authors']}")
                p.add_run(f"\nYayınevi: {book['publisher']}")
                if 'year' in book:
                    p.add_run(f"\nYıl: {book['year']}")
                doc.add_paragraph()
            doc.add_page_break()
        
        # Makaleler
        if 'articles' in data and data['articles']:
            doc.add_heading('Makaleler', level=1)
            for article in data['articles']:
                p = doc.add_paragraph()
                p.add_run(f"Başlık: {article['title']}").bold = True
                p.add_run(f"\nYazarlar: {article['authors']}")
                p.add_run(f"\nDergi: {article['journal']}")
                p.add_run(f"\nYıl: {article['year']}")
                p.add_run(f"\nTür: {article['type']}")
                p.add_run(f"\nİndeks: {article['index']}")
                doc.add_paragraph()
            doc.add_page_break()
        
        # Bildiriler
        if 'proceedings' in data and data['proceedings']:
            doc.add_heading('Bildiriler', level=1)
            for proc in data['proceedings']:
                p = doc.add_paragraph()
                p.add_run(f"Başlık: {proc['title']}").bold = True
                p.add_run(f"\nYazarlar: {proc['authors']}")
                p.add_run(f"\nKonferans: {proc['conference']}")
                p.add_run(f"\nYıl: {proc['year']}")
                p.add_run(f"\nTür: {proc['type']}")
                doc.add_paragraph()
        
        # Dosyayı kaydet
        doc.save(filename)
        print(f"Word dosyası başarıyla oluşturuldu: {filename}") 
