import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
import os
import json

# === Setup Google Sheet Access ===
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# 📄 Load sheet
sheet_id = "1n-Im7JcUfKlpXeiuPIdylAj-V2O6Rqe6bsd7m_mzG_A"
sheet = client.open_by_key(sheet_id).worksheet("Form Responses 1")

# === Setup Telegram Bot ===
TOKEN = os.getenv('TELEGRAM_TOKEN')  # Set di Railway Environment Variables
CHAT_ID = os.getenv('CHAT_ID')       # Set di Railway Environment Variables

# === Fungsi Kirim Notifikasi ===
def send_notifications():
    data = sheet.get_all_values()

    for i, row in enumerate(data[1:], start=2):  # Skip header
        if i <= 1000:
            continue  # Lewati baris 1000 ke bawah
        
        kolomF = row[5].strip() if len(row) > 5 else ''
        other_filled = any(cell.strip() for cell in row[:5])

        if kolomF == '' and other_filled:
            transaksi = row[1] if len(row) > 1 else '(nomor transaksi kosong)'
            technician = row[2] if len(row) > 1 else '(technician kosong)'
            reason = row[3] if len(row) > 2 else '(masalah kosong)'
            message = f'🚨 Ada data baru di baris {i} belum diisi Statusnya!\nNomor Transaksi: {transaksi}\nTechnician: {technician}\nReason: {reason}'

            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
            payload = {'chat_id': CHAT_ID, 'text': message}
            response = requests.post(url, data=payload)

            if response.status_code == 200:
                print(f'✅ Notifikasi dikirim untuk baris {i}')
            else:
                print(f'❌ Gagal kirim notifikasi untuk baris {i}: {response.text}')

# === Loop Tiap 5 Menit ===
if __name__ == '__main__':
    while True:
        try:
            send_notifications()
        except Exception as e:
            print(f'⚠️ Error: {e}')
        time.sleep(300)  # Tunggu 5 menit