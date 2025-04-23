import os

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# --- URLS ---
URLS = {
    'gold_vn': 'https://www.baotinmanhhai.vn/',
    'gold_world': 'https://vn.investing.com/commodities/gold',
    'bitcoin': 'https://coinmarketcap.com/currencies/bitcoin/',
    'stock_us': 'https://vn.investing.com/indices/us-30',
    'stock_vn': 'https://finance.vietstock.vn/AAA/ho-so-doanh-nghiep.htm'  # ví dụ mã VCB
}
