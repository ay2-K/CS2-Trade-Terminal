# 📈 CS2 Trade Terminal

* A high-performance, asynchronous desktop application built with PyQt5 to track and analyze Counter-Strike 2 skin prices across multiple third-party marketplaces for potential arbitrage opportunities.
# 🚀 Features
  * Real-Time Market Scraping: Fetches live pricing data from 15+ popular CS2 marketplaces simultaneously (CS.MONEY, DMarket, Buff163, SkinSwap, etc.).
  * Advanced Anti-Bot Bypass: Utilizes cloudscraper to navigate through basic Cloudflare protections and gather data securely.
  * Smart Auto-Complete & Fuzzy Search: Instantly search through a dynamic database of over 15,000 CS2 items including skins, stickers, agents, and cases.
  * Asynchronous Image Engine: Loads high-resolution item previews and thumbnails in the background (Threading) with a smart memory cache system, ensuring zero UI freezes.
  * Profit/Loss Calculator: Automatically calculates net income and profit margins based on user-defined selling prices and marketplace fees.
  * Modern UI/UX: A sleek, responsive, dark-themed dashboard built with PyQt5, featuring dynamic hover effects and absolute centering.

# 🛠️ Tech Stack
  * Language: Python 3.x
  * GUI Framework: PyQt5
  * Web Scraping: BeautifulSoup4, Requests, Cloudscraper
  * Architecture: Modular MVC-like structure (Separation of UI, Logic, and Network layers)
  * Concurrency: PyQt QThread and pyqtSignal for parallel processing

# ⚙️ Installation & Usage
  1. Clone the repository:
  git clone https://github.com/ay2-K/CS2-Trade-Terminal.git
  cd CS2-Trade-Terminal
  
  2. Install the required dependencies:
  pip install PyQt5 requests beautifulsoup4 cloudscraper urllib3
  
  3. Run the application:
  python main.py

# ⚠️ Legal Disclaimer (Strictly Educational)
This project is strictly for educational and academic purposes only.

No Commercial Use: This tool is open-source, completely free, and is not intended for commercial use or generating revenue.

Web Scraping Liability: The data aggregation methods used in this software may violate the Terms of Service (ToS) or robots.txt policies of certain third-party websites.

Zero Responsibility: The developer of this project assumes no responsibility or liability for how this code is used by others. Any legal issues, account bans, IP blacklisting, or financial losses incurred by utilizing this tool are solely the responsibility of the end-user.

Not Affiliated: This project is not affiliated with, endorsed by, or associated with Valve Corporation, Steam, csgoskins.gg, or any of the third-party marketplaces mentioned in the codebase. Counter-Strike and its assets are registered trademarks of Valve Corporation.

By downloading and using this software, you agree to these terms and acknowledge that you are using it at your own risk.
