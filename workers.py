"""
PyQt QThread workers to handle asynchronous tasks like API calls and image loading.
"""
import requests
from PyQt5.QtCore import QThread, pyqtSignal

class ScraperWorker(QThread):
    """Executes the scraping process in the background."""
    result_ready = pyqtSignal(dict)
    
    def __init__(self, scraper, name):
        super().__init__()
        self.scraper = scraper
        self.name = name
        
    def run(self):
        res = self.scraper.fetch_prices(self.name)
        self.result_ready.emit(res)

class DBWorker(QThread):
    """Fetches the comprehensive item database from the public API."""
    db_ready = pyqtSignal(list)
    
    def run(self):
        try:
            url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/all.json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                temp_db = {}
                for item in data.values():
                    if isinstance(item, dict) and 'name' in item:
                        clean_name = item['name'].replace("★ ", "").strip()
                        if clean_name not in temp_db:
                            image_url = item.get('image') or item.get('image_url') or item.get('icon_url') or ""
                            temp_db[clean_name] = image_url
                
                db_list = [{'name': k, 'image': v} for k, v in temp_db.items()]
                self.db_ready.emit(db_list)
        except Exception as e: 
            print(f"DBWorker Error: {e}")

class IconLoader(QThread):
    """Asynchronously loads multiple thumbnail icons for autocomplete suggestions."""
    icon_loaded = pyqtSignal(int, str, bytes)
    
    def __init__(self, requests_list, cache):
        super().__init__()
        self.requests_list = requests_list
        self.cache = cache
        self.is_cancelled = False
        
    def run(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        for idx, url in self.requests_list:
            if self.is_cancelled: return
            if url in self.cache:
                self.icon_loaded.emit(idx, url, self.cache[url])
                continue
            try:
                resp = requests.get(url, headers=headers, timeout=3)
                if resp.status_code == 200:
                    self.icon_loaded.emit(idx, url, resp.content)
            except Exception: pass
            
    def cancel(self): 
        self.is_cancelled = True

class SingleImageLoader(QThread):
    """Fetches a single high-resolution image for the header preview."""
    loaded = pyqtSignal(bytes)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        
    def run(self):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            resp = requests.get(self.url, headers=headers, timeout=5)
            if resp.status_code == 200:
                self.loaded.emit(resp.content)
        except Exception: pass