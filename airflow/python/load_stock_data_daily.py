import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Sélection des tickers avec Yahoo Finance
tickers = ['^GSPC', '^STOXX50E', '^FCHI', '^NDX', '^DJI', '^N225']

# Calcul des dates de façon à pouvoir faire la maj journalière
end_date = datetime.now()
start_date = end_date - timedelta(days=1)

# Téléchargement des données pour la journée
open_price = pd.DataFrame()
volume = pd.DataFrame()

for ticker in tickers:
    try:
        ticker_data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        if not ticker_data.empty:
            open_price[f'{ticker}_Open'] = ticker_data['Open']
            volume[f'{ticker}_Volume'] = ticker_data['Volume']
            print(f"Successfully downloaded data for {ticker}")
        else:
            print(f"No data downloaded for {ticker}")
    except Exception as e:
        print(f"Failed to download data for {ticker}: {e}")

# Enregistrement des données
open_price.to_csv("/usr/local/airflow/data/new_stock_data_prices.csv")
volume.to_csv("/usr/local/airflow/data/new_stock_data_volumes.csv")
