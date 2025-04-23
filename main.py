# main.py
import schedule
import time
from scraper import get_gold_vn, get_gold_world, get_bitcoin, get_stock_us, get_stock_vn
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import requests

def compose_message():
    from datetime import datetime
    now = datetime.now()
    date_str = now.strftime('%d/%m/%Y')
    msg = f'BẢN TIN GIÁ ({date_str}):\n'
    msg += f"\nVàng trong nước: {get_gold_vn()}"
    msg += f"\nVàng thế giới: {get_gold_world()}"
    msg += f"\nBitcoin: {get_bitcoin()}"
    msg += f"\nCổ phiếu Mỹ: {get_stock_us()}"
    msg += f"\nCổ phiếu VN: {get_stock_vn()}"
    return msg

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    requests.post(url, data=payload)

def job():
    msg = compose_message()
    send_telegram_message(msg)
    print('Da gui ban tin!')

if __name__ == '__main__':
    # Gửi thử bản tin ngay lập tức để kiểm tra
    job()
    # Nếu muốn tự động mỗi sáng, bỏ comment các dòng dưới:
    # schedule.every().day.at('07:00').do(job)
    # print('Dang chay he thong ban tin gia...')
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)
