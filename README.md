[![Daily Stock Screener](https://github.com/dnielasher/idx-automated-screener/actions/workflows/daily_run.yml/badge.svg)](https://github.com/dnielasher/idx-automated-screener/actions/workflows/daily_run.yml)

# 📈 IDX Automated Stock Screener

**Automated Trading Bot** yang memindai saham LQ45 di Bursa Efek Indonesia (IDX) setiap hari untuk mencari sinyal beli berdasarkan Analisis Teknikal Kuantitatif.

## 🚀 Fitur Utama
* **Daily Automation:** Berjalan otomatis setiap hari Senin-Jumat pukul 16:00 WIB (setelah pasar tutup) menggunakan **GitHub Actions**.
* **Smart Filtering:** Menggunakan algoritma gabungan:
    * ✅ **Trend Filter:** EMA-200 (Hanya memilih saham Uptrend).
    * ✅ **Momentum:** RSI < 60 (Mencari saham diskon/koreksi wajar).
    * ✅ **Signal:** MACD Golden Cross (Konfirmasi momentum positif).
* **Auto-Reporting:** Hasil screening disimpan otomatis ke dalam file CSV (`rekomendasi_saham.csv`) untuk analisis lebih lanjut.

## 🛠️ Teknologi yang Digunakan
* **Language:** Python 3.9
* **Libraries:** `yfinance` (Data), `pandas-ta` (Technical Analysis), `pandas`
* **Infrastructure:** GitHub Actions (CI/CD Cron Job)

## 📊 Hasil Screening Terbaru
Lihat file [rekomendasi_saham.csv](rekomendasi_saham.csv) untuk melihat rekomendasi saham hari ini.

---
*Disclaimer: Proyek ini dibuat untuk tujuan edukasi dan portofolio Data Science/Quantitative Finance. Bukan saran finansial.*
