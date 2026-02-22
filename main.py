"""
Main application module for the CS2 Market Arbitrage Tool.
Entry point for the PyQt5 GUI.
"""
import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QProgressBar, QScrollArea, QFrame, QListWidget, 
                             QGraphicsDropShadowEffect, QListWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt, QRegExp, QSize
from PyQt5.QtGui import QCursor, QColor, QRegExpValidator, QPixmap, QIcon

from config import GLOBAL_STYLE
from scraper import SkinScraper
from workers import DBWorker, ScraperWorker, IconLoader, SingleImageLoader


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scraper = SkinScraper()
        self.skin_database = []
        self.image_cache = {} 
        self.icon_loader = None
        self.single_img_loader = None
        
        self.setWindowTitle("CS2 Market Arbitrage Pro")
        self.setMinimumSize(1600, 900)
        self.setWindowIcon(QIcon("logo.png"))
        self.setStyleSheet(GLOBAL_STYLE)
        
        self.setup_ui()
        
        # Initialize background database fetch
        self.db_thread = DBWorker()
        self.db_thread.db_ready.connect(self.on_db_loaded)
        self.db_thread.start()

    def on_db_loaded(self, db_list):
        self.skin_database = db_list

    def setup_ui(self):
        """Constructs the main user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- Top Dashboard Panel ---
        self.header_frame = QFrame()
        self.header_frame.setObjectName("HeaderPanel")
        self.header_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15); shadow.setColor(QColor(0, 0, 0, 80)); shadow.setOffset(0, 5)
        self.header_frame.setGraphicsEffect(shadow)

        header_main_layout = QHBoxLayout(self.header_frame)
        header_main_layout.setContentsMargins(30, 20, 30, 20)
        header_main_layout.setSpacing(40)

        # Left: Dynamic Image Preview
        self.lbl_item_image = QLabel()
        self.lbl_item_image.setFixedSize(140, 100)
        self.lbl_item_image.setAlignment(Qt.AlignCenter)
        self.lbl_item_image.setStyleSheet("background-color: transparent; border: none;")
        header_main_layout.addWidget(self.lbl_item_image)

        # Center: Main Inputs & Title
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        self.lbl_title = QLabel("QES \nTRADE TERMINAL")
        self.lbl_title.setObjectName("AppTitle")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        
        title_glow = QGraphicsDropShadowEffect()
        title_glow.setBlurRadius(15); title_glow.setColor(QColor(0, 230, 118, 100)); title_glow.setOffset(0, 0)
        self.lbl_title.setGraphicsEffect(title_glow)
        right_layout.addWidget(self.lbl_title)

        input_container = QHBoxLayout()
        input_container.setSpacing(10)

        label_style = "color: #9E9E9E; font-size: 11px; font-weight: bold; margin-bottom: 0px;"
        INPUT_HEIGHT = 34 
        number_validator = QRegExpValidator(QRegExp(r"^[0-9]*[.,]?[0-9]*$"))

        vbox_search = QVBoxLayout(); vbox_search.setSpacing(2)
        lbl_search = QLabel("ITEM NAME"); lbl_search.setStyleSheet(label_style)
        self.entry_search = QLineEdit()
        self.entry_search.setPlaceholderText("e.g., AK-47 | Redline (Field-Tested)")
        self.entry_search.setMinimumWidth(380)
        self.entry_search.setFixedHeight(INPUT_HEIGHT)
        self.entry_search.textChanged.connect(self.on_search_type)
        vbox_search.addWidget(lbl_search); vbox_search.addWidget(self.entry_search)

        vbox_price = QVBoxLayout(); vbox_price.setSpacing(2)
        lbl_price = QLabel("SELLING PRICE ($)"); lbl_price.setStyleSheet(label_style)
        self.entry_price = QLineEdit()
        self.entry_price.setPlaceholderText("Sell for...")
        self.entry_price.setFixedWidth(110)
        self.entry_price.setFixedHeight(INPUT_HEIGHT)
        self.entry_price.setValidator(number_validator)
        vbox_price.addWidget(lbl_price); vbox_price.addWidget(self.entry_price)

        vbox_fee = QVBoxLayout(); vbox_fee.setSpacing(2)
        lbl_fee = QLabel("FEE (%)"); lbl_fee.setStyleSheet(label_style)
        self.entry_fee = QLineEdit()
        self.entry_fee.setPlaceholderText("0.0")
        self.entry_fee.setFixedWidth(70)
        self.entry_fee.setFixedHeight(INPUT_HEIGHT)
        self.entry_fee.setValidator(number_validator)
        vbox_fee.addWidget(lbl_fee); vbox_fee.addWidget(self.entry_fee)

        vbox_btn = QVBoxLayout(); vbox_btn.setSpacing(0)
        vbox_btn.setAlignment(Qt.AlignBottom)
        self.btn_search = QPushButton("CALCULATE DEALS")
        self.btn_search.setObjectName("ActionBtn")
        self.btn_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_search.setFixedWidth(160)
        self.btn_search.setFixedHeight(INPUT_HEIGHT)
        self.btn_search.clicked.connect(self.start_search)
        vbox_btn.addWidget(self.btn_search)

        input_container.addStretch()
        input_container.addLayout(vbox_search)
        input_container.addLayout(vbox_price)
        input_container.addLayout(vbox_fee)
        input_container.addLayout(vbox_btn)
        input_container.addStretch()
        
        right_layout.addLayout(input_container)
        header_main_layout.addLayout(right_layout)
        
        # Right: App Logo
        self.lbl_app_logo = QLabel()
        self.lbl_app_logo.setFixedSize(200, 140) 
        self.lbl_app_logo.setAlignment(Qt.AlignCenter)
        
        logo_pixmap = QPixmap("logo.png")
        if not logo_pixmap.isNull():
             self.lbl_app_logo.setPixmap(logo_pixmap.scaled(200, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_main_layout.addWidget(self.lbl_app_logo)

        main_layout.addWidget(self.header_frame, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # --- Autocomplete List (Floating Widget) ---
        self.suggestion_list = QListWidget(self)
        self.suggestion_list.setIconSize(QSize(50, 38)) 
        self.suggestion_list.setStyleSheet("""
            QListWidget {
                background-color: #2A2A35; border: 1px solid #3d3d3d; 
                border-radius: 6px; padding: 2px; font-size: 14px; color: #E0E0E0;
            }
            QListWidget::item { padding: 4px; border-bottom: 1px solid #32323E; border-radius: 4px; }
            QListWidget::item:hover { background-color: #00C853; color: black; font-weight: bold;}
        """)
        list_shadow = QGraphicsDropShadowEffect()
        list_shadow.setBlurRadius(15); list_shadow.setColor(QColor(0,0,0,150)); list_shadow.setOffset(0, 5)
        self.suggestion_list.setGraphicsEffect(list_shadow)
        self.suggestion_list.hide()
        self.suggestion_list.itemClicked.connect(self.select_suggestion)

        # --- Loading & Results Area ---
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar { border: none; background-color: #2A2A35; border-radius: 2px; height: 3px; }
            QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00C853, stop:1 #2979FF); border-radius: 2px;}
        """)
        self.progress.setRange(0, 0)
        self.progress.hide()
        main_layout.addWidget(self.progress)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.result_container = QWidget()
        self.result_container.setStyleSheet("background-color: transparent;")
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setAlignment(Qt.AlignTop)
        self.result_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.result_container)
        main_layout.addWidget(self.scroll_area)

    # --- UI Logic Methods ---
    def on_search_type(self):
        query = self.entry_search.text().lower().strip()
        
        if len(query) < 2 or not self.skin_database:
            self.suggestion_list.hide(); return
            
        query_words = query.split()
        matches = [skin for skin in self.skin_database if all(word in skin['name'].lower() for word in query_words)]
        matches.sort(key=lambda x: len(x['name']))
        matches = matches[:25]
        
        if not matches: self.suggestion_list.hide(); return

        self.suggestion_list.clear()
        
        if self.icon_loader and self.icon_loader.isRunning():
            self.icon_loader.cancel()
            
        requests_list = []
        for idx, skin in enumerate(matches):
            item = QListWidgetItem(skin['name'])
            self.suggestion_list.addItem(item)
            if skin['image']:
                requests_list.append((idx, skin['image']))

        pos = self.entry_search.mapTo(self, self.entry_search.rect().bottomLeft())
        self.suggestion_list.setGeometry(pos.x(), pos.y() + 2, self.entry_search.width(), 300)
        self.suggestion_list.show(); self.suggestion_list.raise_()
        
        if requests_list:
            self.icon_loader = IconLoader(requests_list, self.image_cache)
            self.icon_loader.icon_loaded.connect(self.set_item_icon)
            self.icon_loader.start()

    def set_item_icon(self, row, url, image_data):
        self.image_cache[url] = image_data 
        if row < self.suggestion_list.count():
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            icon = QIcon(pixmap)
            item = self.suggestion_list.item(row)
            if item: item.setIcon(icon)

    def update_header_image(self, skin_name):
        base_name = re.sub(r'\(.*?\)', '', skin_name).strip().lower()
        if len(base_name) < 2: return
            
        skin_data = None
        for s in self.skin_database:
            if s['name'].lower() == base_name:
                skin_data = s
                break
                
        if not skin_data:
            words = base_name.split()
            for s in self.skin_database:
                if all(w in s['name'].lower() for w in words):
                    skin_data = s
                    break

        if skin_data and skin_data.get('image'):
            url = skin_data['image']
            if url in self.image_cache:
                self.display_header_image(self.image_cache[url])
            else:
                self.single_img_loader = SingleImageLoader(url)
                self.single_img_loader.loaded.connect(self.display_header_image)
                self.single_img_loader.start()
        else:
            self.lbl_item_image.clear()
            self.lbl_item_image.setStyleSheet("background-color: transparent; border: none;")

    def display_header_image(self, image_data):
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.lbl_item_image.setPixmap(pixmap.scaled(130, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lbl_item_image.setStyleSheet("background-color: transparent; border: none;")

    def select_suggestion(self, item):
        selected_name = item.text()
        self.entry_search.setText(selected_name)
        self.suggestion_list.hide()
        self.entry_price.setFocus()
        self.update_header_image(selected_name)

    def mousePressEvent(self, event):
        self.suggestion_list.hide()
        super().mousePressEvent(event)

    def start_search(self):
        self.suggestion_list.hide()
        name = self.entry_search.text()
        if not name: return
        
        self.update_header_image(name)
        
        self.btn_search.setText("SCANNING..."); self.btn_search.setEnabled(False); self.progress.show()
        for i in reversed(range(self.result_layout.count())): 
            widget = self.result_layout.itemAt(i).widget()
            if widget: widget.deleteLater()
            
        self.worker = ScraperWorker(self.scraper, name)
        self.worker.result_ready.connect(self.display_results)
        self.worker.start()

    def display_results(self, data):
        self.progress.hide()
        self.btn_search.setText("CALCULATE DEALS")
        self.btn_search.setEnabled(True)
        
        if "error" in data:
            err_lbl = QLabel(f"⚠️ {data['error']}")
            err_lbl.setStyleSheet("color: #FF5555; font-size: 16px; font-weight: bold; padding: 10px;")
            err_lbl.setAlignment(Qt.AlignCenter)
            self.result_layout.addWidget(err_lbl); return

        offers_sorted = sorted(data["offers"], key=lambda x: x['price'])
        try: price_val = float(self.entry_price.text().replace(",", ".")) if self.entry_price.text() else 0.0
        except ValueError: price_val = 0.0
        try: fee_val = float(self.entry_fee.text().replace(",", ".")) if self.entry_fee.text() else 0.0
        except ValueError: fee_val = 0.0
        
        net_income = price_val * (1 - (fee_val / 100))

        # Best Deal Banner Generation
        banner = QFrame()
        banner.setObjectName("BestDealBanner")
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(20, 15, 20, 15)
        
        best_info = QVBoxLayout()
        lbl_best_title = QLabel("🔥 BEST PRICE FOUND")
        lbl_best_title.setStyleSheet("color: #00E676; font-weight: 900; font-size: 12px; letter-spacing: 1px;")
        lbl_best_site = QLabel(offers_sorted[0]['site'])
        lbl_best_site.setStyleSheet("color: white; font-weight: bold; font-size: 24px;")
        best_info.addWidget(lbl_best_title); best_info.addWidget(lbl_best_site)
        
        lbl_best_price = QLabel(f"${offers_sorted[0]['price']:.2f}")
        lbl_best_price.setStyleSheet("color: #00E676; font-weight: 900; font-size: 36px;")
        
        banner_layout.addLayout(best_info); banner_layout.addStretch(); banner_layout.addWidget(lbl_best_price)
        self.result_layout.addWidget(banner)

        if price_val > 0:
            net_lbl = QLabel(f"Your Net Income (after {fee_val}% fee): <b>${net_income:.2f}</b>")
            net_lbl.setStyleSheet("color: #90CAF9; font-size: 14px; margin-top: 5px; margin-left: 5px;")
            self.result_layout.addWidget(net_lbl)

        # Iterate and render results
        for idx, offer in enumerate(offers_sorted):
            card = QFrame()
            card.setObjectName("ResultCard")
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(20, 10, 20, 10)

            rank_lbl = QLabel(f"#{idx+1}")
            rank_lbl.setStyleSheet("color: #757575; font-size: 16px; font-weight: bold;")
            rank_lbl.setFixedWidth(30)
            
            site_lbl = QLabel(offer['site'])
            site_lbl.setStyleSheet(f"color: {'#00E676' if idx==0 else 'white'}; font-size: 16px; font-weight: 600;")
            
            price_info = QVBoxLayout()
            price_info.setAlignment(Qt.AlignRight)
            price_lbl = QLabel(f"${offer['price']:.2f}")
            price_lbl.setStyleSheet("color: #FFB74D; font-size: 18px; font-weight: 900;")
            price_info.addWidget(price_lbl)

            if net_income > 0:
                profit = net_income - offer['price']
                
                if profit > 0:
                    p_text = f"+${profit:.2f} Profit"
                    p_color = "#00E676" 
                elif profit < 0:
                    p_text = f"-${abs(profit):.2f} Loss" 
                    p_color = "#FF5555" 
                else:
                    p_text = "$0.00 Break Even"
                    p_color = "#9E9E9E" 
                    
                profit_lbl = QLabel(p_text)
                profit_lbl.setStyleSheet(f"color: {p_color}; font-size: 13px; font-weight: bold;")
                profit_lbl.setAlignment(Qt.AlignRight)
                price_info.addWidget(profit_lbl)

            card_layout.addWidget(rank_lbl)
            card_layout.addWidget(site_lbl)
            card_layout.addStretch()
            card_layout.addLayout(price_info)
            self.result_layout.addWidget(card)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if hasattr(Qt, 'AA_EnableHighDpiScaling'): 
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'): 
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
    window = App()
    window.show()
    sys.exit(app.exec_())