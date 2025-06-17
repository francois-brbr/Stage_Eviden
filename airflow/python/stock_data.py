import yfinance as yf
import pandas as pd
import time

# Sélection des tickers avec Yahoo Finance
tickers = ['^GSPC', '^STOXX50E', '^FCHI', 'NQ=F', '^DJI', '^N225']  # GSPC = S&P500; STOXX50E = indice européen; FCHI = CAC40; NQF = Nasdaq100; DJI = Dow Jones Industrial; N225 = Nikkei225

# Téléchargement des données sur la plage de date souhaitée
data = pd.DataFrame()

for ticker in tickers:
    try:
        ticker_data = yf.download(ticker, start="2007-04-01", end="2025-06-15")
        if not ticker_data.empty:
            data[ticker] = ticker_data['Open']
            print(f"Successfully downloaded data for {ticker}")
        else:
            print(f"No data downloaded for {ticker}")
    except Exception as e:
        print(f"Failed to download data for {ticker}: {e}")

# Enregistrement des données
data.to_csv("/usr/local/airflow/data/stock_data_prices.csv")