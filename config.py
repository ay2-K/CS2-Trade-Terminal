"""
Configuration and styling constants for the CS2 Market Arbitrage Tool.
"""

TARGET_MARKETS = [
    "CS.MONEY", "WOW Skins", "UUSKINS", "SkinSwap", "Buff163", 
    "LIS-SKINS", "Skins.com", "DMarket", "Avan.market", "Waxpeer", 
    "Tradeit.gg", "Exeskins", "Skinvault", "ShadowPay", "Market.CSGO"
]

GLOBAL_STYLE = """
    QMainWindow { background-color: #121212; }
    QWidget { font-family: 'Segoe UI', Roboto, sans-serif; color: #E0E0E0; }
    
    QLabel#AppTitle {
        color: #00E676;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: 3px;
        margin-bottom: 5px;
    }
    
    QFrame#HeaderPanel, QFrame#ResultCard {
        background-color: #1E1E24;
        border-radius: 10px;
        border: 1px solid #2C2C34;
    }
    QFrame#BestDealBanner {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e3c2e, stop:1 #1E1E24);
        border-radius: 10px;
        border: 2px solid #00E676;
    }
    
    QLineEdit {
        background-color: #2A2A35;
        border: 1px solid #3d3d3d;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 13px;
        color: white;
    }
    QLineEdit:focus {
        border: 1px solid #00E676;
        background-color: #32323E;
    }
    QLineEdit::placeholder { color: #757575; }
    
    QPushButton#ActionBtn {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00C853, stop:1 #69F0AE);
        color: black;
        font-weight: bold;
        font-size: 13px;
        border-radius: 6px;
        padding: 6px 15px;
    }
    QPushButton#ActionBtn:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E676, stop:1 #B9F6CA); }
    QPushButton#ActionBtn:disabled { background: #2C2C34; color: #757575; }
    
    QScrollBar:vertical { border: none; background: #121212; width: 6px; border-radius: 3px; }
    QScrollBar::handle:vertical { background: #424242; min-height: 20px; border-radius: 3px; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
"""