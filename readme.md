# 📬 Telegram Notifier via Google Sheets & GitHub Actions

Automated Telegram notifications based on Google Sheets data, triggered every 5 minutes using GitHub Actions. Designed for operational monitoring, this script alerts when specific rows are missing data in column F.

---

## 🚀 Features

- ⏱️ Scheduled execution every 5 minutes via GitHub Actions
- 📊 Reads data from Google Sheets using `gspread`
- 📲 Sends alerts to Telegram via bot API
- 🔐 Uses GitHub Secrets for secure credential management
- ✅ Filters only rows above index 1000, because below 1000 is not used anymore
- 🧠 Smart detection: alerts only when column F is empty but other columns are filled

---

## 📁 Project Structure
telegram_notifier/
├── main.py
├── requirements.txt
└── .github/workflows/notifier.yml