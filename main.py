import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os
import json
import time
from datetime import datetime

# === Load credentials from environment ===
creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
creds_dict = json.loads(creds_json)
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# === Access spreadsheet ===
spreadsheet_name = '1n-Im7JcUfKlpXeiuPIdylAj-V2O6Rqe6bsd7m_mzG_A'  # Ganti sesuai spreadsheet kamu
sheet = client.open(spreadsheet_name).sheet1

# === Telegram setup ===
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
TELEGRAM_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

# === Notifikasi limit dan delay ===
MAX_ALERTS = 10
alerts_sent = 0

def send_notifications():
    global alerts_sent
    data = sheet.get_all_values()
    print(f'📊 Total baris: {len(data)} | {datetime.now()}')

    for i, row in enumerate(data[1:], start=2):  # Skip header
        if i <= 1000:
            continue
        if alerts_sent >= MAX_ALERTS:
            print(f'⚠️ Batas notifikasi tercapai: {MAX_ALERTS}')
            break

        kolomF = row[5].strip() if len(row) > 5 else ''
        other_filled = any(cell.strip() for cell in row[:5])

        if kolomF == '' and other_filled:
            nama = row[1] if len(row) > 1 else '(nama kosong)'
            masalah = row[2] if len(row) > 2 else '(masalah kosong)'
            message = f'🚨 Baris {i} belum diisi kolom F!\nNama: {nama}\nMasalah: {masalah}'

            response = requests.post(TELEGRAM_URL, data={'chat_id': CHAT_ID, 'text': message})
            if response.status_code == 200:
                print(f'✅ Notifikasi dikirim {datetime.now()} untuk baris {i}')
            else:
                print(f'❌ Gagal kirim notifikasi untuk baris {i}: {response.text}')

            alerts_sent += 1
            time.sleep(1)  # Delay antar notifikasi

if __name__ == '__main__':
    try:
        send_notifications()
    except Exception as e:
        print(f'🔥 Error saat menjalankan script: {e}')