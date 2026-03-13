import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def extract_data(base_url="https://fashion-studio.dicoding.dev", total_pages=50):
    print(f"Mulai mengambil data dari halaman 1 sampai {total_pages}...")
    products = []
    
    try:
        for page in range(1, total_pages + 1):
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}/page/{page}/" 
                
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                url = f"{base_url}/page{page}/"
                response = requests.get(url, timeout=10)
                
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all('div', class_='collection-card')
            
            for card in cards:
                title_elem = card.find('h3', class_='product-title')
                title = title_elem.text.strip() if title_elem else None
                
                price_span = card.find('span', class_='price')
                price_p = card.find('p', class_='price')
                price = price_span.text.strip() if price_span else (price_p.text.strip() if price_p else None)
                
                rating, colors, size, gender = None, None, None, None
                for p in card.find_all('p'):
                    text = p.text.strip()
                    if 'Rating:' in text: rating = text
                    elif 'Colors' in text: colors = text
                    elif 'Size:' in text: size = text
                    elif 'Gender:' in text: gender = text
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                products.append({
                    "Title": title, "Price": price, "Rating": rating,
                    "Colors": colors, "Size": size, "Gender": gender, "Timestamp": timestamp
                })
            
            time.sleep(1) 
            
        print(f"Selesai! Berhasil mengekstrak {len(products)} data mentah.")
        return products
    except Exception as e:
        print(f"[ERROR] Ekstraksi gagal pada halaman {page}: {e}")
        return None