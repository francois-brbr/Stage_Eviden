import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Sélection des tickers avec Yahoo Finance
tickers = ['^GSPC', '^STOXX50E', '^FCHI', 'NQ=F', '^DJI', '^N225']

# Calcul de la date du jour
end_date = datetime.now()

# Téléchargement des données pour la dernière journée
data = pd.DataFrame()

for ticker in tickers:
    try:
        ticker_data = yf.download(ticker, start='2008-01-01', end=end_date.strftime('%Y-%m-%d'))
        if not ticker_data.empty:
            data[f'{ticker}_Open'] = ticker_data['Open']
            #data[f'{ticker}_Volume'] = ticker_data['Volume']
            print(f"Successfully downloaded data for {ticker}")
        else:
            print(f"No data downloaded for {ticker}")
    except Exception as e:
        print(f"Failed to download data for {ticker}: {e}")

# Enregistrement des données
data.to_csv("/usr/local/airflow/data/stock_data_prices.csv")