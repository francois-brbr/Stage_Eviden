import pandas_datareader.data as web
import datetime

# Définir la période
start_date = datetime.datetime(2000,1,1)
end_date = datetime.datetime(2025,4,25)

# Récupérer les taux d'intérêt pour les États-Unis (Federal Funds Rate)
#interest_rate_data = web.DataReader('FEDFUNDS', 'fred', start_date, end_date)

# Récupérer les taux d'intérêt pour la zone euro
interest_rate_data = web.DataReader('FEDFUNDS', 'fred', start_date, end_date)

# Afficher les données
print(interest_rate_data.head())

# Enregistrer les données dans un fichier CSV
interest_rate_data.to_csv("interest_rates_usa.csv")
