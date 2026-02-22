"""
Web scraping module to fetch CS2 item prices from various marketplaces.
"""
import re
import ssl
import urllib3
import cloudscraper
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from config import TARGET_MARKETS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class StrongSSLAdapter(HTTPAdapter):
    """Custom SSL Adapter to handle legacy or strict SSL handshakes."""
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False 
        context.verify_mode = ssl.CERT_NONE
        try: 
            context.set_ciphers("DEFAULT@SECLEVEL=1")
        except Exception: 
            context.set_ciphers("DEFAULT")
        pool_kwargs['ssl_context'] = context
        super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)

class SkinScraper:
    """Core scraper engine utilizing cloudscraper to bypass anti-bot protections."""
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        self.scraper.mount('https://', StrongSSLAdapter())
        self.base_url = "https://csgoskins.gg/items"

    def parse_input(self, raw_name):
        """Formats the raw item name into a URL-friendly slug."""
        is_stattrak = "StatTrak" in raw_name
        is_souvenir = "Souvenir" in raw_name
        
        clean_name = raw_name.replace("★", "").replace("StatTrak™", "").replace("StatTrak", "").replace("Souvenir", "").strip()
        
        condition_slug = ""
        conditions_map = {
            "(Factory New)": "factory-new", "(Minimal Wear)": "minimal-wear",
            "(Field-Tested)": "field-tested", "(Well-Worn)": "well-worn", "(Battle-Scarred)": "battle-scarred"
        }
        
        for cond_text, slug in conditions_map.items():
            if clean_name.endswith(cond_text):
                condition_slug = slug
                clean_name = clean_name[:-len(cond_text)].strip()
                break
                
        clean_name = clean_name.replace("|", "").strip()
        name_slug = re.sub(r'\s+', '-', clean_name).lower()
        
        if is_stattrak: name_slug = f"stattrak-{name_slug}"
        if is_souvenir: name_slug = f"souvenir-{name_slug}"
            
        return name_slug, condition_slug

    def fetch_prices(self, raw_name):
        """Fetches pricing data from the target site."""
        name_slug, condition_slug = self.parse_input(raw_name)
        url = f"{self.base_url}/{name_slug}/{condition_slug}" if condition_slug else f"{self.base_url}/{name_slug}"
            
        try:
            response = self.scraper.get(url, timeout=20)
            if response.status_code == 404: 
                return {"error": f"Item not found!\n{url}"}
            elif response.status_code != 200: 
                return {"error": f"Site Error: {response.status_code}"}

            soup = BeautifulSoup(response.content, "html.parser")
            offers = []
            page_text = soup.get_text()

            for market in TARGET_MARKETS:
                if market.lower() not in page_text.lower(): continue
                market_tag = soup.find(string=lambda t: t and market.lower() in t.lower())
                if market_tag:
                    container = market_tag.find_parent("div") or market_tag.find_parent("tr")
                    if container:
                        price_tag = container.find_next(string=lambda t: t and "$" in t)
                        if not price_tag and container.find_parent():
                             price_tag = container.find_parent().find_next(string=lambda t: t and "$" in t)
                        if price_tag:
                            try:
                                p_val = float(price_tag.strip().replace("$", "").replace(",", ""))
                                offers.append({"site": market, "price": p_val})
                            except ValueError: continue
            return {"offers": offers} if offers else {"error": "No listings found."}
        except Exception as e: 
            return {"error": str(e)}