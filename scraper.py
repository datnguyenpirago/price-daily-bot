# scraper.py
import requests
from bs4 import BeautifulSoup
from config import URLS

def get_gold_vn():
    url = URLS['gold_vn']
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Lấy bảng giá vàng mới
        table = soup.find('table', class_='gold-table-content')
        if not table:
            return 'Không tìm thấy bảng giá vàng!'
        rows = table.find_all('tr')
        result_lines = []
        for row in rows:
            row_text = row.get_text()
            if 'Nhẫn ép vỉ Kim Gia Bảo' in row_text or 'Vàng miếng SJC' in row_text:
                cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                if cols:
                    result_lines.append(' | '.join(cols))
        if result_lines:
            return '\n'.join(result_lines)
        return 'Không tìm thấy dữ liệu bảng giá vàng!'

    except Exception as e:
        return f'Lỗi lấy giá vàng VN: {e}'

def get_gold_world():
    url = URLS['gold_world']
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Trên investing.com, giá vàng thường nằm trong thẻ <span> có data-test="instrument-price-last"
        price_div = soup.find('div', attrs={'data-test': 'instrument-price-last'})
        price_change = soup.find('span', attrs={'data-test': 'instrument-price-change'})
        price_percent = soup.find('span', attrs={'data-test': 'instrument-price-change-percent'})
        if price_div:
            change_str = ''
            if price_change:
                change_str += f" {price_change.text.strip()}"
            if price_percent:
                change_str += f" {price_percent.text.strip()}"
            change_str = change_str.strip()
            if change_str:
                change_str = f" ({change_str})"
            return f"Giá vàng thế giới: {price_div.text.strip()} USD/oz{change_str}"
        # Nếu không tìm thấy, trả về lỗi
        return 'Không tìm thấy giá vàng thế giới!'
    except Exception as e:
        return f'Lỗi lấy giá vàng TG: {e}'

def get_bitcoin():
    url = URLS['bitcoin']
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_span = soup.find('span', class_='sc-65e7f566-0 WXGwg base-text', attrs={'data-test': 'text-cdp-price-display'})
        percent_div = soup.find('div', attrs={'data-role': 'percentage-value'})
        percent_value = ''
        if percent_div:
            percent_p = percent_div.find('p', class_='sc-71024e3e-0 sc-8ec8b63a-1 bgxfSG icQYnE change-text')
            if percent_p:
                percent_value = percent_p.get_text(strip=True)
                # Kiểm tra nếu là tăng (color="green") thì thêm dấu +
                if percent_p.get('color') == 'green' and not percent_value.startswith('+'):
                    # Tìm vị trí phần trăm
                    import re
                    percent_value = re.sub(r'([0-9.]+%)', r'+\1', percent_value)
        if price_span:
            result = f"Giá Bitcoin: {price_span.text.strip()}"
            if percent_value:
                result += f" ({percent_value})"
            return result
        return 'Không tìm thấy giá Bitcoin!'
    except Exception as e:
        return f'Lỗi lấy giá BTC: {e}'

def get_stock_us():
    url = URLS['stock_us']
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_div = soup.find('div', attrs={'data-test': 'instrument-price-last'})

        

        price_change = soup.find('span', attrs={'data-test': 'instrument-price-change'})
        price_percent = soup.find('span', attrs={'data-test': 'instrument-price-change-percent'})
        if price_div:
            change_str = ''
            if price_change:
                change_str += f" {price_change.text.strip()}"
            if price_percent:
                change_str += f" {price_percent.text.strip()}"
            change_str = change_str.strip()
            if change_str:
                change_str = f" ({change_str})"
            return f"Chỉ số US: {price_div.text.strip()}{change_str}"
        return 'Không tìm thấy giá chỉ số US!'
    except Exception as e:
        return f'Lỗi lấy giá chỉ số US: {e}'

def get_stock_vn():
    url = URLS['stock_vn']
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Lấy giá từ <h2 id="stockprice"> <span class="txt-green price">...
        h2_tag = soup.find('h2', id='stockprice')
        stockchange_div = soup.find('div', id='stockchange')
        change_str = ''
        if stockchange_div:
            change_str = f" ({stockchange_div.text.strip()})"
        if h2_tag:
            price_span = h2_tag.find('span', class_='txt-green price')
            if price_span:
                return f"Giá cổ phiếu VN: {price_span.text.strip()}{change_str}"
        # Lấy giá cổ phiếu tại bảng giá (class 'price' hoặc 'price-current')
        price_tag = soup.find('td', class_='price') or soup.find('td', class_='price-current')
        if price_tag:
            return f"Giá cổ phiếu VN (AAA): {price_tag.text.strip()}{change_str}"
        # Nếu không tìm thấy, thử lấy giá từ thẻ strong hoặc span
        price_alt = soup.find('strong', class_='stock-price') or soup.find('span', class_='stock-price')
        if price_alt:
            return f"Giá cổ phiếu AAA: {price_alt.text.strip()}{change_str}"
        return 'Không tìm thấy giá cổ phiếu VN!'
    except Exception as e:
        return f'Lỗi lấy giá cổ phiếu VN: {e}'
