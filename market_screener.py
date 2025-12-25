import yfinance as yf
import pandas as pd
import pandas_ta as ta

# 1. Konfigurasi
# Daftar saham LQ45
tickers = [
    'BBRI.JK', 'BBCA.JK', 'BMRI.JK', 'BBNI.JK', 'TLKM.JK', 
    'ASII.JK', 'UNTR.JK', 'ICBP.JK', 'INDF.JK', 'GOTO.JK',
    'ANTM.JK', 'MDKA.JK', 'ADRO.JK', 'PTBA.JK', 'PGAS.JK'
]

print(f"Memulai screening untuk {len(tickers)} saham...")
print("-" * 50)

screener_results = []

for ticker in tickers:
    try:
        # 1. Ambil Data Historis
        df = yf.download(ticker, period="1y", progress=False)
        
        # Cek jika data kosong
        if df.empty:
            continue

        # === PERBAIKAN ERROR MULTIINDEX ===
        # Jika kolomnya bertingkat (misal: ('Close', 'BBRI.JK')), kita ratakan jadi ('Close') saja
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        # ==================================

        # 2. Hitung Indikator Teknikal
        # RSI (14)
        df['RSI'] = df.ta.rsi(length=14)
        
        # MACD (12, 26, 9)
        # Append=True agar kolom langsung masuk ke df utama tanpa perlu pd.concat manual
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        
        # EMA 200
        df['EMA_200'] = df.ta.ema(length=200)

        # Ambil data baris terakhir
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]

        # 3. LOGIKA SCREENING
        
        # Cek ketersediaan data EMA
        if pd.isna(last_row['EMA_200']):
            continue
            
        # Kriteria 1: Tren Naik (Harga > EMA 200)
        is_uptrend = last_row['Close'] > last_row['EMA_200']
        
        # Kriteria 2: Momentum RSI (Tidak Overbought/Mahal)
        # Kita longgarkan sedikit agar kamu bisa melihat hasil (RSI < 60)
        is_discount = last_row['RSI'] < 60

        # Kriteria 3: MACD Golden Cross
        # Nama kolom otomatis pandas_ta biasanya: MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
        # Kita pakai nama kolom dinamis agar tidak error jika setting beda
        macd_col = 'MACD_12_26_9'
        signal_col = 'MACDs_12_26_9'

        if macd_col not in df.columns:
            # Fallback jika nama kolom beda
            print(f"Skipping {ticker}, kolom MACD tidak ditemukan.")
            continue

        macd_line_now = last_row[macd_col]
        signal_line_now = last_row[signal_col]
        
        macd_line_prev = prev_row[macd_col]
        signal_line_prev = prev_row[signal_col]

        # Logika Cross: Kemarin MACD < Signal, Hari ini MACD > Signal
        is_golden_cross = (macd_line_now > signal_line_now) and (macd_line_prev < signal_line_prev)

        # DEBUGGING: Uncomment baris di bawah ini jika ingin melihat semua status saham
        # print(f"{ticker}: Uptrend={is_uptrend}, RSI={round(last_row['RSI'],2)}, Cross={is_golden_cross}")

        # STRATEGI:
        # Kita buat lebih fleksibel: Uptrend DAN (Diskon ATAU Golden Cross)
        if is_uptrend and (is_discount or is_golden_cross):
            status = "BUY (Golden Cross)" if is_golden_cross else "BUY (Trend + Discount)"
            
            print(f"[FOUND] {ticker} -> {status}")
            screener_results.append({
                'Ticker': ticker,
                'Close Price': int(last_row['Close']),
                'RSI': round(last_row['RSI'], 2),
                'EMA 200': int(last_row['EMA_200']),
                'Signal': status
            })

    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")

# 5. Output Hasil Akhir
print("-" * 50)
if screener_results:
    results_df = pd.DataFrame(screener_results)
    print("REKOMENDASI SAHAM HARI INI:")
    print(results_df)
    
    filename = 'rekomendasi_saham.csv'
    results_df.to_csv(filename, index=False)
    print(f"\nFile tersimpan: {filename}")
else:
    print("Tidak ada saham yang memenuhi kriteria strategi hari ini.")