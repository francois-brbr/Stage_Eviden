import psycopg2
import csv
import os
from dotenv import load_dotenv
from io import StringIO

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Configuration de la connexion à la base de données PostgreSQL
db_config = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# Chemins vers les fichiers .csv
csv_file_path_price = '/usr/local/airflow/data/new_stock_data_prices.csv'
csv_file_volume = '/usr/local/airflow/data/new_stock_data_volumes.csv'

# Nom des tables
table_price = 'stock_data_prices'
table_volume = 'stock_data_volumes'

# Connexion à la base de données
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()


# ----------------------------------------------------------------- INSERTION PRICES --------------------------------------------------------------------- #

with open(csv_file_path_price, 'r') as f: # Lecture du fichier "new_stock_data_prices.csv"

    csv_data = StringIO(f.read())  # Utilisation de StringIO pour simuler un fichier en mémoire

    reader = csv.reader(csv_data) # Utilisation de csv.reader pour lire le fichier CSV

    next(reader) # Lecture de l'en-tête pour obtenir les noms de colonnes

    for row in reader:
            date = row[0]  # La première colonne est la date
            processed_row = [None if value == '' else value for value in row]
            cursor.execute(f"SELECT 1 FROM {table_price} WHERE date = %s", (date,))  # Vérifier si la date existe déjà dans la table
            if cursor.fetchone() is None:
                insert_query = f"INSERT INTO {table_price} (date, GSPC, STOXX50E, FCHI, NASDAQ, DJI, N225) VALUES (%s, %s, %s, %s, %s, %s, %s)" # Si la date n'existe pas, insérer les données
                cursor.execute(insert_query, processed_row)

conn.commit() # Validation des changements


# -------------------------------------------------------------------- INSERTION VOLUMES ---------------------------------------------------------------------- #

with open(csv_file_volume, 'r') as f: # Lecture du fichier csv_file_volume
    
    csv_data = StringIO(f.read()) # Utilisation de StringIO pour simuler un fichier en mémoire

    reader = csv.reader(csv_data) # Utilisation de csv.reader pour lire le fichier CSV

    next(reader) # Lecture de l'en-tête pour obtenir les noms de colonnes

    for row in reader: # Insertion des données
            date = row[0] 
            processed_row = [None if value == '' else value for value in row]
            cursor.execute(f"SELECT 1 FROM {table_volume} WHERE date = %s", (date,)) # Vérifier si la date existe déjà dans la table
            if cursor.fetchone() is None:
                insert_query = f"INSERT INTO {table_volume} (date, GSPC, STOXX50E, FCHI, NASDAQ, DJI, N225) VALUES (%s, %s, %s, %s, %s, %s, %s)"  # Si la date n'existe pas, insérer les données
                cursor.execute(insert_query, processed_row)

conn.commit() # Validation des changements

# Fermeture de la connexion
cursor.close()
conn.close()

print("Données insérées avec succès.")